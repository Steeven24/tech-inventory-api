from pydantic import BaseModel, EmailStr
from typing import Literal


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["admin", "seller", "warehouse"] = "seller"


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: Literal["admin", "seller", "warehouse"] | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str