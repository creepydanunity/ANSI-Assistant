import json
import chromadb
from chromadb.config import Settings

# Create or load Chroma DB
chroma_client = chromadb.Client(Settings(
    persist_directory="chroma_db",  # Folder where DB will be saved
    anonymized_telemetry=False
))

collection = chroma_client.get_or_create_collection("code_chunks")

# Load chunks and insert into Chroma
with open("chunks_with_embeddings.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        chunk = json.loads(line)
        if not chunk.get("embedding"):
            continue

        collection.add(
            ids=[f"chunk-{i}"],
            embeddings=[chunk["embedding"]],
            documents=[chunk["description"] + "\n\n" + chunk["code"]],
            metadatas=[{
                "file_path": chunk.get("file_path"),
                "type": chunk.get("type"),
                "name": chunk.get("name"),
            }]
        )
chroma_client.persist()
print("✅ Chroma DB persisted to disk at ./chroma_db")

