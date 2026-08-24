from typing import Any

from app.services.delivery_service import get_delivery_info


def check_delivery_tool(
    city: str,
) -> dict[str, Any]:
    city = city.strip()

    if not city:
        return {
            "success": False,
            "available": False,
            "message": "Город не указан.",
            "city": None,
            "delivery_price": None,
        }

    delivery = get_delivery_info(city)

    if not delivery["available"]:
        return {
            "success": True,
            "available": False,
            "message": delivery["reason"],
            "city": delivery.get("city") or city,
            "delivery_price": None,
        }

    return {
        "success": True,
        "available": True,
        "message": "Доставка в этот город доступна.",
        "city": delivery["city"],
        "delivery_price": delivery["delivery_price"],
    }