from dotenv import load_dotenv
import os

load_dotenv()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

import requests
import base64
from urllib.parse import urlparse
import tree_sitter_python as tspython
from tree_sitter import Language, Parser


# --- INIT TREE-SITTER ---
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

# --- UTILS ---
def parse_github_url(repo_url):
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) != 2:
        raise ValueError("Invalid GitHub repo URL")
    return path_parts[0], path_parts[1]

def get_default_branch(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()['default_branch']

def get_file_tree(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    tree = r.json()['tree']
    return [item['path'] for item in tree if item['type'] == 'blob' and item['path'].endswith('.py')]

def get_file_content(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    content = r.json()['content']
    return base64.b64decode(content).decode('utf-8')

def extract_chunks(code: str, file_path: str):
    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node
    chunks = []

    def walk(node):
        if node.type in ("function_definition", "class_definition"):
            name_node = node.child_by_field_name("name")
            name = code[name_node.start_byte:name_node.end_byte]
            chunk_code = code[node.start_byte:node.end_byte]
            chunks.append({
                "type": "function" if node.type == "function_definition" else "class",
                "name": name,
                "code": chunk_code.strip(),
                "file_path": file_path,
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1
            })
        for child in node.children:
            walk(child)

    walk(root_node)
    return chunks

def ingest_repo(repo_url):
    owner, repo = parse_github_url(repo_url)
    branch = get_default_branch(owner, repo)
    paths = get_file_tree(owner, repo, branch)

    all_chunks = []
    for path in paths:
        try:
            code = get_file_content(owner, repo, path)
            chunks = extract_chunks(code, path)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"Failed to process {path}: {e}")

    return all_chunks

# --- USAGE EXAMPLE ---
if __name__ == "__main__":
    repo_url = "https://github.com/creepydanunity/BaYaga"
    chunks = ingest_repo(repo_url)
    # from pprint import pprint
    # pprint(chunks)

import json

with open("chunks.jsonl", "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
