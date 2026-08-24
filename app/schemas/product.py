from typing import Any

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=100)
    brand: str | None = None
    description: str | None = None

    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

    specifications: dict[str, Any] = Field(default_factory=dict)

    image_url: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    brand: str | None = None
    description: str | None = None

    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)

    specifications: dict[str, Any] | None = None

    image_url: str | None = None


class ProductResponse(ProductBase):
    id: int

    @property
    def is_available(self) -> bool:
        return self.stock > 0