from datetime import datetime
import json
import time
from typing import Any, Dict, List
from utilities.transcription_parser import extract_json_from_response
from llm.prompts import get_alignment_prompt, get_glossary_prompt, get_intent_prompt, get_summarization_prompt, get_transcription_prompt
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

def generate_structured_tasks(transcript_text: str, backlog_text: str, source_date: str) -> list:
    full_prompt = (
    get_transcription_prompt().format(source_date=source_date) +f"\n\nTRANSCRIPT:\n{transcript_text}\n\nCURRENT BACKLOG:\n{backlog_text}")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that converts meeting transcripts into structured backlog entries."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.2,
        max_tokens=3500
    )
    
    raw_response = response.choices[0].message.content
    json_str = extract_json_from_response(raw_response)

    if json_str is not None:
        try:
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            print("[!] JSON decoding failed:", e)
            return []
    return []

def summarize_file(filepath, code) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": get_summarization_prompt(filepath, code)}],
        temperature=0.2
    )

    if response.choices[0].message.content:
        return response.choices[0].message.content.strip()
    return ""

def compare_tasks_and_merge(task_md, merge_md):
    prompt = get_alignment_prompt(task_md, merge_md)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    if response.choices[0].message.content:
        return response.choices[0].message.content.strip()
    return ""

def extract_glossary_llm(text: str, max_retries: int = 2) -> List[Dict[str, Any]]:
    """Extract acronyms with self-assessed confidence scores from the LLM."""
    prompt = get_glossary_prompt(text)
    
    for attempt in range(1, max_retries + 2):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Provide a JSON array of terms with model_guess and confidence."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.2
        )
        raw = (response.choices[0].message.content or "").strip()

        if raw.startswith("```"):
            lines = raw.splitlines()
            if lines and lines[0].startswith("```"):
                lines.pop(0)
            if lines and lines[-1].startswith("```"):
                lines.pop(-1)
            raw = "\n".join(lines).strip()


        try:
            entries = json.loads(raw)
            return entries
        except json.JSONDecodeError:
            if attempt > max_retries:
                return []
            time.sleep(attempt)
    return []