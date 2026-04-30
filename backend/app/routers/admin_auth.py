"""Admin authentication router. US-A01, US-A10."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import AdminLoginRequest, RegisterAdminRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=TokenResponse, summary="관리자 로그인")
async def admin_login(
    request: AdminLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Authenticate admin user and return JWT token. (US-A01)"""
    return await auth_service.admin_login(db, request)


@router.post("/register", status_code=201, summary="관리자 계정 등록")
async def register_admin(
    request: RegisterAdminRequest,
    req: Request = None,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Register a new admin account for the current store. (US-A10)"""
    store_id = req.state.store_id
    return await auth_service.register_admin(db, store_id, request)
