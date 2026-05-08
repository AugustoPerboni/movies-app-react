from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    database_url: str

    jwt_public_key_path: Path
    access_token_expire_minutes: int = 15
    algorithm: str = "RS256"
    key_vault_url: str
    jwt_key_name: str

    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    



settings = Settings()
