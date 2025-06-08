import os
import openai
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
MERGE_DIR = "merge"
OUTPUT_MD = "merge_summary.md"

def load_files_from_dir(directory):
    code_files = []
    for file_path in Path(directory).glob("*"):
        if file_path.is_file():
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
                code_files.append((file_path.name, code))
    return code_files

def summarize_file(filename, code):
    prompt = f"""You are a code reviewer. Summarize the following file in a few bullet points.
Filename: {filename}

```{code}```

Return only bullet points of what's implemented, added, or modified."""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def save_to_markdown(filename, summary, output_path):
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(f"## {filename}\n\n")
        f.write(summary + "\n\n---\n\n")

def main():
    # Clear previous summary
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("# Merge Summary\n\n")

    # Process all files
    files = load_files_from_dir(MERGE_DIR)
    for filename, code in files:
        print(f"Summarizing {filename}...")
        try:
            summary = summarize_file(filename, code)
            save_to_markdown(filename, summary, OUTPUT_MD)
            print(f"✅ Saved: {filename}")
        except Exception as e:
            print(f"❌ Error summarizing {filename}:\n{e}")

if __name__ == "__main__":
    main()