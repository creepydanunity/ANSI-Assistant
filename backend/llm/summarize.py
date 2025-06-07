import time
from tqdm import tqdm
from openai import OpenAI
from utilities.chunking import ingest_repo
from core.config import settings


client = OpenAI(api_key=settings.openai_api_key)

OUTPUT_PATH = "chunks_with_descriptions.jsonl"
MODEL = "gpt-4"
TEMPERATURE = 0.2


def generate_description(code: str) -> str | None:
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
        
        if response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            return None
    except Exception as e:
        print(f"Error generating description: {e}")
        return ""


def enrich_chunks_with_descriptions(repo_link, token):
    inlist = ingest_repo(repo_link, token)
    chunks = []
    for chunk in tqdm(inlist, desc="Generating descriptions"):
        if "description" not in chunk or not chunk["description"]:
            chunk["description"] = generate_description(chunk["code"])
            time.sleep(1)  # avoid rate limiting
        chunks.append(chunk)

    return chunks