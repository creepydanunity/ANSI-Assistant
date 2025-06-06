import time
from typing import List
from openai import OpenAI
from tqdm import tqdm
from core.config import settings
from openai import OpenAI
from .config import client

MODEL = "text-embedding-ada-002"

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model=MODEL
    )
    return response.data[0].embedding

def process_chunks(chunks):
    embedded_chunks = []
    for chunk in tqdm(chunks, desc="Embedding chunks"):
        text = f"{chunk['description']}\n\n{chunk['code']}".strip()

        try:
            embedding = get_embedding(text)
            chunk["embedding"] = embedding
        except Exception as e:
            print(f"Failed to embed: {chunk.get('name', 'unknown')} — {e}")
            chunk["embedding"] = None

        chunk.__delitem__("code")
        embedded_chunks.append(chunk)
        time.sleep(1.0)

    return embedded_chunks