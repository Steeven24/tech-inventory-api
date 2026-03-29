from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class InventoryMovementCreate(BaseModel):
    product_id: int
    movement_type: Literal["in", "out"]
    quantity: int = Field(gt=0)
    note: str | None = None


class InventoryMovementResponse(BaseModel):
    id: int
    product_id: int
    movement_type: str
    quantity: int
    note: str | None
    created_at: datetime