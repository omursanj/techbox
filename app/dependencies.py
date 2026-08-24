from supabase import Client

from app.config import Settings, get_settings
from app.database import get_supabase


def get_database() -> Client:
    """
    FastAPI dependency для получения клиента Supabase.
    """
    return get_supabase()


def get_app_settings() -> Settings:
    """
    FastAPI dependency для получения настроек приложения.
    """
    return get_settings()