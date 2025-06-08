from fastapi import HTTPException

from .api import summarize_file


def analyze_added(files):
    summaries = []
    for ff in files:
        try:
            summary = summarize_file(ff["path"], ff["content"])
            summaries.append(summary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error summarizing {ff["path"]}:\n{e}")
    return "\n".join(summaries)