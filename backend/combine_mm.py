import os
import openai

from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

MERGE_PATH = "merge_summary.md"
TASKS_PATH = "shared_backlog.md"
OUTPUT_PATH = "match_report.md"

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def compare_tasks_and_merge(task_md, merge_md):
    prompt = f"""
You are a senior engineer performing delivery alignment.

You are given:
1. A list of tasks extracted from meetings (task_md)
2. A list of summaries of code changes from a merge request (merge_md)

Instructions:

Step 1: For each task, determine whether it is **related** to anything done in the merge.
- A task is related if at least part of its described behavior or component appears in the merge.
- Skip unrelated tasks completely. Do not include them in the report.

Step 2: For each related task:
- Write the task title
- List ✅ aligned items: task requirements clearly fulfilled by the merge
- List ⚠️ missing items: things the task requires but the merge does not include
- List ➕ extra items: merge changes that are not mentioned in the task

Output format: well-structured Markdown grouped by task title.

--- TASK SUMMARY ---
{task_md}

--- MERGE SUMMARY ---
{merge_md}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()

def main():
    task_md = load_file(TASKS_PATH)
    merge_md = load_file(MERGE_PATH)
    print("🔍 Matching merge → tasks...")

    result = compare_tasks_and_merge(task_md, merge_md)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# Merge ⇄ Task Matching Report\n\n")
        f.write(result)

    print(f"✅ Done! Report written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
