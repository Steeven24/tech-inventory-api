from datetime import datetime

from pydantic import BaseModel, Field


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class SaleCreate(BaseModel):
    discount: float = Field(default=0, ge=0)
    items: list[SaleItemCreate] = Field(min_length=1)


class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    line_total: float


class SaleResponse(BaseModel):
    id: int
    user_id: int
    subtotal: float
    discount: float
    total: float
    created_at: datetime
    items: list[SaleItemResponse]
