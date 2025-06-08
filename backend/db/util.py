import asyncio
from collections import defaultdict
import hashlib
import logging
from typing import Any, Dict, List, Mapping, Sequence

from fastapi import HTTPException

from llm.embedding import process_chunks
from llm.summarize import generate_description
from utilities.chunking import extract_chunks
from .dbconfig import chromaConfig
from tqdm import tqdm


logger = logging.getLogger("db.util")

def fingerprint(text: str) -> str:
    """Return a stable SHA-256 hex digest for a chunk of text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

async def add_chunks(project_id, repo_id, path, content):
    inlist = extract_chunks(content, path)

    chunks = []
    for chunk in tqdm(inlist, desc=f"Generating descriptions for {path}"):
        if "description" not in chunk or not chunk["description"]:
            chunk["description"] = generate_description(chunk["code"])
            chunk["fp"] = fingerprint(chunk["code"])
            await asyncio.sleep(0.2)
        chunks.append(chunk)
    
    embedded_chunks = process_chunks(chunks)
    store_chunks(project_id, repo_id, embedded_chunks)

async def update_chunks(project_id, repo_id, path, content):
    inlist = extract_chunks(content, path)
    collection = chromaConfig.client_chroma.get_or_create_collection(name="codebase")

    saved_chunks = []
    to_delete = []
    for i, chunk in enumerate(tqdm(inlist, desc=f"Saving common chunks for {path}")):
        fp = fingerprint(chunk["code"])
        
        chunk_old = collection.get(
            where={
                "project_id": project_id,
                "repo_id": repo_id,
                "file_path": path,
                "fp": fp
            },
            limit=1,
            include=["documents", "metadatas", "embeddings"],
        )
        
        if chunk_old["metadatas"]:
            saved_chunks.append(chunk_old)
            to_delete.append(chunk)
    
    for chunk in to_delete:
        inlist.remove(chunk)

    collection.delete(
        where={
            "project_id": project_id,
            "repo_id": repo_id,
            "file_path": path,
        }
    )
    
    chunks = []
    for chunk in tqdm(inlist, desc=f"Generating descriptions for {path}"):
        if "description" not in chunk or not chunk["description"]:
            chunk["description"] = generate_description(chunk["code"])
            chunk["fp"] = fingerprint(chunk["code"])
            await asyncio.sleep(0.2)
        chunks.append(chunk)
    
    embedded_chunks = process_chunks(chunks)
    store_chunks(project_id, repo_id, embedded_chunks)
    restore_chunks(saved_chunks)

def restore_chunks(chunks):
    collection = chromaConfig.client_chroma.get_or_create_collection(name="codebase")

    docs, embs, metas, ids = [], [], [], []
    for i, obj in enumerate(chunks):
        docs.append(obj["documents"][0])
        embs.append(obj["embeddings"][0])
        ids.append(obj["ids"][0])
        metas.append(obj["metadatas"][0])
    
    collection.add(
        documents=docs,
        embeddings=embs,
        metadatas=metas,
        ids=ids,
    )

    return {"status": "restored"}

def store_chunks(project_id, repo_id, chunks):
    collection = chromaConfig.client_chroma.get_or_create_collection(name="codebase")

    docs, embs, metas, ids = [], [], [], []
    for i, obj in enumerate(chunks):
        raw_path = obj["file_path"]
        safe_path = raw_path.replace("/", "_")
        chunk_id = f"{project_id}_{repo_id}_{safe_path}_{i}"

        existing = collection.get(
            where={
                "project_id": project_id,
                "repo_id": repo_id,
                "file_path": raw_path,
                "fp": obj["fp"]
            }
        )

        if existing["ids"]:
            continue

        docs.append(obj["description"])
        embs.append(obj["embedding"])
        ids.append(chunk_id)
        metas.append({
            "file_path":   raw_path,
            "start_line":  obj["start_line"],
            "end_line":    obj["end_line"],
            "type":        obj.get("type"),
            "name":        obj.get("name"),
            "project_id":  project_id,
            "repo_id":     repo_id,
            "fp":          obj["fp"]
        })

    collection.add(
        documents=docs,
        embeddings=embs,
        metadatas=metas,
        ids=ids,
    )
    
    return {"status": "stored"}

def delete_chunks(
    project_id: int,
    repo_id: int,
    file_path: str
):
    collection = chromaConfig.client_chroma.get_or_create_collection(name="codebase")

    chunks = collection.get(
        where={
            "project_id": project_id,
            "repo_id": repo_id,
            "file_path": file_path,
        }
    )
    if not chunks["metadatas"]:
        return {"status": "no chunks found to delete"}

    collection.delete(
        where={
            "project_id": project_id,
            "repo_id": repo_id,
            "file_path": file_path,
        }
    )
    return {"status": "chunks deleted"}

def move_chunks(
    project_id: int,
    repo_id: int,
    old_path: str,
    new_path: str
):
    collection = chromaConfig.client_chroma.get_or_create_collection(name="codebase")

    chunks = collection.get(
        where={
            "project_id": project_id,
            "repo_id": repo_id,
            "file_path": old_path,
        },
        include=["documents", "metadatas", "embeddings"],
    )

    if not chunks["metadatas"]:
        raise HTTPException(status_code=404, detail="No chunks found to move")

    old_meta = chunks["metadatas"] or []
    old_docs = chunks["documents"] or []
    old_ids = chunks["ids"] or []
    old_embeddings = chunks["embeddings"] or []

    new_meta = []

    for meta in old_meta:
        new_meta.append(
            {
                "file_path": new_path,
                "start_line": meta["start_line"],
                "end_line": meta["end_line"],
                "type": meta.get("type"),
                "name": meta.get("name"),
                "project_id": project_id,
                "repo_id": repo_id,
                "fp": meta["fp"]
            }
        )

    collection.delete(
        where={
            "project_id": project_id,
            "repo_id": repo_id,
            "file_path": old_path,
        }
    )

    collection.add(
        documents=old_docs,
        embeddings=old_embeddings,
        metadatas=new_meta,
        ids=old_ids,
    )

def generate_catalog() -> str:
    """
    1) Fetches all chunks from Chroma ("codebase" collection).
    2) Groups them by metadata["file_path"].
    3) Builds and returns a high-level summary listing functions/classes under each file.
    """
    collection = chromaConfig.client_chroma.get_or_create_collection(name="codebase")

    # Fetch every stored document+metadata pair from Chroma
    all_items = collection.get(include=["documents", "metadatas"])
    docs: List[str] = all_items.get("documents") or []
    metas: Sequence[Mapping[str, Any]] = all_items.get("metadatas") or []

    # If there are no stored chunks, create a minimal "no chunks" catalog
    if not metas:
        return "No code chunks found in the collection."

    # Group metadata (and associated doc text) by file_path
    files: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for meta, doc_text in tqdm(zip(metas, docs), desc="Grouping metadata"):
        raw_fp = meta.get("file_path")
        file_path = str(raw_fp) if raw_fp is not None else "__unknown__"

        type_val = meta.get("type", "")
        type_str = str(type_val)

        name_val = meta.get("name", "<unnamed>")
        name_str = str(name_val)

        # If metadata has "description", use it; otherwise fall back to doc_text.
        desc_val = meta.get("description", doc_text)
        desc_str = str(desc_val).strip()

        entry = {
            "type":        type_str,
            "name":        name_str,
            "description": desc_str,
        }
        files[file_path].append(entry)

    # Build the markdown-style description
    description_lines: List[str] = ["This is a high-level summary of the project structure:\n"]
    for file_path, chunk_list in tqdm(sorted(files.items()), desc="Building md description"):
        description_lines.append(f"- `{file_path}`:")
        for ch in chunk_list:
            ctype = ch["type"]
            if ctype in {"function", "class"}:
                name = ch["name"]
                desc = ch["description"]
                if desc:
                    description_lines.append(f"  - `{name}`: {desc}")
                else:
                    description_lines.append(f"  - `{name}`")
        description_lines.append("")

    return "\n".join(description_lines).strip()