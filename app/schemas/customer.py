from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    phone: str = Field(..., min_length=5, max_length=30)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    phone: str | None = Field(default=None, min_length=5, max_length=30)


class CustomerResponse(CustomerBase):
    id: int