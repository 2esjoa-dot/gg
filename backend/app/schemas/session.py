"""Session request/response schemas."""

from datetime import datetime

from pydantic import BaseModel


class SessionResponse(BaseModel):
    """Table session response."""

    id: int
    store_id: int
    table_id: int
    status: str
    started_at: datetime
    completed_at: datetime | None
    expires_at: datetime

    model_config = {"from_attributes": True}


class SessionCompleteResponse(BaseModel):
    """Session completion response."""

    message: str = "이용 완료 처리되었습니다"
    session_id: int
