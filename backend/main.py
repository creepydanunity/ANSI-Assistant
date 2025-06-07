import logging
from fastapi import FastAPI
from auth.routes import router as auth_router
from api.routes import router as api_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(title="AI Project Assistant")

app.include_router(auth_router)
app.include_router(api_router)

@app.get("/")
def root():
    return {"status": "ok"}