from fastapi import HTTPException

from .api import summarize_file


def analyze_added(files):
    summaries = []
    for filepath, code in files:
        try:
            summary = summarize_file(filepath, code)
            summaries.append(summary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error summarizing {filepath}:\n{e}")
    return "\n".join(summaries)