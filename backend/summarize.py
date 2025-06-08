import os
import json
import time
from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI()  # Automatically uses OPENAI_API_KEY from env

INPUT_PATH = "chunks.jsonl"
OUTPUT_PATH = "chunks_with_descriptions.jsonl"
MODEL = "gpt-4"
TEMPERATURE = 0.2


def generate_description(code: str) -> str:
    prompt = f"""You are a Python expert. Summarize what the following code does in 1–2 clear sentences:

```python
{code.strip()}
```"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error generating description: {e}")
        return ""


def enrich_chunks_with_descriptions():
    with open(INPUT_PATH, "r", encoding="utf-8") as infile, open(OUTPUT_PATH, "w", encoding="utf-8") as outfile:
        for line in tqdm(infile, desc="Generating descriptions"):
            chunk = json.loads(line)
            if "description" not in chunk or not chunk["description"]:
                chunk["description"] = generate_description(chunk["code"])
                time.sleep(1)  # avoid rate limiting
            outfile.write(json.dumps(chunk, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    enrich_chunks_with_descriptions()
