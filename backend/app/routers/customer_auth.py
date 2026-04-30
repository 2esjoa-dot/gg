"""Customer (tablet) authentication router. US-C01."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import TabletLoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=TokenResponse, summary="태블릿 로그인")
async def tablet_login(
    request: TabletLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Authenticate a tablet device and return JWT token. (US-C01)"""
    return await auth_service.tablet_login(db, request)
