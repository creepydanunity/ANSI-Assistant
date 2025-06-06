import json
from fastapi import FastAPI
from auth.routes import router as auth_router
from utilities.chunking import ingest_repo
from llm.embedding import process_chunks
from llm.summarize import enrich_chunks_with_descriptions
from core.config import settings

OUTPUT_PATH = "chunks_with_embeddings.jsonl"
app = FastAPI(title="AI Project Assistant")

# Register routers
app.include_router(auth_router)

@app.get("/")
def root():
    return {"status": "ok"}