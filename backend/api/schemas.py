from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    project_id: int
    mode: str = "strict" # "strict" or "advisory"

class AskResponse(BaseModel):
    answer: str

class GithubRequest(BaseModel):
    token: str

class GithubResponse(BaseModel):
    chunks: List[Dict[str, str | List[float]]]

class RepoResponse(BaseModel):
    id: int
    name: str
    repo_url: str
    project_id: int

    class Config:
        from_attributes = True

class RepoRequest(BaseModel):
    name: str
    repo_url: str
    token: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

class ProjectRequest(BaseModel):
    name: str

class ReloadRequest(BaseModel):
    token: str
    repo_url: str