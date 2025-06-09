from typing import List
from fastapi import HTTPException
from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Glossary

async def get_terms(db: AsyncSession, project_id: int) -> List[str]:
    stmt = (
        select(Glossary)
        .filter(Glossary.project_id == project_id)
    )

    result = await db.execute(stmt)

    terms = [i.term for i in result.scalars().all()]

    return terms

async def save_term(db: AsyncSession, project_id: int, term: str) -> Glossary:
    glossary = Glossary(
        project_id=project_id,
        term=term
    )

    db.add(glossary)
    await db.commit()
    await db.refresh(glossary)

    return glossary

async def get_undefined_terms(db: AsyncSession, project_id: int) -> List[Glossary]:
    stmt = (
        select(Glossary)
        .filter(Glossary.project_id == project_id)
    )

    result = await db.execute(stmt)

    undefined_wrods = list(result.scalars().all())

    return undefined_wrods

async def define_term(db: AsyncSession, term_id: int, definition: str):
    stmt = (
        select(Glossary)
        .filter(Glossary.id == term_id)
    )

    result = await db.execute(stmt)
    term = result.scalar_one_or_none()

    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    term.definition = definition
    await db.refresh(term)

async def retrieve_defined(db: AsyncSession, project_id: int):
    stmt = (
        select(Glossary)
        .filter(Glossary.project_id == project_id, Glossary.definition.isnot(None))
    )

    result = await db.execute(stmt)

    terms = result.scalars().all()

    return terms