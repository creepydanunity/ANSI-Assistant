from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List
from sqlalchemy.orm import Session

from api.deps import get_db
from auth.utils import get_current_user
from auth.models import ProjectRepo
from llm.api import process_github
from core.config import settings

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    project_id: int

class AskResponse(BaseModel):
    answer: str

class GithubRequest(BaseModel):
    github_repo: str
    token: str

class GithubResponse(BaseModel):
    chunks: List[Dict[str, str | List[float]]]

class RepoAdded(BaseModel):
    details: str

class RepoAdd(BaseModel):
    project_id: int
    name: str
    repo_url: str
    token: str

class ProjectCreated(BaseModel):
    name: str

@router.post("/ask", response_model=AskResponse)
def ask_user_question(
    data: AskRequest,
    user_id: int = Depends(get_current_user)
) -> Any:
    return {"user_id": {user_id}, "question": {data.question}, "answer": f"[MOCK]"}

@router.post("/create_project", response_model=ProjectCreated)
def project_create(data: GithubRequest,
    user_id: int = Depends(get_current_user)
) -> Any:
    pass

@router.post("/update_repo_chunks", response_model=GithubResponse)
def update_chunks(
    data: GithubRequest,
    user_id: int = Depends(get_current_user)
) -> Any:
    chunks = process_github(data.github_repo, settings.github_token)

    return {"user_id": {user_id}, "repo": {data.github_repo}, "chunks": f"{chunks}"}

@router.post("/repo", response_model=RepoAdded)
def repo_add(data: RepoAdd, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    #existing = db.query(ProjectRepo).filter(ProjectRepo.project_id == data.project_id).first()
    #if existing:
    #    raise HTTPException(status_code=400, detail="Email already registered")

    repoObj = ProjectRepo(
        name=data.name,
        repo_url=data.repo_url,
        token=data.token,
        project_id=data.project_id
    )

    db.add(repoObj)