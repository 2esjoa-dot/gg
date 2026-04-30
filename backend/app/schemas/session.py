from datetime import datetime

from pydantic import BaseModel

from app.models.session import SessionStatus


class SessionResponse(BaseModel):
    id: int
    store_id: int
    table_id: int
    status: SessionStatus
    started_at: datetime
    completed_at: datetime | None
    expires_at: datetime

    class Config:
        from_attributes = True
