"""Table request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class TableCreateRequest(BaseModel):
    """Table creation request."""

    table_number: int = Field(..., gt=0)
    password: str = Field(..., min_length=4)


class TableResponse(BaseModel):
    """Table response."""

    id: int
    store_id: int
    table_number: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TableListResponse(BaseModel):
    """Table list response."""

    tables: list[TableResponse]
    total: int
