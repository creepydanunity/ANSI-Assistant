# # api/routes/ask.py

# from fastapi import APIRouter, Request
# from agent.llm_agent import handle_user_query

# router = APIRouter()

# @router.post("/ask")
# async def ask(req: Request):
#     data = await req.json()
#     text = data.get("text", "")
#     reply = await handle_user_query(text)
#     return {"response": reply}
