from fastapi import APIRouter, HTTPException, Query

from app.repositories.order_repository import (
    get_order_by_id,
    get_orders_by_customer,
    update_order_status,
)
from app.schemas.order import OrderResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Получить заказ по ID",
)
def get_order(
    order_id: int,
):
    if order_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID заказа должен быть больше нуля.",
        )

    order = get_order_by_id(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Заказ не найден.",
        )

    return order


@router.get(
    "/customer/{customer_id}",
    summary="Получить заказы клиента",
)
def get_customer_orders(
    customer_id: int,
):
    if customer_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID клиента должен быть больше нуля.",
        )

    orders = get_orders_by_customer(customer_id)

    return {
        "customer_id": customer_id,
        "count": len(orders),
        "orders": orders,
    }


@router.patch(
    "/{order_id}/status",
    summary="Изменить статус заказа",
)
def change_order_status(
    order_id: int,
    status: str = Query(
        ...,
        min_length=1,
        max_length=30,
    ),
):
    if order_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID заказа должен быть больше нуля.",
        )

    allowed_statuses = {
        "pending",
        "confirmed",
        "processing",
        "shipped",
        "completed",
        "cancelled",
    }

    normalized_status = status.strip().lower()

    if normalized_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=(
                "Недопустимый статус заказа. "
                "Допустимые значения: "
                "pending, confirmed, processing, shipped, "
                "completed, cancelled."
            ),
        )

    existing_order = get_order_by_id(order_id)

    if existing_order is None:
        raise HTTPException(
            status_code=404,
            detail="Заказ не найден.",
        )

    updated_order = update_order_status(
        order_id=order_id,
        status=normalized_status,
    )

    if updated_order is None:
        raise HTTPException(
            status_code=500,
            detail="Не удалось изменить статус заказа.",
        )

    return {
        "success": True,
        "message": "Статус заказа обновлён.",
        "order": updated_order,
    }