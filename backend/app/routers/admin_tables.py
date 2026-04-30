"""Admin table management router. US-A04, US-A06."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.session import SessionCompleteResponse
from app.schemas.table import TableCreateRequest, TableListResponse, TableResponse
from app.services.session_service import SessionService
from app.services.table_service import TableService

router = APIRouter()
table_service = TableService()
session_service = SessionService()


@router.post("", response_model=TableResponse, status_code=201, summary="테이블 등록")
async def create_table(
    request: TableCreateRequest,
    req: Request = None,
    db: AsyncSession = Depends(get_db),
) -> TableResponse:
    """Register a new table for the current store. (US-A04)"""
    store_id = req.state.store_id
    return await table_service.create_table(db, store_id, request)


@router.get("", response_model=TableListResponse, summary="테이블 목록 조회")
async def list_tables(
    req: Request = None,
    db: AsyncSession = Depends(get_db),
) -> TableListResponse:
    """List all active tables for the current store. (US-A04)"""
    store_id = req.state.store_id
    return await table_service.list_tables(db, store_id)


@router.post("/{table_id}/complete", response_model=SessionCompleteResponse, summary="이용 완료")
async def complete_table_session(
    table_id: int,
    req: Request = None,
    db: AsyncSession = Depends(get_db),
) -> SessionCompleteResponse:
    """Complete the active session for a table. (US-A06)"""
    store_id = req.state.store_id
    return await session_service.complete_session(db, store_id, table_id)
