from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "TechBox API"
    app_version: str = "1.0.0"
    debug: bool = True

    # Supabase
    supabase_url: str
    supabase_key: str

    # OpenRouter
    openrouter_api_key: str
    openrouter_model: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()