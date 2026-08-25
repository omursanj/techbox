from typing import Any

from app.database import supabase


def get_customer_by_id(customer_id: int) -> dict[str, Any] | None:
    response = (
        supabase
        .table("customers")
        .select("*")
        .eq("id", customer_id)
        .maybe_single()
        .execute()
    )

    # maybe_single().execute() returns None when no row matches.
    return response.data if response is not None else None


def get_customer_by_phone(phone: str) -> dict[str, Any] | None:
    response = (
        supabase
        .table("customers")
        .select("*")
        .eq("phone", phone)
        .maybe_single()
        .execute()
    )

    # A new customer is a valid case during order creation.
    return response.data if response is not None else None


def create_customer(
    name: str,
    phone: str,
) -> dict[str, Any]:

    response = (
        supabase
        .table("customers")
        .insert(
            {
                "name": name,
                "phone": phone,
            }
        )
        .select("*")
        .execute()
    )

    if not response.data:
        raise RuntimeError("Не удалось создать клиента.")

    return response.data[0]


def update_customer(
    customer_id: int,
    name: str | None = None,
    phone: str | None = None,
) -> dict[str, Any] | None:

    data: dict[str, Any] = {}

    if name is not None:
        data["name"] = name

    if phone is not None:
        data["phone"] = phone

    if not data:
        return get_customer_by_id(customer_id)

    response = (
        supabase
        .table("customers")
        .update(data)
        .eq("id", customer_id)
        .select("*")
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def get_or_create_customer(
    name: str,
    phone: str,
) -> dict[str, Any]:

    customer = get_customer_by_phone(phone)

    if customer:
        return customer

    return create_customer(
        name=name,
        phone=phone,
    )
