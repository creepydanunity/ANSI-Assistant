from llm.prompts import get_intent_prompt
from .embedding import process_chunks
from .summarize import enrich_chunks_with_descriptions
from .config import client

async def process_github(github_url: str, token: str):
    chunks_with_descriptions = await enrich_chunks_with_descriptions(github_url, token)
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

def classify_mode(question: str) -> str:
    intent_prompt = get_intent_prompt(question)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": intent_prompt}],
        temperature=0
    )
    return str(response.choices[0].message.content).strip().lower()