from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    database_url: str

    jwt_private_key_path: Path
    jwt_public_key_path: Path
    access_token_expire_minutes: int = 15
    algorithm: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()