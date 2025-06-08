import openai
import os
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# === CONFIGURATION ===
TRANSCRIPTS_DIR = Path("transcripts")
BACKLOG_FILE = Path("shared_backlog.md")
PROMPT_TEMPLATE = '''You are a product assistant managing a shared project backlog.

You are given:
1. A meeting date
2. A transcript from the meeting
3. The current shared backlog (in Markdown)

Your job is to return an updated backlog as a list of JSON task objects. Each task must include:
- title: short and consistent (always use the feature or module name)
- status: "Open", "In Progress", or "Resolved"
- summary: one-sentence state summary (can summarize multiple aspects like UI/backend progress)
- history: list like {{"date": "YYYY-MM-DD", "description": "..."}}
- source_date: the meeting date you are given
- alerts (optional): list of {{"date": "YYYY-MM-DD", "issue": "..."}}

General rules:
- Use the provided meeting date {source_date} as the default for all history and alerts unless the transcript mentions a different one.
- Do not invent or guess dates.
- Record contradictions clearly in both `history` and `alerts`.

Grouping and normalization rules:
- Group all updates under the same feature or product module. A feature is something like "Analytics Dashboard", "Voice Command", "User Login", etc.
- Subcomponents like "UI", "Backend", "Access Control", "API", or "STT" must be recorded inside the same task — as part of `history` or `summary`.
- Normalize names: avoid splitting tasks by saying "X UI", "X backend", or "X (frontend)". Instead, just use "X" and consolidate all aspects.
- Do not create multiple tasks just because of rewording. Merge tasks that are clearly related by meaning, even if phrased differently in the transcript.
- If there's a disagreement across components (e.g. one says "UI is complete", another says "UI just started"), record this contradiction clearly in `alerts` and reflect both statements in `history`.

Output: ONLY a JSON array of task objects. Do not wrap it in Markdown or text commentary.
'''


def load_backlog_text() -> str:
    return BACKLOG_FILE.read_text(encoding="utf-8") if BACKLOG_FILE.exists() else ""


import re

def extract_json_from_response(response_text: str) -> str:
    # Remove Markdown-style code block if present
    match = re.search(r"```json\s*(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response_text.strip()


def generate_structured_tasks(transcript_text: str, backlog_text: str, source_date: str) -> list:
    full_prompt = (
    PROMPT_TEMPLATE.format(source_date=source_date) +f"\n\nTRANSCRIPT:\n{transcript_text}\n\nCURRENT BACKLOG:\n{backlog_text}")

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

    try:
        return json.loads(json_str)

    except json.JSONDecodeError as e:
        print("[!] JSON decoding failed:", e)
        return []



def merge_backlog_from_tasks(task_list: list):
    last_updated = task_list[0]['source_date'] if task_list else datetime.now().strftime("%Y-%m-%d")
    result = {}
    for item in task_list:
        title = item['title']
        block = [
            f"## {title}\n",
            f"- Status: {item['status']}\n",
            f"- Last updated: {last_updated}\n",
            f"- Summary: {item['summary']}\n",
            f"- History:\n"
        ]
        for entry in item['history']:
            block.append(f"  - {entry['date']}: {entry['description']}\n")
        if 'alerts' in item and item['alerts']:
            block.append(f"- Alerts:\n")
            for alert in item['alerts']:
                block.append(f"  - {alert['date']}: {alert['issue']}\n")
        block.append("\n")
        result[title] = block
    return result


def write_backlog(data: dict):
    with open(BACKLOG_FILE, "w", encoding="utf-8") as f:
        for block in data.values():
            f.writelines(block)


def process_transcripts():
    for path in TRANSCRIPTS_DIR.glob("*.txt"):
        date_str = path.stem
        print(f"[+] Processing: {path.name}")
        transcript = path.read_text(encoding="utf-8")
        backlog_text = load_backlog_text()
        tasks = generate_structured_tasks(transcript, backlog_text, date_str)
        print(f"    -> Extracted {len(tasks)} tasks from transcript.")
        updated_backlog = merge_backlog_from_tasks(tasks)
        write_backlog(updated_backlog)
        print("    -> Backlog updated with GPT-verified task list.\n")


if __name__ == "__main__":
    process_transcripts()