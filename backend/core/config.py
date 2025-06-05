from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: AnyUrl
    secret_key: str
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 1440
    mode: str = "development" # TODO: Change for prod
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

settings = Settings()