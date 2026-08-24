from typing import Iterable


def calculate_subtotal(
    price: int,
    quantity: int,
) -> int:
    """
    Считает стоимость одной позиции заказа.
    """

    if price < 0:
        raise ValueError(
            "Цена не может быть отрицательной."
        )

    if quantity <= 0:
        raise ValueError(
            "Количество должно быть больше нуля."
        )

    return price * quantity


def calculate_products_total(
    items: Iterable[dict],
) -> int:
    """
    Считает общую стоимость всех товаров.

    Ожидает элементы формата:
    {
        "price": 24990,
        "quantity": 2
    }
    """

    total = 0

    for item in items:
        price = int(item["price"])
        quantity = int(item["quantity"])

        total += calculate_subtotal(
            price=price,
            quantity=quantity,
        )

    return total


def calculate_order_total(
    products_total: int,
    delivery_price: int,
) -> int:
    """
    Считает итог заказа с доставкой.
    """

    if products_total < 0:
        raise ValueError(
            "Стоимость товаров не может быть отрицательной."
        )

    if delivery_price < 0:
        raise ValueError(
            "Стоимость доставки не может быть отрицательной."
        )

    return products_total + delivery_price


def calculate_order_summary(
    items: list[dict],
    delivery_price: int,
) -> dict:
    """
    Возвращает полную сводку расчёта заказа.
    """

    prepared_items = []

    for item in items:
        price = int(item["price"])
        quantity = int(item["quantity"])

        subtotal = calculate_subtotal(
            price=price,
            quantity=quantity,
        )

        prepared_items.append(
            {
                **item,
                "subtotal": subtotal,
            }
        )

    products_total = calculate_products_total(
        prepared_items
    )

    total = calculate_order_total(
        products_total=products_total,
        delivery_price=delivery_price,
    )

    return {
        "items": prepared_items,
        "products_total": products_total,
        "delivery_price": delivery_price,
        "total": total,
    }