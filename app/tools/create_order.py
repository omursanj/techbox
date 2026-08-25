from typing import Any

from app.repositories.customer_repository import get_or_create_customer
from app.repositories.order_repository import create_order_transaction
from app.services.order_service import (
    OrderValidationError,
    preview_order,
)


def _format_price(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def _format_order_confirmation(order: dict[str, Any]) -> str:
    items = order["items"]
    items_text = "\n".join(
        "| {name} | {quantity} шт. | {_price} ₸ | {_subtotal} ₸ |".format(
            name=item["name"],
            quantity=item["quantity"],
            _price=_format_price(item["price"]),
            _subtotal=_format_price(item["subtotal"]),
        )
        for item in items
    )

    status_labels = {
        "pending": "Принят автоматически, ожидает обработки",
        "confirmed": "Подтверждён",
        "processing": "В обработке",
        "shipped": "Передан в доставку",
        "completed": "Выполнен",
        "cancelled": "Отменён",
    }
    status = status_labels.get(
        order["status"],
        order["status"],
    )

    return (
        "Заказ успешно оформлен! 🎉\n\n"
        "**Детали заказа:**\n\n"
        "| Товар | Количество | Цена за шт. | Подытог |\n"
        "| --- | ---: | ---: | ---: |\n"
        f"{items_text}\n\n"
        f"**Доставка ({order['city']})**: "
        f"{_format_price(order['delivery_price'])} ₸\n"
        f"**Итого**: **{_format_price(order['total'])} ₸**\n\n"
        f"📦 **Статус:** {status}\n\n"
        "Заказ зарегистрирован автоматически. "
        "Дополнительное подтверждение не требуется."
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

    order = {
        "order_id": order_result["order_id"],
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "customer_phone": customer["phone"],
        "city": preview["city"],
        "items": preview["items"],
        "delivery_price": preview["delivery_price"],
        "total": order_result["total"],
        "status": order_result["status"],
    }

    return {
        "success": True,
        "message": "Заказ успешно создан.",
        "order": order,
        "customer_message": _format_order_confirmation(order),
    }
