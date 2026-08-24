from typing import Any

from app.database import supabase


def get_all_products() -> list[dict[str, Any]]:
    response = (
        supabase
        .table("products")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data or []


def get_product_by_id(product_id: int) -> dict[str, Any] | None:
    response = (
        supabase
        .table("products")
        .select("*")
        .eq("id", product_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def get_products_by_category(category: str) -> list[dict[str, Any]]:
    response = (
        supabase
        .table("products")
        .select("*")
        .ilike("category", category)
        .order("price")
        .execute()
    )

    return response.data or []


def search_products(
    query: str | None = None,
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    in_stock_only: bool = False,
) -> list[dict[str, Any]]:
    request = supabase.table("products").select("*")

    if query:
        request = request.or_(
            f"name.ilike.%{query}%,"
            f"brand.ilike.%{query}%,"
            f"description.ilike.%{query}%"
        )

    if category:
        request = request.ilike("category", category)

    if min_price is not None:
        request = request.gte("price", min_price)

    if max_price is not None:
        request = request.lte("price", max_price)

    if in_stock_only:
        request = request.gt("stock", 0)

    response = (
        request
        .order("price")
        .execute()
    )

    return response.data or []


def get_product_stock(product_id: int) -> int | None:
    response = (
        supabase
        .table("products")
        .select("stock")
        .eq("id", product_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]["stock"]