from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CategoryCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryResponse(BaseModel):
    id: int
    store_id: int
    name: str
    display_order: int
    created_at: datetime

    class Config:
        from_attributes = True


class MenuItemCreateRequest(BaseModel):
    category_id: int
    name: str = Field(..., min_length=1, max_length=100)
    price: int = Field(..., gt=0)
    description: str | None = Field(None, max_length=1000)
    image_url: str | None = None


class MenuItemUpdateRequest(BaseModel):
    category_id: int | None = None
    name: str | None = Field(None, min_length=1, max_length=100)
    price: int | None = Field(None, gt=0)
    description: str | None = None
    image_url: str | None = None


class MenuItemResponse(BaseModel):
    id: int
    store_id: int
    category_id: int
    name: str
    price: int
    description: str | None
    image_url: str | None
    display_order: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MenuOrderUpdateRequest(BaseModel):
    items: list[dict]  # [{menu_item_id: int, display_order: int}]
