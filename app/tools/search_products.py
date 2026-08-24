from typing import Any

from app.services.product_service import find_products


def search_products_tool(
    query: str | None = None,
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    in_stock_only: bool = True,
) -> dict[str, Any]:
    products = find_products(
        query=query,
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only,
    )

    return {
        "count": len(products),
        "products": products,
    }