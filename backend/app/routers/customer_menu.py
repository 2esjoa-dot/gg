"""고객 메뉴 조회 API — Unit 2 (개발자 2 담당)"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_store_id
from app.schemas.menu import CategoryResponse, MenuItemResponse
from app.services.menu_service import MenuService

router = APIRouter(prefix="/api/customer/menu", tags=["Customer - Menu"])


class CategoryWithItemsResponse(BaseModel):
    category: CategoryResponse
    items: list[MenuItemResponse]


@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    """매장의 카테고리 목록 조회."""
    service = MenuService(db)
    return await service.get_categories(store_id)


@router.get("/", response_model=list[CategoryWithItemsResponse])
async def get_menu(
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    """매장의 전체 메뉴 조회 (카테고리별 그룹핑, 활성 메뉴만)."""
    service = MenuService(db)
    return await service.get_menu_by_store(store_id, active_only=True)
