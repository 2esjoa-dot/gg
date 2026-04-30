from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import require_role, get_store_id
from app.schemas.auth import AdminLoginRequest, RegisterRequest, TokenResponse
from app.schemas.table import TableCreateRequest, TableResponse
from app.schemas.session import SessionResponse
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.table_service import TableService
from app.services.session_service import SessionService

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# --- Auth ---
@router.post("/auth/login", response_model=TokenResponse)
async def admin_login(request: AdminLoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login_admin(request.store_code, request.username, request.password)


@router.post("/auth/register", response_model=dict, dependencies=[Depends(require_role("store_admin"))])
async def register_admin(
    request: RegisterRequest,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = AccountService(db)
    user = await service.register_admin(store_id, request.username, request.password)
    return {"id": user.id, "username": user.username, "message": "계정이 등록되었습니다"}


# --- Tables ---
@router.post("/tables", response_model=TableResponse, dependencies=[Depends(require_role("store_admin"))])
async def create_table(
    request: TableCreateRequest,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = TableService(db)
    return await service.create_table(store_id, request.table_number, request.password)


@router.get("/tables", response_model=list[TableResponse], dependencies=[Depends(require_role("store_admin"))])
async def list_tables(store_id: int = Depends(get_store_id), db: AsyncSession = Depends(get_db)):
    service = TableService(db)
    return await service.get_tables(store_id)


# --- Session (이용 완료) ---
@router.post("/tables/{table_id}/complete", response_model=SessionResponse, dependencies=[Depends(require_role("store_admin"))])
async def complete_table(
    table_id: int,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = SessionService(db)
    return await service.end_session(store_id, table_id)
