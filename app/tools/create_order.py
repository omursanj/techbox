from typing import Any

from app.repositories.customer_repository import get_or_create_customer
from app.repositories.order_repository import create_order_transaction
from app.services.order_service import (
    OrderValidationError,
    preview_order,
)


def create_order_tool(
    customer_name: str,
    customer_phone: str,
    city: str,
    items: list[dict[str, int]],
) -> dict[str, Any]:
    """
    Создаёт заказ TechBox после всех проверок.

    items example:
    [
        {
            "product_id": 1,
            "quantity": 2
        }
    ]
    """

    try:
        # 1. Проверяем товар, остатки, город и рассчитываем сумму
        preview = preview_order(
            customer_name=customer_name,
            customer_phone=customer_phone,
            city=city,
            items=items,
        )

    except OrderValidationError as error:
        return {
            "success": False,
            "message": str(error),
            "order": None,
        }

    # 2. Находим существующего клиента
    # или создаём нового
    customer = get_or_create_customer(
        name=preview["customer_name"],
        phone=preview["customer_phone"],
    )

    # 3. Подготавливаем товары для RPC
    rpc_items = [
        {
            "product_id": item["product_id"],
            "quantity": item["quantity"],
        }
        for item in preview["items"]
    ]

    try:
        # 4. Создаём заказ через атомарную
        # PostgreSQL функцию
        order_result = create_order_transaction(
            customer_id=customer["id"],
            city=preview["city"],
            delivery_price=preview["delivery_price"],
            items=rpc_items,
        )

    except Exception as error:
        return {
            "success": False,
            "message": (
                "Не удалось создать заказ. "
                f"Причина: {str(error)}"
            ),
            "order": None,
        }

    return {
        "success": True,
        "message": "Заказ успешно создан.",
        "order": {
            "order_id": order_result["order_id"],
            "customer_id": customer["id"],
            "customer_name": customer["name"],
            "customer_phone": customer["phone"],
            "city": preview["city"],
            "items": preview["items"],
            "delivery_price": preview["delivery_price"],
            "total": order_result["total"],
            "status": order_result["status"],
        },
    }