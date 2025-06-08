import json
from collections import defaultdict

INPUT_PATH = "chunks_with_embeddings.jsonl"
OUTPUT_PATH = "catalog_chunk.jsonl"

def generate_catalog():
    files = defaultdict(list)

    # Step 1: Read all chunks and group by file
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            files[obj["file_path"]].append(obj)

    # Step 2: Build description
    description_lines = ["This is a high-level summary of the project structure:\n"]

    for file_path, chunks in sorted(files.items()):
        description_lines.append(f"- `{file_path}`:")
        for ch in chunks:
            if ch["type"] in {"function", "class"}:
                entry = f"  - `{ch['name']}`: {ch['description']}"
                description_lines.append(entry)
        description_lines.append("")  # blank line between files

    # Step 3: Construct catalog chunk
    catalog_chunk = {
        "type": "catalog",
        "name": "__project_catalog__",
        "file_path": "__catalog__",
        "start_line": 0,
        "end_line": 0,
        "description": "\n".join(description_lines)
    }

    # Step 4: Write to file
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(json.dumps(catalog_chunk, ensure_ascii=False) + "\n")

    print(f"✅ Catalog chunk written to {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_catalog()
