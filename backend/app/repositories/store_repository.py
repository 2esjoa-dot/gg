from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store


class StoreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str, code: str, address: str | None = None) -> Store:
        store = Store(name=name, code=code, address=address)
        self.db.add(store)
        await self.db.flush()
        return store

    async def get_by_id(self, store_id: int) -> Store | None:
        result = await self.db.execute(select(Store).where(Store.id == store_id))
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Store | None:
        result = await self.db.execute(select(Store).where(Store.code == code))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Store]:
        result = await self.db.execute(select(Store).where(Store.is_active == True))
        return list(result.scalars().all())
