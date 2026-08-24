from fastapi import APIRouter, HTTPException, Query

from app.schemas.product import ProductResponse
from app.services.product_service import (
    get_product,
    find_products,
    list_products,
    list_products_by_category,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    "",
    response_model=list[ProductResponse],
    summary="Получить все товары",
)
def get_products():
    return list_products()


@router.get(
    "/search",
    response_model=list[ProductResponse],
    summary="Поиск товаров",
)
def search_products(
    query: str | None = Query(
        default=None,
        min_length=1,
        description="Название, бренд или описание товара",
    ),
    category: str | None = Query(
        default=None,
        description="Категория товара",
    ),
    min_price: int | None = Query(
        default=None,
        ge=0,
        description="Минимальная цена",
    ),
    max_price: int | None = Query(
        default=None,
        ge=0,
        description="Максимальная цена",
    ),
    in_stock_only: bool = Query(
        default=True,
        description="Показывать только товары в наличии",
    ),
):
    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=400,
            detail="min_price не может быть больше max_price.",
        )

    return find_products(
        query=query,
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only,
    )


@router.get(
    "/category/{category}",
    response_model=list[ProductResponse],
    summary="Получить товары по категории",
)
def get_products_by_category(
    category: str,
):
    products = list_products_by_category(category)

    return products


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Получить товар по ID",
)
def get_product_by_id(
    product_id: int,
):
    if product_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID товара должен быть больше нуля.",
        )

    product = get_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Товар не найден.",
        )

    return product