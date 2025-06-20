import chromadb
from chromadb.config import Settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.config import settings

class PostgreConfig():
    def __init__(self):
        self.engine = create_async_engine(str(settings.postgres_database_url), future=True, echo=False)
        self.AsyncSessionLocal = async_sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
    
    def get_engine(self):
        return self.engine
    
    def get_session(self):
        return self.AsyncSessionLocal

class ChromaConfig():
    def __init__(self):
        self.client_chroma = chromadb.PersistentClient(path="chromadb", settings=Settings(persist_directory="chromadb", anonymized_telemetry=False))
        self.catalog_id: str = "__project_catalog__"
    
    def get_catalog_id(self) -> str:
        return self.catalog_id
    
postgresConfig = PostgreConfig()
chromaConfig = ChromaConfig()