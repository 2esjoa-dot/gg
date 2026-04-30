"""Customer session router. US-C02."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.session import SessionResponse
from app.services.session_service import SessionService

router = APIRouter()
session_service = SessionService()


@router.get("/current", response_model=SessionResponse | None, summary="현재 세션 조회")
async def get_current_session(
    req: Request = None,
    db: AsyncSession = Depends(get_db),
) -> SessionResponse | None:
    """Get the current active session for the tablet's table. (US-C02)"""
    store_id = req.state.store_id
    table_id = req.state.user.get("table_id")
    return await session_service.get_active_session_for_table(db, store_id, table_id)
