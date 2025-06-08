from typing import Optional
import httpx
import requests
import base64
from urllib.parse import urlparse

from tree_sitter import Node

from .language_config import EXTENSION_TO_LANGUAGE, LANGUAGE_NODE_TYPES
from .parser_languages import detect_language_from_path, loaded_parsers


def parse_github_url(repo_url: str) -> tuple[str, str]:
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) != 2:
        raise ValueError("Invalid GitHub repo URL")
    return path_parts[0], path_parts[1]


def get_default_branch(owner: str, repo: str, token: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(url, headers={"Authorization": f"token {token}"})
    r.raise_for_status()
    return r.json()['default_branch']


def get_file_tree(owner: str, repo: str, branch: str, token: str) -> list[str]:
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    r = requests.get(url, headers={"Authorization": f"token {token}"})
    r.raise_for_status()
    tree = r.json()['tree']

    valid_paths = []
    for item in tree:
        if item["type"] != "blob":
            continue
        path = item["path"]
        # Check exact filename first
        if path in EXTENSION_TO_LANGUAGE:
            valid_paths.append(path)
            continue
        # Otherwise check extension (case-insensitive)
        ext = "." + path.rsplit(".", 1)[-1].lower()
        if ext in EXTENSION_TO_LANGUAGE:
            valid_paths.append(path)
    return valid_paths


async def get_file_content(owner: str, repo: str, path: str, token: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        content = response.json()['content']
        return base64.b64decode(content).decode('utf-8')


def extract_chunks(code: str, file_path: str) -> list[dict]:
    """
    Parse `code` using the correct Tree-sitter parser (based on file_path),
    then walk the AST to extract function and class definitions according
    to LANGUAGE_NODE_TYPES[lang_key].

    For C-like functions, we first look two levels down under "declarator"
    (skipping parameter lists) to find the actual identifier. Only if that
    fails do we do a generic "name"/"identifier" search.
    """
    lang_key = detect_language_from_path(file_path)
    if not lang_key:
        return []

    node_types = LANGUAGE_NODE_TYPES.get(lang_key, {"functions": [], "classes": []})
    func_types = set(node_types.get("functions", []))
    class_types = set(node_types.get("classes", []))

    parser = loaded_parsers.get(lang_key)
    if parser is None:
        return []

    tree = parser.parse(code.encode("utf8"))
    root_node = tree.root_node

    chunks: list[dict] = []

    def find_cpp_identifier_in_decl(node: Node) -> Optional[Node]:
        """
        Given the "declarator" subtree for a C-family function, find the
        first child of type "identifier" or "field_identifier", skipping
        any "parameter_list" subtrees. Returns None if not found.
        """
        # If this node itself is an identifier of interest, return it
        if node.type in ("identifier", "field_identifier"):
            return node

        for child in node.children:
            # Do not descend into parameter lists
            if child.type == "parameter_list":
                continue
            # Recurse
            result = find_cpp_identifier_in_decl(child)
            if result:
                return result
        return None

    def find_identifier(node: Node) -> Optional[Node]:
        """
        Attempts to find the “true” name for a function or class node:

        1) For C-family function nodes, do a two-level drill-down:
           node → "declarator" → child with type "identifier" or "field_identifier",
           skipping over any parameter_list subtrees.

        2) Otherwise, look for a direct "name" or "identifier" child at this level.

        3) If still not found, recursively search the entire subtree for
           "name" or "identifier".
        """
        ntype = node.type

        # (1) C-family specific check
        if lang_key in ("c", "cpp", "objc", "cuda") and ntype in func_types:
            # First-level declarator (e.g., function_definition.declarator)
            decl = node.child_by_field_name("declarator")
            if decl:
                # Inside that, find the inner declarator (e.g., function_declarator.declarator)
                inner_decl = decl.child_by_field_name("declarator") or decl
                # Search that subtree for identifier/field_identifier
                id_node = find_cpp_identifier_in_decl(inner_decl)
                if id_node:
                    return id_node

            # Also handle the case where the node IS itself a function_declarator:
            if ntype == "function_declarator":
                id_node = find_cpp_identifier_in_decl(node)
                if id_node:
                    return id_node

        # (2) Direct child named "name" or "identifier"
        for field in ("name", "identifier"):
            direct = node.child_by_field_name(field)
            if direct:
                return direct

        # (3) Recurse over all children
        for child in node.children:
            found = find_identifier(child)
            if found:
                return found

        return None

    def walk(node: Node):
        ntype = node.type

        if ntype in func_types or ntype in class_types:
            name_node = find_identifier(node)
            name = (
                code[name_node.start_byte : name_node.end_byte]
                if name_node is not None
                else "<anonymous>"
            )

            snippet = code[node.start_byte : node.end_byte]
            chunks.append({
                "type": "function" if ntype in func_types else "class",
                "name": name,
                "code": snippet.strip(),
                "file_path": file_path,
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
                "node_type": ntype,
            })

        for child in node.children:
            walk(child)

    walk(root_node)
    return chunks


async def ingest_repo(repo_url: str, token: str = "") -> list[dict]:
    owner, repo = parse_github_url(repo_url)
    branch = get_default_branch(owner, repo, token)
    paths = get_file_tree(owner, repo, branch, token)

    all_chunks: list[dict] = []
    for path in paths:
        try:
            code = await get_file_content(owner, repo, path, token)
            chunks = extract_chunks(code, path)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"Failed to process {path}: {e}")

    return all_chunks
