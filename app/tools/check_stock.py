from typing import Any

from app.services.product_service import get_product


def check_stock_tool(
    product_id: int,
    quantity: int = 1,
) -> dict[str, Any]:
    if quantity <= 0:
        return {
            "success": False,
            "available": False,
            "message": "Количество должно быть больше нуля.",
            "product_id": product_id,
            "requested_quantity": quantity,
            "stock": None,
        }

    product = get_product(product_id)

    if product is None:
        return {
            "success": False,
            "available": False,
            "message": f"Товар с ID {product_id} не найден.",
            "product_id": product_id,
            "requested_quantity": quantity,
            "stock": None,
        }

    stock = product.get("stock", 0)

    if stock <= 0:
        return {
            "success": True,
            "available": False,
            "message": f'Товар "{product["name"]}" сейчас отсутствует на складе.',
            "product_id": product_id,
            "product_name": product["name"],
            "requested_quantity": quantity,
            "stock": 0,
        }

    if quantity > stock:
        return {
            "success": True,
            "available": False,
            "message": (
                f'Недостаточно товара "{product["name"]}". '
                f"Доступно: {stock}, запрошено: {quantity}."
            ),
            "product_id": product_id,
            "product_name": product["name"],
            "requested_quantity": quantity,
            "stock": stock,
        }

    return {
        "success": True,
        "available": True,
        "message": "Товар доступен в нужном количестве.",
        "product_id": product_id,
        "product_name": product["name"],
        "requested_quantity": quantity,
        "stock": stock,
    }