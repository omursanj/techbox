from typing import Any

from app.repositories.product_repository import (
    get_all_products,
    get_product_by_id,
    get_products_by_category,
    search_products,
)


def list_products() -> list[dict[str, Any]]:
    return get_all_products()


def get_product(product_id: int) -> dict[str, Any] | None:
    return get_product_by_id(product_id)


def list_products_by_category(
    category: str,
) -> list[dict[str, Any]]:
    return get_products_by_category(category)


def find_products(
    query: str | None = None,
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    in_stock_only: bool = True,
) -> list[dict[str, Any]]:

    products = search_products(
        query=query,
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only,
    )

    return products


def compare_products(
    product_ids: list[int],
) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []

    for product_id in product_ids:
        product = get_product_by_id(product_id)

        if product is not None:
            products.append(product)

    return products


def is_product_available(
    product_id: int,
    quantity: int = 1,
) -> bool:
    product = get_product_by_id(product_id)

    if product is None:
        return False

    stock = product.get("stock", 0)

    return stock >= quantity


def validate_requested_quantity(
    product_id: int,
    quantity: int,
) -> dict[str, Any]:
    if quantity <= 0:
        return {
            "valid": False,
            "reason": "Количество должно быть больше нуля.",
        }

    product = get_product_by_id(product_id)

    if product is None:
        return {
            "valid": False,
            "reason": "Товар не найден.",
        }

    stock = product.get("stock", 0)

    if stock <= 0:
        return {
            "valid": False,
            "reason": "Товара нет в наличии.",
            "available_stock": 0,
        }

    if quantity > stock:
        return {
            "valid": False,
            "reason": (
                f"Недостаточно товара на складе. "
                f"Доступно: {stock}."
            ),
            "available_stock": stock,
        }

    return {
        "valid": True,
        "available_stock": stock,
        "product": product,
    }