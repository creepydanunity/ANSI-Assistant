import json
import time
from openai import OpenAI
from tqdm import tqdm

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  # Использует OPENAI_API_KEY из .env или переменных окружения

INPUT_PATH = "chunks_with_descriptions.jsonl"
OUTPUT_PATH = "chunks_with_embeddings.jsonl"
MODEL = "text-embedding-ada-002"

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model=MODEL
    )
    return response.data[0].embedding

def process_chunks():
    with open(INPUT_PATH, "r", encoding="utf-8") as infile, \
         open(OUTPUT_PATH, "w", encoding="utf-8") as outfile:

        for line in tqdm(infile, desc="Embedding chunks"):
            chunk = json.loads(line)

            text = f"{chunk['description']}\n\n{chunk['code']}".strip()

            try:
                embedding = get_embedding(text)
                chunk["embedding"] = embedding
            except Exception as e:
                print(f"❌ Failed to embed: {chunk.get('name', 'unknown')} — {e}")
                chunk["embedding"] = None

            outfile.write(json.dumps(chunk, ensure_ascii=False) + "\n")
            time.sleep(1.0)  # защита от rate limit

if __name__ == "__main__":
    process_chunks()
