from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.menu_item import MenuItem
from app.repositories.category_repository import CategoryRepository
from app.repositories.menu_repository import MenuRepository
from app.services.file_service import LocalFileService
from app.utils.exceptions import NotFoundError, DuplicateError


class MenuService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.category_repo = CategoryRepository(db)
        self.menu_repo = MenuRepository(db)
        self.file_service = LocalFileService()

    # --- Category ---

    async def create_category(self, store_id: int, name: str) -> Category:
        existing = await self.category_repo.get_by_name(store_id, name)
        if existing:
            raise DuplicateError("카테고리명")
        return await self.category_repo.create(store_id, name)

    async def get_categories(self, store_id: int) -> list[Category]:
        return await self.category_repo.get_by_store(store_id)

    async def update_category(
        self, store_id: int, category_id: int, name: str
    ) -> Category:
        category = await self.category_repo.get_by_id(store_id, category_id)
        if not category:
            raise NotFoundError("카테고리")

        existing = await self.category_repo.get_by_name(store_id, name)
        if existing and existing.id != category_id:
            raise DuplicateError("카테고리명")

        category.name = name
        return await self.category_repo.update(category)

    async def delete_category(self, store_id: int, category_id: int) -> None:
        category = await self.category_repo.get_by_id(store_id, category_id)
        if not category:
            raise NotFoundError("카테고리")

        has_items = await self.category_repo.has_menu_items(store_id, category_id)
        if has_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="메뉴가 존재하는 카테고리는 삭제할 수 없습니다",
            )

        await self.category_repo.delete(category)

    # --- MenuItem ---

    async def create_menu_item(
        self,
        store_id: int,
        category_id: int,
        name: str,
        price: int,
        description: str | None = None,
        image: UploadFile | None = None,
    ) -> MenuItem:
        category = await self.category_repo.get_by_id(store_id, category_id)
        if not category:
            raise NotFoundError("카테고리")

        image_url = None
        if image:
            image_url = await self.file_service.save_file(store_id, image)

        max_order = await self.menu_repo.get_max_display_order(store_id, category_id)

        return await self.menu_repo.create(
            store_id=store_id,
            category_id=category_id,
            name=name,
            price=price,
            description=description,
            image_url=image_url,
            display_order=max_order + 1,
        )

    async def update_menu_item(
        self,
        store_id: int,
        menu_item_id: int,
        category_id: int | None = None,
        name: str | None = None,
        price: int | None = None,
        description: str | None = None,
        image: UploadFile | None = None,
    ) -> MenuItem:
        menu_item = await self.menu_repo.get_by_id(store_id, menu_item_id)
        if not menu_item:
            raise NotFoundError("메뉴")

        if category_id is not None:
            category = await self.category_repo.get_by_id(store_id, category_id)
            if not category:
                raise NotFoundError("카테고리")
            menu_item.category_id = category_id

        if name is not None:
            menu_item.name = name
        if price is not None:
            menu_item.price = price
        if description is not None:
            menu_item.description = description

        if image:
            image_url = await self.file_service.save_file(store_id, image)
            menu_item.image_url = image_url

        return await self.menu_repo.update(menu_item)

    async def delete_menu_item(self, store_id: int, menu_item_id: int) -> None:
        menu_item = await self.menu_repo.get_by_id(store_id, menu_item_id)
        if not menu_item:
            raise NotFoundError("메뉴")
        await self.menu_repo.soft_delete(menu_item)

    async def get_menu_by_store(
        self, store_id: int, active_only: bool = True
    ) -> list[dict]:
        """카테고리별로 그룹핑된 메뉴 목록 반환."""
        categories = await self.category_repo.get_by_store(store_id)
        result = []
        for category in categories:
            items = await self.menu_repo.get_by_category(
                store_id, category.id, active_only=active_only
            )
            result.append({"category": category, "items": items})
        return result

    async def get_menu_items(self, store_id: int) -> list[MenuItem]:
        """관리자용: 비활성 포함 전체 메뉴 목록 반환."""
        return await self.menu_repo.get_by_store(store_id, include_inactive=True)

    async def update_menu_order(
        self, store_id: int, items: list[dict]
    ) -> None:
        await self.menu_repo.update_display_orders(store_id, items)
