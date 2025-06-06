from typing import AsyncGenerator
from chromadb import Collection
from sqlalchemy.ext.asyncio import AsyncSession
from db.dbconfig import postgresConfig, chromaConfig

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    postgreSession = postgresConfig.get_session()
    async with postgreSession() as session:
        yield session

def get_sync_db():
    postgreSession = postgresConfig.get_session()
def get_chromadb() -> Collection:
    chromaCollection = chromaConfig.get_collection()

    return chromaCollection