from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store
from app.repositories.store_repository import StoreRepository
from app.utils.exceptions import DuplicateError, NotFoundError


class StoreService:
    def __init__(self, db: AsyncSession):
        self.store_repo = StoreRepository(db)

    async def create_store(self, name: str, code: str, address: str | None = None) -> Store:
        existing = await self.store_repo.get_by_code(code)
        if existing:
            raise DuplicateError("매장 식별자")
        return await self.store_repo.create(name=name, code=code, address=address)

    async def get_store(self, store_id: int) -> Store:
        store = await self.store_repo.get_by_id(store_id)
        if not store:
            raise NotFoundError("매장")
        return store

    async def list_stores(self) -> list[Store]:
        return await self.store_repo.get_all()
