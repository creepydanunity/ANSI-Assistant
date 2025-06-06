from .embedding import process_chunks
from .summarize import enrich_chunks_with_descriptions
from .config import client

def process_github(github_url: str, token: str):
    chunks_with_descriptions = enrich_chunks_with_descriptions(github_url, token)
    chunks = process_chunks(chunks_with_descriptions)
    
    return chunks

def process_question(system_prompt: str, prompt: str, mode: str = "strict"):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0 if mode == "strict" else 0.3
    )

    return response