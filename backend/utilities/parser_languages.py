import os
from typing import get_args
from tqdm import tqdm
from tree_sitter_language_pack import get_parser, SupportedLanguage

from .language_config import EXTENSION_TO_LANGUAGE

loaded_parsers = {}

for key in tqdm(get_args(SupportedLanguage), desc="Loading parsers"):
    try:
        parser = get_parser(key)
        loaded_parsers[key] = parser
    except Exception as e:
        print(f"Error loading '{key}': {e}")

def detect_language_from_path(file_path: str) -> str | None:
    filename = os.path.basename(file_path)
    if filename in EXTENSION_TO_LANGUAGE:
        return EXTENSION_TO_LANGUAGE[filename]
    _, ext = os.path.splitext(filename.lower())
    return EXTENSION_TO_LANGUAGE.get(ext)