from datetime import datetime

from pydantic import BaseModel, Field


class TableCreateRequest(BaseModel):
    table_number: int = Field(..., gt=0)
    password: str = Field(..., min_length=4)


class TableResponse(BaseModel):
    id: int
    store_id: int
    table_number: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TableStatusResponse(BaseModel):
    id: int
    table_number: int
    has_active_session: bool
    session_id: int | None = None
    total_order_amount: int = 0
