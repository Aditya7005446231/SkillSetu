from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SkillSetu API"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./skillsetu.db"
    debug: bool = False
    openwebninja_api_key: str = ""
    openwebninja_api_host: str = "api.openwebninja.com"
    jsearch_country: str = "in"
    jsearch_query: str = "software developer internship"
    jsearch_num_pages: int = 1

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()
