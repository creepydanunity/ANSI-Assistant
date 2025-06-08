

# import os
# from typing import List
# from fastapi import FastAPI
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import openai as openai_sdk
# import chromadb
# from chromadb.config import Settings
# from load_chunks import load_chunks  # 👈 внешний загрузчик
# import json

# load_dotenv()

# # --- OpenAI client ---
# client_openai = openai_sdk.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # --- Chroma persistent client ---
# client_chroma = chromadb.Client(Settings(persist_directory="chroma_db"))
# collection = client_chroma.get_or_create_collection(name="codebase")

# # --- FastAPI app ---
# app = FastAPI()

# # --- Request schema ---
# class AskRequest(BaseModel):
#     question: str
#     mode: str = "strict"  # "strict" or "advisory"

# # --- Embedding helper ---
# def get_embedding(text: str) -> List[float]:
#     response = client_openai.embeddings.create(
#         input=[text],
#         model="text-embedding-ada-002"
#     )
#     return response.data[0].embedding

# @app.post("/ask")
# async def ask(req: AskRequest):
#     query_vec = get_embedding(req.question)

#     results = collection.query(query_embeddings=[query_vec], n_results=5)
#     documents = results["documents"][0]
#     metadatas = results["metadatas"][0]

#     context_parts = [
#         f"[{m['file_path']}:{m['start_line']}-{m['end_line']}]\n{d}"
#         for m, d in zip(metadatas, documents)
#     ]

#     # Добавим обзор проекта, если режим advisory
#     if req.mode == "advisory":
#         try:
#             with open("catalog_chunk.json", "r", encoding="utf-8") as f:
#                 catalog = json.load(f)
#                 context_parts.insert(0, f"[Project Catalog]\n{catalog['description']}")
#         except Exception:
#             pass

#     context = "\n\n".join(context_parts)

#     system_prompt = (
#         "You are a senior backend engineer reviewing a specific codebase. "
#         "Use the provided code context to answer questions about its architecture and implementation."
#         "Avoid vague phrases and general programming advice; be specific, confident, and professional."


#         if req.mode == "advisory"
#         else
#         "You are a code assistant. Answer strictly based on the provided context. "
#         "If the context does not contain the answer, respond with 'No relevant information found.' "
#         "Do not make anything up."
#     )

#     prompt = f"""The following are code-related descriptions from a project:\n{context}\n\nQuestion: {req.question}\nAnswer:"""

#     response = client_openai.chat.completions.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0 if req.mode == "strict" else 0.3
#     )

#     return {"answer": response.choices[0].message.content}


# # --- Reload embeddings manually ---
# @app.post("/reload_embeddings")
# async def reload_embeddings():
#     load_chunks("chunks_with_embeddings.jsonl", collection)
#     return {"status": "reloaded", "count": collection.count()}

import os
import json
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import openai as openai_sdk
import chromadb
from chromadb.config import Settings
from load_chunks import load_chunks

load_dotenv()

# --- OpenAI client ---
client_openai = openai_sdk.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Chroma persistent client ---
client_chroma = chromadb.Client(Settings(persist_directory="chroma_db"))
collection = client_chroma.get_or_create_collection(name="codebase")

# --- FastAPI app ---
app = FastAPI()

# --- Request schema ---
class AskRequest(BaseModel):
    question: str

# --- Embedding helper ---
def get_embedding(text: str) -> List[float]:
    response = client_openai.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# --- Mode classification via GPT ---
def classify_mode(question: str) -> str:
    intent_prompt = f"""
Classify the following question as either "strict" or "advisory".

Rules:
- Use "strict" if the question requires factual answers strictly from code.
- Use "advisory" if the question asks for design advice, recommendations, or architectural insights.

Only output one word: strict or advisory.

Question: {question}
Answer:"""

    response = client_openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": intent_prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()

# --- Ask route ---
@app.post("/ask")
async def ask(req: AskRequest):
    mode = classify_mode(req.question)

    query_vec = get_embedding(req.question)
    results = collection.query(query_embeddings=[query_vec], n_results=5)
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = [
        f"[{m['file_path']}:{m['start_line']}-{m['end_line']}]\n{d}"
        for m, d in zip(metadatas, documents)
    ]

    if mode == "advisory":
        try:
            with open("catalog_chunk.json", "r", encoding="utf-8") as f:
                catalog = json.load(f)
                context_parts.insert(0, f"[Project Catalog]\n{catalog['description']}")
        except Exception:
            pass

    context = "\n\n".join(context_parts)

    system_prompt = (
        "You are a senior backend engineer reviewing a specific codebase. "
        "Use the provided code context to answer questions about its architecture and implementation. "
        "Avoid vague phrases and general programming advice; be specific, confident, and professional."
        if mode == "advisory"
        else
        "You are a code assistant. Answer strictly based on the provided context. "
        "If the context does not contain the answer, respond with 'No relevant information found.' "
        "Do not make anything up."
    )

    prompt = f"""The following are code-related descriptions from a project:\n{context}\n\nQuestion: {req.question}\nAnswer:"""

    response = client_openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0 if mode == "strict" else 0.3
    )

    return {
        "mode": mode,
        "answer": response.choices[0].message.content
    }

# --- Reload embeddings manually ---
@app.post("/reload_embeddings")
async def reload_embeddings():
    load_chunks("chunks_with_embeddings.jsonl", collection)
    return {"status": "reloaded", "count": collection.count()}
