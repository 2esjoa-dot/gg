"""
개발자 2 담당: 고객 메뉴 조회 API
TODO: MenuService 구현 후 연동
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import require_role
from app.schemas.menu import CategoryResponse, MenuItemResponse

router = APIRouter(prefix="/api/customer/menu", tags=["Customer - Menu"])


@router.get("/{store_id}/categories", response_model=list[CategoryResponse])
async def get_categories(store_id: int, db: AsyncSession = Depends(get_db)):
    # TODO: 구현
    return []


@router.get("/{store_id}", response_model=list[MenuItemResponse])
async def get_menu(store_id: int, db: AsyncSession = Depends(get_db)):
    # TODO: 카테고리별 활성 메뉴만 반환
    return []
