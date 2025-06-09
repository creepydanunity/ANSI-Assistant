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

class DeliveryAlignmentResponse(BaseModel):
    id: int
    pull_url: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
        
class AlignmentsResponse(BaseModel):
    alignments: List[DeliveryAlignmentResponse]

class GlossaryWordResponse(BaseModel):
    id: int
    project_id: int
    term: str

    class Config:
        orm_mode = True

class GlossaryResponse(BaseModel):
    glossary: List[GlossaryWordResponse]

class GlossaryData(BaseModel):
    id: int
    definition: str

class StatusOK(BaseModel):
    status: str