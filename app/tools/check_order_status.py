from typing import Any

from app.repositories.order_repository import get_order_by_id


STATUS_LABELS = {
    "pending": "Принят автоматически, ожидает обработки",
    "confirmed": "Подтверждён",
    "processing": "В обработке",
    "shipped": "Передан в доставку",
    "completed": "Выполнен",
    "cancelled": "Отменён",
}


def check_order_status_tool(
    order_id: int,
) -> dict[str, Any]:
    if order_id <= 0:
        return {
            "success": False,
            "message": "Номер заказа должен быть больше нуля.",
            "order": None,
        }

    order = get_order_by_id(order_id)

    if order is None:
        return {
            "success": False,
            "message": f"Заказ №{order_id} не найден.",
            "order": None,
        }

    status = order["status"]

    return {
        "success": True,
        "message": "Статус заказа получен.",
        "order": {
            "order_id": order["id"],
            "status": status,
            "status_label": STATUS_LABELS.get(status, status),
        },
    }
