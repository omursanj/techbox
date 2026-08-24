from supabase import Client, create_client

from app.config import settings


def create_supabase_client() -> Client:
    """
    Создаёт клиент Supabase для работы с базой данных TechBox.
    """
    return create_client(
        settings.supabase_url,
        settings.supabase_key,
    )


supabase: Client = create_supabase_client()


def get_supabase() -> Client:
    """
    Возвращает готовый клиент Supabase.

    Эту функцию позже можно использовать
    в FastAPI dependencies и services.
    """
    return supabase