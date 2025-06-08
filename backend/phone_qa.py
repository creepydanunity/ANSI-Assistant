import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import openai
import os
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


LOG_PATH = "shared_backlog.md"

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

# Load logs once
if not Path(LOG_PATH).exists():
    raise FileNotFoundError(f"{LOG_PATH} not found")
with open(LOG_PATH, "r", encoding="utf-8") as f:
    LOG_TEXT = f.read()

SYSTEM_PROMPT = (
    "You are an assistant that answers user questions strictly based on the following project logs. "
    "If the logs do not contain the answer, respond with: 'Not found. No matching info in the logs.' "
    "If a decision was explicitly logged as undecided, uncertain, or pending, you may say so using the exact phrasing from the logs. "
    "Do not invent anything. Do not assume. Do not guess. Do not generalize. Only use direct, verifiable information from the logs."
)

@app.post("/ask")
async def ask(req: QuestionRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": LOG_TEXT},
                {"role": "user", "content": req.question}
            ],
            temperature=0,
        )
        return {"answer": response.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
