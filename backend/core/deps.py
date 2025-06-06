from typing import AsyncGenerator
from chromadb import Collection
from sqlalchemy.ext.asyncio import AsyncSession
from db.dbconfig import postgresConfig, chromaConfig

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    postgreSession = postgresConfig.get_session()
    async with postgreSession() as session:
        yield session