from typing import Any

from app.services.product_service import get_product


def get_product_tool(
    product_id: int,
) -> dict[str, Any]:
    product = get_product(product_id)

    if product is None:
        return {
            "found": False,
            "message": f"Товар с ID {product_id} не найден.",
            "product": None,
        }

    return {
        "found": True,
        "message": None,
        "product": product,
    }