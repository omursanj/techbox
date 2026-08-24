from datetime import datetime

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=150)
    customer_phone: str = Field(..., min_length=5, max_length=30)
    city: str = Field(..., min_length=1, max_length=100)

    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: int
    subtotal: int


class OrderResponse(BaseModel):
    id: int

    customer_name: str
    customer_phone: str
    city: str

    delivery_price: int
    total: int
    status: str

    created_at: datetime

    items: list[OrderItemResponse]