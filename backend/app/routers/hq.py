from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import require_role
from app.schemas.store import StoreCreateRequest, StoreResponse
from app.services.store_service import StoreService

router = APIRouter(prefix="/api/hq", tags=["HQ"])


@router.post("/stores", response_model=StoreResponse, dependencies=[Depends(require_role("hq_admin"))])
async def create_store(request: StoreCreateRequest, db: AsyncSession = Depends(get_db)):
    service = StoreService(db)
    store = await service.create_store(name=request.name, code=request.code, address=request.address)
    return store


@router.get("/stores", response_model=list[StoreResponse], dependencies=[Depends(require_role("hq_admin"))])
async def list_stores(db: AsyncSession = Depends(get_db)):
    service = StoreService(db)
    return await service.list_stores()


@router.get("/stores/{store_id}", response_model=StoreResponse, dependencies=[Depends(require_role("hq_admin"))])
async def get_store(store_id: int, db: AsyncSession = Depends(get_db)):
    service = StoreService(db)
    return await service.get_store(store_id)
