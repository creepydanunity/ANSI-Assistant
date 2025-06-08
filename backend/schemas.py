import json
import re
from collections import defaultdict

def load_chunks(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def extract_imports(code: str):
    pattern = re.compile(r"from\s+([.\w_]+)\s+import|import\s+([.\w_]+)")
    matches = pattern.findall(code)
    imports = set()
    for match in matches:
        imp = match[0] or match[1]
        if imp:
            imports.add(imp.split('.')[0])  # use only top-level module
    return imports

def sanitize_id(s: str):
    return s.replace("/", "_").replace(".", "_").replace("-", "_")

def build_graph(chunks):
    graph = defaultdict(list)
    imports_map = defaultdict(set)
    file_paths = set()

    for chunk in chunks:
        file_path = chunk["file_path"]
        file_paths.add(file_path)
        file_node = sanitize_id(file_path)

        # what is inside the file
        node_id = f"{file_node}_{chunk['name']}"
        label = f"{chunk['type']} {chunk['name']}()".replace("function", "def").replace("class", "class")
        graph[file_node].append((node_id, label))

        # collect import relations
        imported = extract_imports(chunk["code"])
        imports_map[file_node].update(imported)

    return graph, imports_map, file_paths

def guess_file_from_import(import_name: str, file_paths):
    for path in file_paths:
        if import_name in path:
            return sanitize_id(path)
    return None

def render_mermaid(graph, imports_map, file_paths):
    lines = ["graph TD"]
    for file_node, children in graph.items():
        lines.append(f'  {file_node}["{file_node.replace("_", "/")}"]')
        for child_id, label in children:
            lines.append(f'  {file_node} --> {child_id}["{label}"]')

    # add cross-file import dependencies
    for src_file, imports in imports_map.items():
        for imp in imports:
            target_file = guess_file_from_import(imp, file_paths)
            if target_file and target_file != src_file:
                lines.append(f'  {src_file} --> {target_file}')

    return "\n".join(lines)

if __name__ == "__main__":
    chunks = load_chunks("chunks_with_embeddings.jsonl")  # path to your JSONL file
    graph, imports_map, file_paths = build_graph(chunks)
    mermaid = render_mermaid(graph, imports_map, file_paths)

    with open("full_component_graph.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid)

    print("✅ Mermaid graph written to full_component_graph.mmd")
