from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu_item import MenuItem


class MenuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_store(
        self, store_id: int, include_inactive: bool = False
    ) -> list[MenuItem]:
        query = select(MenuItem).where(MenuItem.store_id == store_id)
        if not include_inactive:
            query = query.where(MenuItem.is_active == True)
        query = query.order_by(MenuItem.category_id, MenuItem.display_order, MenuItem.id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_category(
        self, store_id: int, category_id: int, active_only: bool = True
    ) -> list[MenuItem]:
        query = select(MenuItem).where(
            and_(MenuItem.store_id == store_id, MenuItem.category_id == category_id)
        )
        if active_only:
            query = query.where(MenuItem.is_active == True)
        query = query.order_by(MenuItem.display_order, MenuItem.id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, store_id: int, menu_item_id: int) -> MenuItem | None:
        result = await self.db.execute(
            select(MenuItem).where(
                and_(MenuItem.id == menu_item_id, MenuItem.store_id == store_id)
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        store_id: int,
        category_id: int,
        name: str,
        price: int,
        description: str | None = None,
        image_url: str | None = None,
        display_order: int = 0,
    ) -> MenuItem:
        menu_item = MenuItem(
            store_id=store_id,
            category_id=category_id,
            name=name,
            price=price,
            description=description,
            image_url=image_url,
            display_order=display_order,
        )
        self.db.add(menu_item)
        await self.db.flush()
        return menu_item

    async def update(self, menu_item: MenuItem) -> MenuItem:
        await self.db.flush()
        return menu_item

    async def soft_delete(self, menu_item: MenuItem) -> None:
        menu_item.is_active = False
        await self.db.flush()

    async def update_display_orders(
        self, store_id: int, items: list[dict]
    ) -> None:
        for item in items:
            menu_item = await self.get_by_id(store_id, item["menu_item_id"])
            if menu_item:
                menu_item.display_order = item["display_order"]
        await self.db.flush()

    async def get_max_display_order(self, store_id: int, category_id: int) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.max(MenuItem.display_order), 0)).where(
                and_(
                    MenuItem.store_id == store_id,
                    MenuItem.category_id == category_id,
                )
            )
        )
        return result.scalar_one()
