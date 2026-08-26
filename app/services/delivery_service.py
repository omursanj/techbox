from typing import Any

from app.repositories.delivery_repository import (
    get_all_delivery_cities,
    get_delivery_by_city,
)


CITY_NAMES: dict[str, tuple[str, str]] = {
    "астана": ("Астана", "Astana"),
    "astana": ("Астана", "Astana"),
    "алматы": ("Алматы", "Almaty"),
    "almaty": ("Алматы", "Almaty"),
    "караганда": ("Караганда", "Karaganda"),
    "karaganda": ("Караганда", "Karaganda"),
    "шымкент": ("Шымкент", "Shymkent"),
    "shymkent": ("Шымкент", "Shymkent"),
    "павлодар": ("Павлодар", "Pavlodar"),
    "pavlodar": ("Павлодар", "Pavlodar"),
}


def normalize_city(city: str) -> str:
    """Возвращает каноническое русское название города."""
    city = city.strip()
    names = CITY_NAMES.get(city.casefold())

    return names[0] if names else city


def _city_variants(city: str) -> tuple[str, ...]:
    """Возвращает варианты для баз, где города могли быть сохранены по-разному."""
    city = city.strip()
    names = CITY_NAMES.get(city.casefold())

    if names is None:
        return (city,)

    return names


def list_delivery_cities() -> list[dict[str, Any]]:
    return get_all_delivery_cities()


def get_delivery_info(city: str) -> dict[str, Any]:
    requested_city = city.strip()
    delivery = next(
        (
            delivery
            for city_variant in _city_variants(requested_city)
            if (delivery := get_delivery_by_city(city_variant)) is not None
        ),
        None,
    )

    if delivery is None:
        return {
            "available": False,
            "reason": "Город не найден в списке доставки TechBox.",
            "city": normalize_city(requested_city),
            "delivery_price": None,
        }

    if not delivery.get("is_available", False):
        return {
            "available": False,
            "reason": "Доставка в этот город сейчас недоступна.",
            "city": delivery.get("city"),
            "delivery_price": None,
        }

    return {
        "available": True,
        "reason": None,
        "city": delivery.get("city"),
        "delivery_price": delivery.get("delivery_price"),
    }


def can_deliver(city: str) -> bool:
    delivery_info = get_delivery_info(city)

    return delivery_info["available"]


def calculate_delivery_price(city: str) -> int | None:
    delivery_info = get_delivery_info(city)

    if not delivery_info["available"]:
        return None

    return delivery_info["delivery_price"]
