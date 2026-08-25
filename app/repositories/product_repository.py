import re
from typing import Any

from app.database import supabase


def _get_search_terms(query: str) -> list[str]:
    return re.findall(
        r"\w+",
        query.casefold(),
        flags=re.UNICODE,
    )


def _product_matches_query(
    product: dict[str, Any],
    search_terms: list[str],
) -> bool:
    searchable_values = [
        product.get("name", ""),
        product.get("brand", ""),
        product.get("description", ""),
        product.get("category", ""),
    ]

    specifications = product.get("specifications") or {}

    if isinstance(specifications, dict):
        searchable_values.extend(
            f"{key} {value}"
            for key, value in specifications.items()
        )

    searchable_text = " ".join(
        str(value).casefold()
        for value in searchable_values
        if value is not None
    )

    return all(
        term in searchable_text
        for term in search_terms
    )


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

    products = response.data or []

    if not query:
        return products

    search_terms = _get_search_terms(query)

    if not search_terms:
        return products

    return [
        product
        for product in products
        if _product_matches_query(product, search_terms)
    ]


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
