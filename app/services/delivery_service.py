from typing import Any

from app.repositories.delivery_repository import (
    get_all_delivery_cities,
    get_delivery_by_city,
)


def list_delivery_cities() -> list[dict[str, Any]]:
    return get_all_delivery_cities()


def get_delivery_info(city: str) -> dict[str, Any]:
    delivery = get_delivery_by_city(city)

    if delivery is None:
        return {
            "available": False,
            "reason": "Город не найден в списке доставки TechBox.",
            "city": city,
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