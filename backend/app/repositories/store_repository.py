"""Store repository for database operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store
from app.repositories.base import BaseRepository


class StoreRepository(BaseRepository[Store]):
    """Repository for Store entity operations."""

    def __init__(self):
        super().__init__(Store)

    async def get_by_code(self, db: AsyncSession, code: str) -> Store | None:
        """Find a store by its unique code."""
        result = await db.execute(select(Store).where(Store.code == code))
        return result.scalar_one_or_none()

    async def get_active_stores(self, db: AsyncSession) -> list[Store]:
        """Get all active stores."""
        result = await db.execute(
            select(Store).where(Store.is_active.is_(True)).order_by(Store.created_at.desc())
        )
        return list(result.scalars().all())
