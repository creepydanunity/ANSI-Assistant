from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    project_id: int

class AskResponse(BaseModel):
    mode: str
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

class TranscriptData(BaseModel):
    content: str
    timestamp: str # Format: dd.mm.YYYY HH:MM

class RepoOut(BaseModel):
    repo_id: int
    name: str
    repo_url: str
    repo_token: str

class ProjectOut(BaseModel):
    project_id: int
    project_name: str
    repos: List[RepoOut]

class ProjectsRepos(BaseModel):
    projects: List[ProjectOut]

class TranscriptionRead(BaseModel):
    id: int
    last_update: datetime
    content: str

    class Config:
        orm_mode = True