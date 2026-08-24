from fastapi import APIRouter, HTTPException, Query

from app.schemas.delivery import DeliveryResponse
from app.services.delivery_service import (
    get_delivery_info,
    list_delivery_cities,
)


router = APIRouter(
    prefix="/delivery",
    tags=["Delivery"],
)


@router.get(
    "",
    response_model=list[DeliveryResponse],
    summary="Получить список городов доставки",
)
def get_delivery_cities():
    return list_delivery_cities()


@router.get(
    "/check",
    summary="Проверить доставку в город",
)
def check_delivery(
    city: str = Query(
        ...,
        min_length=1,
        max_length=100,
        description="Город доставки",
    ),
):
    city = city.strip()

    if not city:
        raise HTTPException(
            status_code=400,
            detail="Город не указан.",
        )

    delivery = get_delivery_info(city)

    return {
        "city": delivery.get("city") or city,
        "available": delivery["available"],
        "delivery_price": delivery["delivery_price"],
        "message": delivery["reason"],
    }


@router.get(
    "/{city}",
    summary="Получить информацию о доставке в конкретный город",
)
def get_delivery_by_city(
    city: str,
):
    city = city.strip()

    if not city:
        raise HTTPException(
            status_code=400,
            detail="Город не указан.",
        )

    delivery = get_delivery_info(city)

    if not delivery["available"]:
        raise HTTPException(
            status_code=404,
            detail=delivery["reason"],
        )

    return {
        "city": delivery["city"],
        "available": True,
        "delivery_price": delivery["delivery_price"],
    }