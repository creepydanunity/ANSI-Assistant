from datetime import datetime
from urllib.parse import urlparse
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Any, List, Mapping, Sequence
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import logging
from api.schemas import AlignmentsResponse, AskResponse, AskRequest, GlossaryData, GlossaryResponse, ProjectRequest, ProjectResponse, ProjectsRepos, RepoRequest, RepoResponse, TranscriptData, TranscriptionRead
from db.helper import define_term, get_terms, get_undefined_terms, save_term
from llm.utils import analyze_added
from utilities.transcription_parser import merge_backlog_from_tasks
from utilities.pr_parsing import categorize_files, fetch_changed_files
from llm.prompts import get_ask_prompt, get_ask_system_prompt
from db.util import add_chunks, delete_chunks, generate_catalog, move_chunks, store_chunks, update_chunks
from core.deps import get_db
from auth.utils import get_current_user
from core.models import DeliveryAlignment, Project, ProjectRepo, Transcription, UserProject
from llm.api import classify_mode, compare_tasks_and_merge, extract_glossary_llm, generate_structured_tasks, process_github, process_question
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

@router.get("/projects", response_model=ProjectsRepos)
async def get_all_projects(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    stmt = (
        select(Project)
        .join(UserProject, UserProject.project_id == Project.id)
        .filter(UserProject.user_id == user_id)
        .options(selectinload(Project.repos))
    )

    result = await db.execute(stmt)
    projects: Sequence[Project] = result.scalars().all()

    if not projects:
        raise HTTPException(404, detail="No projects found for this user")

    out_projects = []
    for p in projects:
        repos = [
            {
                "repo_id":    r.id,
                "name":       r.name,
                "repo_url":   r.repo_url,
                "repo_token": r.token,
            }
            for r in p.repos
        ]
        out_projects.append({
            "project_id":   p.id,
            "project_name": p.name,
            "repos":        repos
        })

    return {"projects": out_projects}
    
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
    
    return RepoResponse(id=new_repo.id, name=new_repo.name, repo_url=new_repo.repo_url, project_id=new_repo.project_id)

'''@router.get("/projects/{project_id}/reload")
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

    return {"status": "ok", "message": f"Chunks reloaded"}'''

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
    
    summaries = analyze_added(categorized_files["added"]) + "\n" + analyze_added(categorized_files["modified"])

    stmt = (
        select(Transcription)
        .filter(
            Transcription.project_id == repo_obj.project_id
        )
    )

    result = await db.execute(stmt)
    transcription = result.scalar_one_or_none()

    if transcription:
        diff = compare_tasks_and_merge(summaries, transcription.content)
        alignment = DeliveryAlignment(
            project_id=repo_obj.project_id,
            pull_url=payload["pull_request"]["url"],
            content=diff
        )

        db.add(alignment)
        await db.commit()
        await db.refresh(alignment)

        return {
            "status": "ok",
            "delivery_alignment": alignment,
            "removed": len(categorized_files["removed"]),
            "renamed": len(categorized_files["renamed"]),
            "added": len(categorized_files["added"]),
            "modified": len(categorized_files["modified"])
        }

    return {
        "status": "ok",
        "removed": len(categorized_files["removed"]),
        "renamed": len(categorized_files["renamed"]),
        "added": len(categorized_files["added"]),
        "modified": len(categorized_files["modified"])
    }

@router.get("/projects/{project_id}/alignments", response_model=AlignmentsResponse)
async def get_project_alignments(
    project_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
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
        select(DeliveryAlignment)
        .filter(
            UserProject.project_id == project_id
        )
    )

    result = await db.execute(stmt)
    alignments = result.scalars().all()

    if not alignments:
        raise HTTPException(status_code=404, detail="No related delivery alignments found")

    return {"alignments": alignments}

@router.post("/ask", response_model=AskResponse)
async def ask_user_question(
    data: AskRequest,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    stmt = (
        select(UserProject)
        .filter(
            UserProject.project_id == data.project_id,
            UserProject.user_id == user_id
        )
    )

    result = await db.execute(stmt)

    user_project = result.one_or_none()
    if not user_project:
        raise HTTPException(status_code=403, detail="Access denied: you are not a member of this project")
    
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

@router.post("/projects/{project_id}/transcription", response_model=TranscriptionRead)
async def add_transcript(
    data: TranscriptData,
    project_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
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
    
    dt = datetime.strptime(data.timestamp, "%d.%m.%Y %H:%M") 

    stmt = (
        select(Transcription)
        .where(
            Transcription.project_id == project_id
        )
    )

    result = await db.execute(stmt)

    transcription = result.scalar_one_or_none()

    if transcription is None:
        content = ""
    else:
        content = transcription.content

    dd, mm, yy = data.timestamp.split()[0].split(".")

    tasks = generate_structured_tasks(data.content, content, f"{yy}-{mm}-{dd}")

    updated_backlog_dict = merge_backlog_from_tasks(tasks)

    updated_backlog = ""

    for block_lines in updated_backlog_dict.values():
        updated_backlog += "".join(block_lines)

    if transcription is None:
        transcription = Transcription(
            project_id=project_id,
            content=updated_backlog,
            last_update=dt
        )
        db.add(transcription)
    else:
        transcription.content = updated_backlog
        transcription.last_update = dt

    await db.commit()
    await db.refresh(transcription)

    raw_glossary_entries = extract_glossary_llm(data.content)
    
    saved_entries = await get_terms(db, project_id)

    for entry in raw_glossary_entries:
        term = entry.get("term")
        confidence = entry.get("confidence")
        if term and term not in saved_entries and confidence and confidence < 0.69:
            await save_term(db, project_id, term)

    return TranscriptionRead(id=transcription.id, last_update=transcription.last_update, content=transcription.content)

@router.get(
    "/projects/{project_id}/glossary",
    response_model=GlossaryResponse
)
async def get_glossary(
    project_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
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
    
    undefined_words = await get_undefined_terms(db, project_id)

    return {"glossary": undefined_words}

@router.post(
    "/projects/{project_id}/glossary",
    response_model=GlossaryResponse
)
async def add_to_glossary(
    project_id: int,
    data: GlossaryData,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
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
    
    await define_term(db, data.id, data.definition)

    return {"status": "ok"}

@router.get(
    "/projects/{project_id}/transcription",
    response_model=TranscriptionRead
)
async def get_transcription(
    project_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(UserProject)
        .filter(
            UserProject.project_id == project_id,
            UserProject.user_id == user_id
        )
    )
    res = await db.execute(stmt)
    if res.scalar_one_or_none() is None:
        raise HTTPException(403, "Access denied: you are not a member of this project")

    stmt = select(Transcription).where(Transcription.project_id == project_id)
    res = await db.execute(stmt)
    transcription = res.scalar_one_or_none()
    if transcription is None:
        raise HTTPException(404, "No transcription found for this project")

    return TranscriptionRead(id=transcription.id, last_update=transcription.last_update, content=transcription.content)