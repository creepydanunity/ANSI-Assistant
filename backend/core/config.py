from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_database_url: AnyUrl
    secret_key: str
    access_token_expire_minutes: int = 60
    openai_api_key: str
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

settings = Settings()