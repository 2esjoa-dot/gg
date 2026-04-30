from datetime import datetime

from pydantic import BaseModel, Field


class StoreCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9\-]+$")
    address: str | None = Field(None, max_length=200)


class StoreResponse(BaseModel):
    id: int
    name: str
    code: str
    address: str | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
