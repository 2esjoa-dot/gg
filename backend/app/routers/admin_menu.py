"""관리자 메뉴 관리 API — Unit 2 (개발자 2 담당)"""
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import require_role, get_store_id
from app.schemas.menu import (
    CategoryCreateRequest,
    CategoryResponse,
    MenuItemResponse,
    MenuOrderUpdateRequest,
)
from app.services.menu_service import MenuService

router = APIRouter(
    prefix="/api/admin/menu",
    tags=["Admin - Menu"],
    dependencies=[Depends(require_role("store_admin"))],
)


# --- Categories ---


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    return await service.get_categories(store_id)


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    request: CategoryCreateRequest,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    return await service.create_category(store_id, request.name)


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    request: CategoryCreateRequest,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    return await service.update_category(store_id, category_id, request.name)


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    await service.delete_category(store_id, category_id)


# --- Menu Items ---


@router.get("/items", response_model=list[MenuItemResponse])
async def list_menu_items(
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    return await service.get_menu_items(store_id)


@router.post("/items", response_model=MenuItemResponse, status_code=201)
async def create_menu_item(
    category_id: int = Form(...),
    name: str = Form(..., min_length=1, max_length=100),
    price: int = Form(..., gt=0),
    description: str | None = Form(None, max_length=1000),
    image: UploadFile | None = File(None),
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    return await service.create_menu_item(
        store_id=store_id,
        category_id=category_id,
        name=name,
        price=price,
        description=description,
        image=image,
    )


@router.put("/items/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    category_id: int | None = Form(None),
    name: str | None = Form(None, min_length=1, max_length=100),
    price: int | None = Form(None, gt=0),
    description: str | None = Form(None, max_length=1000),
    image: UploadFile | None = File(None),
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    return await service.update_menu_item(
        store_id=store_id,
        menu_item_id=item_id,
        category_id=category_id,
        name=name,
        price=price,
        description=description,
        image=image,
    )


@router.delete("/items/{item_id}", status_code=204)
async def delete_menu_item(
    item_id: int,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    await service.delete_menu_item(store_id, item_id)


# --- Menu Order ---


@router.put("/items/order")
async def update_menu_order(
    request: MenuOrderUpdateRequest,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    await service.update_menu_order(store_id, request.items)
    return {"message": "메뉴 순서가 변경되었습니다"}


# --- Image Upload ---


@router.post("/upload-image")
async def upload_image(
    image: UploadFile = File(...),
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    service = MenuService(db)
    image_url = await service.file_service.save_file(store_id, image)
    return {"image_url": image_url}
