from typing import Any

from app.database import supabase


def get_all_delivery_cities() -> list[dict[str, Any]]:
    response = (
        supabase
        .table("delivery_cities")
        .select("*")
        .order("city")
        .execute()
    )

    return response.data or []


def get_delivery_by_city(city: str) -> dict[str, Any] | None:
    response = (
        supabase
        .table("delivery_cities")
        .select("*")
        .ilike("city", city)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def is_delivery_available(city: str) -> bool:
    delivery = get_delivery_by_city(city)

    if delivery is None:
        return False

    return bool(delivery.get("is_available", False))


def get_delivery_price(city: str) -> int | None:
    delivery = get_delivery_by_city(city)

    if delivery is None:
        return None

    if not delivery.get("is_available", False):
        return None

    return delivery.get("delivery_price")