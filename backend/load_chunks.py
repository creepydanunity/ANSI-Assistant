# load_chunks.py

import json

# def load_chunks(path: str, collection):
#     with open(path, "r", encoding="utf-8") as f:
#         for i, line in enumerate(f):
#             obj = json.loads(line)
#             collection.add(
#                 documents=[obj["description"]],
#                 metadatas=[{
#                     "file_path": obj["file_path"],
#                     "start_line": obj["start_line"],
#                     "end_line": obj["end_line"]
#                 }],
#                 embeddings=[obj["embedding"]],
#                 ids=[f"chunk_{i}"]
#             )

def load_chunks(file_path, collection):
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            obj = json.loads(line)
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
