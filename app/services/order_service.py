from typing import Any

from app.repositories.customer_repository import get_or_create_customer
from app.repositories.product_repository import get_product_by_id
from app.services.delivery_service import get_delivery_info


class OrderValidationError(Exception):
    pass


def calculate_order_total(
    items: list[dict[str, Any]],
    delivery_price: int,
) -> int:
    products_total = sum(
        item["price"] * item["quantity"]
        for item in items
    )

    return products_total + delivery_price


def prepare_order_items(
    requested_items: list[dict[str, int]],
) -> list[dict[str, Any]]:
    prepared_items: list[dict[str, Any]] = []

    if not requested_items:
        raise OrderValidationError(
            "В заказе должен быть хотя бы один товар."
        )

    for requested_item in requested_items:
        product_id = requested_item["product_id"]
        quantity = requested_item["quantity"]

        if quantity <= 0:
            raise OrderValidationError(
                "Количество товара должно быть больше нуля."
            )

        product = get_product_by_id(product_id)

        if product is None:
            raise OrderValidationError(
                f"Товар с ID {product_id} не найден."
            )

        stock = product.get("stock", 0)

        if stock <= 0:
            raise OrderValidationError(
                f'Товар "{product["name"]}" отсутствует на складе.'
            )

        if quantity > stock:
            raise OrderValidationError(
                f'Недостаточно товара "{product["name"]}". '
                f"Доступно: {stock}, запрошено: {quantity}."
            )

        prepared_items.append(
            {
                "product_id": product["id"],
                "name": product["name"],
                "quantity": quantity,
                "price": product["price"],
                "stock": stock,
                "subtotal": product["price"] * quantity,
            }
        )

    return prepared_items


def preview_order(
    customer_name: str,
    customer_phone: str,
    city: str,
    items: list[dict[str, int]],
) -> dict[str, Any]:
    """
    Проверяет заказ и рассчитывает стоимость,
    но ещё НЕ создаёт его в базе.
    """

    if not customer_name.strip():
        raise OrderValidationError(
            "Не указано имя покупателя."
        )

    if not customer_phone.strip():
        raise OrderValidationError(
            "Не указан телефон покупателя."
        )

    delivery = get_delivery_info(city)

    if not delivery["available"]:
        raise OrderValidationError(
            delivery["reason"]
        )

    prepared_items = prepare_order_items(items)

    delivery_price = delivery["delivery_price"]

    total = calculate_order_total(
        items=prepared_items,
        delivery_price=delivery_price,
    )

    return {
        "customer_name": customer_name.strip(),
        "customer_phone": customer_phone.strip(),
        "city": delivery["city"],
        "items": prepared_items,
        "delivery_price": delivery_price,
        "total": total,
    }


def create_customer_for_order(
    customer_name: str,
    customer_phone: str,
) -> dict[str, Any]:
    return get_or_create_customer(
        name=customer_name,
        phone=customer_phone,
    )