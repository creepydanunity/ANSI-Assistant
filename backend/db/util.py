from collections import defaultdict
from datetime import time
import json
import logging
from time import sleep
from typing import Any, Dict, List, Mapping, Sequence
from .dbconfig import chromaConfig
from tqdm import tqdm
from .dbconfig import chromaConfig

logger = logging.getLogger("db.util")

def load_chunks(chunks):
    collection = chromaConfig.client_chroma.get_or_create_collection(name="codebase")
    for i, obj in enumerate(chunks):
        collection.add(
            documents=[obj["description"]],
            metadatas=[{
                "file_path": obj["file_path"],
                "start_line": obj["start_line"],
                "end_line": obj["end_line"],
                "type": obj.get("type"),
                "name": obj.get("name")
            }],
            embeddings=[obj["embedding"]],
            ids=[f"{obj.get('type', 'chunk')}_{i}"]
        )
        sleep(1)


def store_embeddings(chunks):
    load_chunks(chunks)
    return {"status": "reloaded"}

def generate_catalog() -> None:
    """
    1) Fetches all chunks from Chroma (“codebase” collection).
    2) Groups them by metadata["file_path"].
    3) Builds a high‐level summary listing functions/classes under each file.
    4) Upserts the resulting “catalog chunk” back into Chroma under CATALOG_ID.
    """
    collection = chromaConfig.client_chroma.get_or_create_collection(name="codebase")

    # Fetch every stored document+metadata pair from Chroma
    all_items = collection.get(include=["documents", "metadatas"])
    docs: List[str] = all_items.get("documents") or []
    metas: Sequence[Mapping[str, Any]] = all_items.get("metadatas") or []

    # If there are no stored chunks, create a minimal “no chunks” catalog
    if not metas:
        catalog_description = "No code chunks found in the collection."
    else:
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
            # Then cast to str and strip whitespace.
            desc_val = meta.get("description", doc_text)
            desc_str = str(desc_val).strip()

            entry = {
                "type":        type_str,
                "name":        name_str,
                "description": desc_str,
            }
            files[file_path].append(entry)

        # Build the markdown‐style description
        description_lines: List[str] = ["This is a high‐level summary of the project structure:\n"]
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
            description_lines.append("")  # blank line between files
        catalog_description = "\n".join(description_lines).strip()

    # Construct metadata for the catalog entry
    catalog_metadata: Dict[str, Any] = {
        "type":       "catalog",
        "file_path":  "__catalog__",
        "start_line": 0,
        "end_line":   0,
        "name":       "__project_catalog__",
    }

    c_id = chromaConfig.get_catalog_id()
    # Upsert into Chroma under the fixed ID CATALOG_ID
    collection.add(
        ids=[c_id],
        documents=[catalog_description],
        metadatas=[catalog_metadata],
    )

    print("✅ Catalog chunk upserted into Chroma under ID:", c_id)