from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    category: str
    brand: str
    sku: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    brand: str | None = None
    sku: str | None = None
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    brand: str
    sku: str
    price: float
    stock: int