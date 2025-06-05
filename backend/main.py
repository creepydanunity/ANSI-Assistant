from fastapi import FastAPI
from backend.auth.routes import router as auth_router

app = FastAPI(title="AI Project Assistant")

# Register routers
app.include_router(auth_router)

@app.get("/")
def root():
    return {"status": "ok"}