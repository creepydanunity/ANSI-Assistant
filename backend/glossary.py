# # # # import os
# # # # import json
# # # # from typing import Dict, Any
# # # # from dotenv import load_dotenv
# # # # from pathlib import Path
# # # # import openai
# # # # from openai import OpenAI
# # # # from dotenv import load_dotenv
# # # # import os
# # # # import json
# # # # from typing import Dict, Any
# # # # from dotenv import load_dotenv
# # # # from pathlib import Path
# # # # from openai import OpenAI

# # # # load_dotenv()
# # # # client = OpenAI()

# # # # TRANSCRIPTS_DIR = "transcripts"
# # # # OUTPUT_PATH = "global_glossary.json"

# # # # def extract_glossary_llm(text: str) -> Dict[str, Any]:
# # # #     """Extract glossary from text using OpenAI, focusing only on unclear/tricky terms."""
# # # #     prompt = f"""
# # # # You are a glossary extractor for meeting transcripts.

# # # # Your task is to extract ONLY tricky, ambiguous, unclear, or team-specific terms from this transcript that may confuse a language model.

# # # # Rules:
# # # # - Do NOT include common terms.
# # # # - Include only terms whose meaning is vague, inferred from context, or likely to be specific to this team (like "July sprint", "Matrix", "jumpy deploy").
# # # # - If the meaning is unclear or a guess, set "needs_clarification": true.
# # # # - If you're confident and the term is generic (e.g., "API", "database"), do NOT include it at all.
# # # # - Return a JSON object where each key is the term, and the value has:
# # # #     - "definition": string
# # # #     - "needs_clarification": true

# # # # Transcript:
# # # # {text[:5000]}
# # # # """


# # # #     response = client.chat.completions.create(
# # # #         model="gpt-4",
# # # #         messages=[
# # # #             {"role": "system", "content": "You extract glossary terms that may confuse language models."},
# # # #             {"role": "user", "content": prompt}
# # # #         ],
# # # #         temperature=0.2
# # # #     )

# # # #     try:
# # # #         return json.loads(response.choices[0].message.content)
# # # #     except json.JSONDecodeError as e:
# # # #         print("⚠️ JSON decode error:", e)
# # # #         print("Raw response was:", response.choices[0].message.content[:500])
# # # #         return {}

# # # # def main():
# # # #     # Load existing glossary
# # # #     if os.path.exists(OUTPUT_PATH):
# # # #         with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
# # # #             global_glossary = json.load(f)
# # # #     else:
# # # #         global_glossary = {}

# # # #     for fname in os.listdir(TRANSCRIPTS_DIR):
# # # #         if fname.endswith(".txt") or fname.endswith(".md"):
# # # #             path = os.path.join(TRANSCRIPTS_DIR, fname)
# # # #             with open(path, encoding="utf-8") as f:
# # # #                 text = f.read()

# # # #             print(f"📄 Processing: {fname}")
# # # #             new_terms = extract_glossary_llm(text)

# # # #             # Add only new terms that aren't in the global glossary
# # # #             added = 0
# # # #             for term, info in new_terms.items():
# # # #                 if term not in global_glossary:
# # # #                     global_glossary[term] = info
# # # #                     added += 1

# # # #             print(f"✅ Added {added} new unclear terms from {fname}")

# # # #     with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
# # # #         json.dump(global_glossary, f, indent=2, ensure_ascii=False)

# # # #     print(f"\n📘 Global glossary saved to: {OUTPUT_PATH}")


# # # # if __name__ == "__main__":
# # # #     main()

# # # import os
# # # import json
# # # from typing import Dict
# # # from dotenv import load_dotenv
# # # from openai import OpenAI

# # # load_dotenv()
# # # client = OpenAI()

# # # TRANSCRIPTS_DIR = "transcripts"
# # # OUTPUT_PATH = "global_glossary.json"

# # # def extract_glossary_llm(text: str) -> Dict[str, str]:
# # #     """Extract only unclear or ambiguous terms from transcript using OpenAI."""
# # #     prompt = f"""
# # # You are analyzing a meeting transcript.

# # # Your task is to extract ONLY terms (words or short phrases) whose meaning you are **not fully sure about** or that could be **easily misunderstood or mistranslated** by a language model.

# # # This includes:
# # # - Rare abbreviations or uncommon acronyms
# # # - Misspellings, ambiguous identifiers, or phrases with unclear references

# # # DO NOT include:
# # # - Any terms you are confident about
# # # - Common English technical terms like "API", "JWT", "Celery", etc.
# # # - Well-described functions, paths, endpoints, tools

# # # Output a JSON object:
# # # - Keys: the unclear terms
# # # - Values: your **best guess** of the meaning from context (even if you're unsure)

# # # If all terms are clear and nothing seems ambiguous, return an **empty JSON object**.

# # # Transcript:
# # # {text[:5000]}
# # # """


# # #     response = client.chat.completions.create(
# # #         model="gpt-4",
# # #         messages=[
# # #             {"role": "system", "content": "You extract glossary terms that may confuse a language model."},
# # #             {"role": "user", "content": prompt}
# # #         ],
# # #         temperature=0.2
# # #     )

# # #     try:
# # #         return json.loads(response.choices[0].message.content)
# # #     except json.JSONDecodeError as e:
# # #         print("⚠️ JSON decode error:", e)
# # #         print("Raw response was:", response.choices[0].message.content[:500])
# # #         return {}

# # # def load_existing_glossary() -> Dict[str, str]:
# # #     """Load existing glossary safely if present."""
# # #     if os.path.exists(OUTPUT_PATH):
# # #         try:
# # #             with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
# # #                 content = f.read().strip()
# # #                 return json.loads(content) if content else {}
# # #         except json.JSONDecodeError as e:
# # #             print(f"⚠️ Could not parse glossary file. Starting fresh. Error: {e}")
# # #             return {}
# # #     return {}

# # # def main():
# # #     global_glossary = load_existing_glossary()

# # #     for fname in os.listdir(TRANSCRIPTS_DIR):
# # #         if fname.endswith(".txt") or fname.endswith(".md"):
# # #             path = os.path.join(TRANSCRIPTS_DIR, fname)
# # #             with open(path, encoding="utf-8") as f:
# # #                 text = f.read()

# # #             print(f"📄 Processing: {fname}")
# # #             new_terms = extract_glossary_llm(text)

# # #             added = 0
# # #             for term, definition in new_terms.items():
# # #                 if term not in global_glossary:
# # #                     global_glossary[term] = definition
# # #                     added += 1

# # #             print(f"✅ Added {added} new unclear terms from {fname}")

# # #     with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
# # #         json.dump(global_glossary, f, indent=2, ensure_ascii=False)

# # #     print(f"\n📘 Global glossary saved to: {OUTPUT_PATH}")

# # # if __name__ == "__main__":
# # #     main()

# # import os
# # import json
# # from typing import Dict, Any
# # from dotenv import load_dotenv
# # from openai import OpenAI

# # load_dotenv()
# # client = OpenAI()

# # TRANSCRIPTS_DIR = "transcripts"
# # OUTPUT_PATH = "global_glossary.json"

# # def extract_glossary_llm(text: str) -> Dict[str, Any]:
# #     """Extract only truly ambiguous acronyms/terms from a transcript."""
# #     prompt = f"""
# # You are a glossary extractor analyzing a meeting transcript.

# # Your job is to find only those terms or acronyms that cannot be mapped to a clear, standard definition from context alone—or where a language model might infer the wrong meaning. This includes:
# # 1. Rare or team-specific acronyms (e.g. “gtv”) whose expansion isn’t spelled out.
# # 2. Shorthand or misspellings that could be misinterpreted.

# # Do NOT include:
# # - Common technical acronyms whose meaning is obvious (e.g. “API”, “HTTP”).
# # - Terms whose meaning is fully defined or consistently used.

# # For each term you include, return an object with keys:
# # - "term": the exact acronym or phrase,
# # - "context_snippets": a list of 1–2 brief excerpts showing its usage,
# # - "model_guess": what a language model might mistakenly infer,
# # - "correct_expansion": your actual best guess.

# # Return a JSON array of these objects.

# # Transcript:
# # {text[:5000]}
# # """
# #     response = client.chat.completions.create(
# #         model="gpt-4",
# #         messages=[
# #             {"role": "system", "content": "You extract glossary terms that may confuse a language model."},
# #             {"role": "user", "content": prompt}
# #         ],
# #         temperature=0.2
# #     )
# #     try:
# #         return json.loads(response.choices[0].message.content)
# #     except json.JSONDecodeError as e:
# #         print("⚠️ JSON decode error:", e)
# #         print("Raw response:", response.choices[0].message.content)
# #         return []

# # def load_existing_glossary() -> Any:
# #     """Load existing glossary if present, else return empty list."""
# #     if os.path.exists(OUTPUT_PATH):
# #         try:
# #             with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
# #                 content = f.read().strip()
# #                 return json.loads(content) if content else []
# #         except json.JSONDecodeError as e:
# #             print(f"⚠️ Could not parse glossary file. Starting fresh. Error: {e}")
# #     return []

# # def main():
# #     global_glossary = load_existing_glossary()
# #     seen_terms = {entry["term"] for entry in global_glossary}

# #     for fname in os.listdir(TRANSCRIPTS_DIR):
# #         if not fname.lower().endswith((".txt", ".md")):
# #             continue

# #         path = os.path.join(TRANSCRIPTS_DIR, fname)
# #         with open(path, encoding="utf-8") as f:
# #             text = f.read()

# #         print(f"📄 Processing: {fname}")
# #         new_entries = extract_glossary_llm(text)
# #         added = 0
# #         for entry in new_entries:
# #             term = entry.get("term")
# #             if term and term not in seen_terms:
# #                 global_glossary.append(entry)
# #                 seen_terms.add(term)
# #                 added += 1

# #         print(f"✅ Added {added} new unclear terms from {fname}")

# #     with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
# #         json.dump(global_glossary, f, indent=2, ensure_ascii=False)

# #     print(f"\n📘 Global glossary saved to: {OUTPUT_PATH}")

# # if __name__ == "__main__":
# #     main()

# import os
# import json
# from typing import Any, List, Dict
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()
# client = OpenAI()

# TRANSCRIPTS_DIR = "transcripts"
# OUTPUT_PATH = "global_glossary.json"
# def extract_glossary_llm(text: str) -> List[Dict[str, str]]:
#     """Ask the LLM to return only truly doubtful acronyms with a worked example."""
#     prompt = f"""
# You are a glossary extractor analyzing a meeting transcript.

# Only surface acronyms or shorthand where you are **truly super uncertain** of the meaning from context alone.  
# **Do NOT** include any term whose most likely expansion is a **widely known** technology or acronym.  
# If you recognize it as one of those standard terms, assume you know it and do not return it.

# **Example output** (for truly ambiguous acronyms):
# ```json
# [
#   {{ "term": "gtv", "model_guess": "Google TV" }},
#   {{ "term": "ТС",  "model_guess": "транспортное средство" }}
# ]
# ```

# For each remaining term you include, return a JSON array of objects with:
# - "term": the exact acronym/phrase,
# - "model_guess": your single best guess.

# If no acronyms meet that “super uncertain” threshold, return an empty JSON array.

# Transcript:
# {text[:5000]}
# """
#     resp = client.chat.completions.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "Only extract acronyms you are highly unsure about."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.2
#     )
#     return json.loads(resp.choices[0].message.content)


# import time
# import json
# from openai import OpenAI

# client = OpenAI()

# def extract_glossary_llm(text: str, max_retries: int = 2) -> list[dict[str,str]]:
#     prompt = f"""
# You are a glossary extractor analyzing a meeting transcript.

# Only surface acronyms or shorthand where you are **truly super uncertain** of the meaning from context alone.  
# **Do NOT** include any term whose most likely expansion is a **widely known** technology or acronym.  
# If you recognize it as one of those standard terms, assume you know it and do not return it.

# **Example output** (for truly ambiguous acronyms):
# ```json
# [
#   {{ "term": "gtv", "model_guess": "Google TV" }},
#   {{ "term": "ТС",  "model_guess": "транспортное средство" }}
# ]
# ```

# For each remaining term you include, return a JSON array of objects with:
# - "term": the exact acronym/phrase,
# - "model_guess": your single best guess.

# If no acronyms meet that “super uncertain” threshold, return an empty JSON array.

# Transcript:
# {text[:5000]}
# """

#     for attempt in range(1, max_retries + 2):
#         resp = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role":"system", "content":"Only extract acronyms you are highly unsure about."},
#                 {"role":"user",   "content":prompt}
#             ],
#             temperature=0.2
#         )
#         raw = (resp.choices[0].message.content or "").strip()

#         # Quick sanity check
#         if raw.startswith("["):
#             try:
#                 return json.loads(raw)
#             except json.JSONDecodeError as e:
#                 print(f"⚠️ JSON decode error on attempt {attempt}: {e}")
#                 print("Raw:", raw)
#         else:
#             print(f"⚠️ Bad format on attempt {attempt}:", repr(raw))

#         if attempt <= max_retries:
#             # back off before retrying
#             time.sleep(1 * attempt)
#             print(f"🔄 Retrying (attempt {attempt + 1}/{max_retries + 1})…")
#         else:
#             print("❌ Max retries reached; returning empty list.")
#             return []

#     return []  # fallback, though loop should return or exit first


# def load_existing_glossary() -> List[Dict[str, str]]:
#     """Ensure we always load a list of term/guess objects."""
#     if os.path.exists(OUTPUT_PATH):
#         try:
#             data = json.load(open(OUTPUT_PATH, encoding="utf-8"))
#             if isinstance(data, list):
#                 return data
#         except Exception:
#             pass
#     return []

# def main():
#     glossary = load_existing_glossary()
#     seen = {entry["term"] for entry in glossary}

#     for fname in os.listdir(TRANSCRIPTS_DIR):
#         if not fname.lower().endswith((".txt", ".md")):
#             continue

#         with open(os.path.join(TRANSCRIPTS_DIR, fname), encoding="utf-8") as f:
#             text = f.read()

#         print(f"Processing {fname}…")
#         new = extract_glossary_llm(text)
#         added = 0
#         for item in new:
#             term = item.get("term")
#             if term and term not in seen:
#                 glossary.append(item)
#                 seen.add(term)
#                 added += 1

#         print(f"  → Added {added} uncertain terms.")

#     with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
#         json.dump(glossary, f, ensure_ascii=False, indent=2)
#     print(f"Saved {len(glossary)} total entries to {OUTPUT_PATH}")

# if __name__ == "__main__":
#     main()

import os
import json
import time
from typing import Any, List, Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

TRANSCRIPTS_DIR = "transcripts"
OUTPUT_PATH = "global_glossary.json"


def extract_glossary_llm(text: str, max_retries: int = 2) -> List[Dict[str, str]]:
    """Ask the LLM to return only truly doubtful acronyms with retries and fence stripping."""
    prompt = f"""
You are a glossary extractor analyzing a meeting transcript.

Only surface acronyms or shorthand where you are **truly super uncertain** of the meaning from context alone.  
**Do NOT** include any term whose most likely expansion is a **widely known** technology or acronym.  
If you recognize it as one of those standard terms, assume you know it and do not return it.

**Example output** (for truly ambiguous acronyms):
```json
[
  {{ "term": "gtv", "model_guess": "Google TV" }},
  {{ "term": "ТС",  "model_guess": "транспортное средство" }}
]
```

For each remaining term you include, return a JSON array of objects with:
- "term": the exact acronym/phrase,
- "model_guess": your single best guess.

If no acronyms meet that “super uncertain” threshold, return an empty JSON array.

Transcript:
{text[:5000]}
"""

    for attempt in range(1, max_retries + 2):
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Only extract acronyms you are highly unsure about."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.2
        )
        raw = (resp.choices[0].message.content or "").strip()

        # Strip fenced code blocks if present
        if raw.startswith("```"):
            lines = raw.splitlines()
            # drop opening fence
            if lines and lines[0].startswith("```"):
                lines.pop(0)
            # drop closing fence
            if lines and lines[-1].startswith("```"):
                lines.pop(-1)
            raw = "\n".join(lines).strip()

        # Quick sanity check and parse
        if raw.startswith("["):
            try:
                return json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON decode error on attempt {attempt}: {e}")
                print("Raw after stripping fences:", raw)
        else:
            print(f"⚠️ Bad format on attempt {attempt}:", repr(raw))

        if attempt <= max_retries:
            time.sleep(attempt)
            print(f"🔄 Retrying (attempt {attempt + 1}/{max_retries + 1})…")
        else:
            print("❌ Max retries reached; returning empty list.")
            return []

    return []


def load_existing_glossary() -> List[Dict[str, str]]:
    """Ensure we always load a list of term/guess objects."""
    if os.path.exists(OUTPUT_PATH):
        try:
            with open(OUTPUT_PATH, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print("⚠️ Unexpected format in glossary file—starting fresh.")
        except Exception as e:
            print(f"⚠️ Could not load glossary file: {e}")
    return []


def main():
    glossary = load_existing_glossary()
    seen = {entry.get("term") for entry in glossary if isinstance(entry, dict)}

    for fname in os.listdir(TRANSCRIPTS_DIR):
        if not fname.lower().endswith((".txt", ".md")):
            continue

        path = os.path.join(TRANSCRIPTS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            text = f.read()

        print(f"Processing {fname}…")
        new_entries = extract_glossary_llm(text)
        added = 0
        for item in new_entries:
            term = item.get("term")
            if term and term not in seen:
                glossary.append(item)
                seen.add(term)
                added += 1

        print(f"  → Added {added} uncertain terms.")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(glossary, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(glossary)} total entries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
