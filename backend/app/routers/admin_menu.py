"""
개발자 2 담당: 메뉴 관리 API
TODO: MenuService, MenuRepository 구현 후 연동
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import require_role, get_store_id
from app.schemas.menu import (
    CategoryCreateRequest, CategoryResponse,
    MenuItemCreateRequest, MenuItemUpdateRequest, MenuItemResponse,
    MenuOrderUpdateRequest,
)

router = APIRouter(prefix="/api/admin/menu", tags=["Admin - Menu"])


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: 구현
    return []


@router.post("/categories", response_model=CategoryResponse)
async def create_category(
    request: CategoryCreateRequest,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: 구현
    pass


@router.get("/", response_model=list[MenuItemResponse])
async def list_menu_items(
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: 구현
    return []


@router.post("/", response_model=MenuItemResponse)
async def create_menu_item(
    request: MenuItemCreateRequest,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: 구현
    pass
