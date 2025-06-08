from urllib.parse import urlparse
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Any, Dict, List, Mapping, Sequence
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from api.schemas import AskResponse, AskRequest, ProjectRequest, ProjectResponse, RepoRequest, RepoResponse
from utilities.pr_parsing import categorize_files, fetch_changed_files
from llm.prompts import get_ask_prompt, get_ask_system_prompt
from db.util import add_chunks, delete_chunks, generate_catalog, move_chunks, store_chunks, update_chunks
from core.deps import get_db
from auth.utils import get_current_user
from core.models import Project, ProjectRepo, UserProject
from llm.api import classify_mode, process_github, process_question
from llm.embedding import get_embedding
from db.dbconfig import chromaConfig

router = APIRouter()
logger = logging.getLogger("api.routes")

@router.post("/projects", response_model=ProjectResponse)
async def project_create(
    data: ProjectRequest,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    
    stmt = (
        select(Project)
        .join(Project.users)
        .filter(
            Project.name == data.name,
            UserProject.user_id == user_id
        )
    )
    
    result = await db.execute(stmt)
    existing_project = result.scalar_one_or_none()

    if existing_project:
        raise HTTPException(status_code=400, detail="You already have a project with this name")
    
    new_project = Project(name=data.name)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    user_project = UserProject(user_id=user_id, project_id=new_project.id)
    db.add(user_project)
    await db.commit()
    await db.refresh(user_project)

    return ProjectResponse(
        id=new_project.id,
        name=new_project.name,
        created_at=new_project.created_at
    )

@router.post("/projects/{project_id}/repos", response_model=RepoResponse)
async def add_repo_to_project(
    project_id: int,
    data: RepoRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    
    stmt = select(Project).filter(Project.id == project_id)
    result = await db.execute(stmt)
    project = result.one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    stmt = select(UserProject).filter(UserProject.project_id == project_id, UserProject.user_id == user_id)
    result = await db.execute(stmt)
    user_project = result.one_or_none()

    if not user_project:
        raise HTTPException(status_code=403, detail="User does not have access to this project")
    
    parsed = urlparse(data.repo_url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")
    owner, repo = parts[0], parts[1].removesuffix(".git")

    hook_url = f"https://api.github.com/repos/{owner}/{repo}/hooks"
    payload = {
        "name": "web",
        "active": True,
        "events": ["pull_request"],
        "config": {
            "url": "http://64.225.65.211/webhook/github",
            "content_type": "json",
            "insecure_ssl": "1"
        }
    }
    headers = {
        "Authorization": f"token {data.token}",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(hook_url, json=payload, headers=headers)
    if resp.status_code >= 300:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create GitHub webhook: {resp.status_code} {resp.text}"
        )
    
    new_repo = ProjectRepo(
        name=data.name,
        repo_url=data.repo_url,
        token=data.token,
        project_id=project_id
    )

    db.add(new_repo)
    await db.commit()
    await db.refresh(new_repo)

    github_url = data.repo_url
    github_token = data.token

    try:
        chunks = await process_github(github_url, github_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process GitHub repo: {e}")

    try:
        result = store_chunks(project_id, new_repo.id, chunks)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed while storing embeddings in Chroma: {exc}")
    
    return new_repo

@router.get("/projects/{project_id}/reload")
async def reload_chunks(
    project_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    
    stmt = (
        select(UserProject)
        .filter(
            UserProject.project_id == project_id,
            UserProject.user_id == user_id
        )
    )

    result = await db.execute(stmt)
    user_project = result.one_or_none()
    if not user_project:
        raise HTTPException(status_code=403, detail="Access denied: you are not a member of this project")

    stmt = (
        select(ProjectRepo)
        .filter(
            ProjectRepo.project_id == project_id
        )
    )
    
    result = await db.execute(stmt)
    repos = result.all()

    if not repos:
        raise HTTPException(status_code=404, detail="Repository not found in this project")

    for repo in repos:
        github_url = repo.repo_url
        github_token = repo.token

        try:
            chunks = await process_github(github_url, github_token)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process GitHub repo: {e}")
    
        try:
            result = store_chunks(project_id, repo.id, chunks)
        except Exception as exc:
            raise HTTPException(status_code=500, detail="Failed while storing embeddings in Chroma")

    return {"status": "ok", "message": f"Chunks reloaded"}

@router.post("/webhook/github")
async def github_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.json()

    if not (
        payload.get("action") == "closed" 
        and payload.get("pull_request", {}).get("merged") is True
    ):
        return {"status": "ignored"}

    pr_number = payload["pull_request"]["number"]
    owner = payload["repository"]["owner"]["login"]
    repo = payload["repository"]["name"]

    raw_url = f"https://github.com/{owner}/{repo}"

    stmt = (
        select(ProjectRepo)
        .filter(
            ProjectRepo.repo_url == raw_url
        )
    )

    result = await db.execute(stmt)
    repo_obj = result.scalar_one_or_none()
    
    if not repo_obj:
        raise HTTPException(404, "Repository token not found")
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    files = await fetch_changed_files(api_url, repo_obj.token)

    categorized_files = await categorize_files(owner, repo, files, repo_obj.token)

    for removed_file in categorized_files["removed"]:
        delete_chunks(repo_obj.project_id, repo_obj.id, removed_file["path"])

    for renamed_file in categorized_files["renamed"]:
        move_chunks(repo_obj.project_id, repo_obj.id, renamed_file["old_path"], renamed_file["path"])

    for added_file in categorized_files["added"]:
        await add_chunks(repo_obj.project_id, repo_obj.id, added_file["path"], added_file["content"])

    for modified_file in categorized_files["modified"]:
        await update_chunks(repo_obj.project_id, repo_obj.id, modified_file["path"], modified_file["content"])

    logger.info(categorized_files)

    return {
        "status": "processed",
        "removed": len(categorized_files["removed"]),
        "renamed": len(categorized_files["renamed"]),
        "added": len(categorized_files["added"]),
        "modified": len(categorized_files["modified"])
    }

@router.post("/ask", response_model=AskResponse)
def ask_user_question(
    data: AskRequest,
    user_id: int = Depends(get_current_user),
) -> Any:
    mode = classify_mode(data.question)
    collection = chromaConfig.client_chroma.get_or_create_collection(name="codebase")
    query_vec = get_embedding(data.question)

    results = collection.query(
        query_embeddings=[query_vec],
        where={
                "project_id": data.project_id
            },
        n_results=5,
        include=["documents", "metadatas"]
    )

    docs_list = results.get("documents") or []
    if len(docs_list) == 0:
        return {"answer": "No relevant information found."}

    metas_list = results.get("metadatas") or []
    if len(metas_list) == 0:
        return {"answer": "No relevant information found."}

    raw_docs: List[str] = docs_list[0]
    raw_meta: Sequence[Mapping[str, Any]] = metas_list[0]
    
    if raw_meta is None:
        raw_meta = []

    context_parts: List[str] = []

    for m, d in zip(raw_meta, raw_docs):
        file_path = m.get("file_path", "unknown")
        start_line = m.get("start_line", "?")
        end_line = m.get("end_line", "?")
        context_parts.append(f"[{file_path}:{start_line}-{end_line}]\n{d}")

    # Добавим обзор проекта, если режим advisory
    if mode == "advisory":
        try:
            catalog = generate_catalog(data.project_id)
            context_parts.insert(0, catalog)
        except Exception:
            pass

    context = "\n\n".join(context_parts)
    system_prompt = get_ask_system_prompt(mode)
    prompt = get_ask_prompt(context, data.question)
    response = process_question(system_prompt, prompt, mode)

    return {"mode": mode, "answer": response.choices[0].message.content}