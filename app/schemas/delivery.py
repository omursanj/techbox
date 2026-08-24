from pydantic import BaseModel, Field


class DeliveryBase(BaseModel):
    city: str = Field(..., min_length=1, max_length=100)
    delivery_price: int = Field(..., ge=0)
    is_available: bool = True


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryUpdate(BaseModel):
    city: str | None = None
    delivery_price: int | None = Field(default=None, ge=0)
    is_available: bool | None = None


class DeliveryResponse(DeliveryBase):
    id: int