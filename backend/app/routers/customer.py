from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import TabletLoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/customer", tags=["Customer"])


@router.post("/auth/login", response_model=TokenResponse)
async def tablet_login(request: TabletLoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login_tablet(request.store_code, request.table_number, request.password)
