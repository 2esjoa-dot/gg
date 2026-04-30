from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.menu_item import MenuItem


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_store(self, store_id: int) -> list[Category]:
        result = await self.db.execute(
            select(Category)
            .where(Category.store_id == store_id)
            .order_by(Category.display_order, Category.id)
        )
        return list(result.scalars().all())

    async def get_by_id(self, store_id: int, category_id: int) -> Category | None:
        result = await self.db.execute(
            select(Category).where(
                and_(Category.id == category_id, Category.store_id == store_id)
            )
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, store_id: int, name: str) -> Category | None:
        result = await self.db.execute(
            select(Category).where(
                and_(Category.store_id == store_id, Category.name == name)
            )
        )
        return result.scalar_one_or_none()

    async def create(self, store_id: int, name: str) -> Category:
        max_order = await self.get_max_display_order(store_id)
        category = Category(
            store_id=store_id,
            name=name,
            display_order=max_order + 1,
        )
        self.db.add(category)
        await self.db.flush()
        return category

    async def update(self, category: Category) -> Category:
        await self.db.flush()
        return category

    async def delete(self, category: Category) -> None:
        await self.db.delete(category)
        await self.db.flush()

    async def has_menu_items(self, store_id: int, category_id: int) -> bool:
        result = await self.db.execute(
            select(func.count(MenuItem.id)).where(
                and_(
                    MenuItem.store_id == store_id,
                    MenuItem.category_id == category_id,
                    MenuItem.is_active == True,
                )
            )
        )
        count = result.scalar_one()
        return count > 0

    async def get_max_display_order(self, store_id: int) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.max(Category.display_order), 0)).where(
                Category.store_id == store_id
            )
        )
        return result.scalar_one()
