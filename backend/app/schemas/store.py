"""Store request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class StoreCreateRequest(BaseModel):
    """Store creation request."""

    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9\-]+$")
    address: str | None = Field(None, max_length=200)


class StoreResponse(BaseModel):
    """Store response."""

    id: int
    name: str
    code: str
    address: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StoreListResponse(BaseModel):
    """Store list response."""

    stores: list[StoreResponse]
    total: int
