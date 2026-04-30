"""HQ (headquarters) router for store management. US-H01, US-H02."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.store import StoreCreateRequest, StoreListResponse, StoreResponse
from app.services.store_service import StoreService

router = APIRouter()
store_service = StoreService()


@router.post("/stores", response_model=StoreResponse, status_code=201, summary="매장 등록")
async def create_store(
    request: StoreCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> StoreResponse:
    """Register a new store. (US-H01)"""
    return await store_service.create_store(db, request)


@router.get("/stores", response_model=StoreListResponse, summary="매장 목록 조회")
async def list_stores(
    db: AsyncSession = Depends(get_db),
) -> StoreListResponse:
    """List all active stores. (US-H02)"""
    return await store_service.list_stores(db)


@router.get("/stores/{store_id}", response_model=StoreResponse, summary="매장 상세 조회")
async def get_store(
    store_id: int,
    db: AsyncSession = Depends(get_db),
) -> StoreResponse:
    """Get store details by ID. (US-H02)"""
    return await store_service.get_store(db, store_id)
