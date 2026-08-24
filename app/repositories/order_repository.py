from typing import Any

from app.database import supabase


def create_order(
    customer_id: int,
    city: str,
    delivery_price: int,
    total: int,
    status: str = "pending",
) -> dict[str, Any]:
    response = (
        supabase
        .table("orders")
        .insert(
            {
                "customer_id": customer_id,
                "city": city,
                "delivery_price": delivery_price,
                "total": total,
                "status": status,
            }
        )
        .select("*")
        .execute()
    )

    if not response.data:
        raise RuntimeError("Не удалось создать заказ.")

    return response.data[0]


def create_order_items(
    order_id: int,
    items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []

    for item in items:
        rows.append(
            {
                "order_id": order_id,
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "price": item["price"],
            }
        )

    response = (
        supabase
        .table("order_items")
        .insert(rows)
        .select("*")
        .execute()
    )

    return response.data or []


def get_order_by_id(
    order_id: int,
) -> dict[str, Any] | None:
    response = (
        supabase
        .table("orders")
        .select(
            """
            *,
            customers (
                id,
                name,
                phone
            ),
            order_items (
                id,
                product_id,
                quantity,
                price,
                products (
                    id,
                    name,
                    category,
                    brand
                )
            )
            """
        )
        .eq("id", order_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def get_orders_by_customer(
    customer_id: int,
) -> list[dict[str, Any]]:
    response = (
        supabase
        .table("orders")
        .select(
            """
            *,
            order_items (
                id,
                product_id,
                quantity,
                price
            )
            """
        )
        .eq("customer_id", customer_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []


def update_order_status(
    order_id: int,
    status: str,
) -> dict[str, Any] | None:
    response = (
        supabase
        .table("orders")
        .update(
            {
                "status": status,
            }
        )
        .eq("id", order_id)
        .select("*")
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def create_order_transaction(
    customer_id: int,
    city: str,
    delivery_price: int,
    items: list[dict],
) -> dict[str, Any]:
    rpc_items = [
        {
            "product_id": item["product_id"],
            "quantity": item["quantity"],
        }
        for item in items
    ]

    response = (
        supabase
        .rpc(
            "create_techbox_order",
            {
                "p_customer_id": customer_id,
                "p_city": city,
                "p_delivery_price": delivery_price,
                "p_items": rpc_items,
            },
        )
        .execute()
    )

    if response.data is None:
        raise RuntimeError(
            "Не удалось создать заказ."
        )

    return response.data