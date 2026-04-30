"""Table repository for database operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.table import Table
from app.repositories.base import BaseRepository


class TableRepository(BaseRepository[Table]):
    """Repository for Table entity operations."""

    def __init__(self):
        super().__init__(Table)

    async def get_by_store_and_number(
        self, db: AsyncSession, store_id: int, table_number: int
    ) -> Table | None:
        """Find a table by store_id and table_number."""
        result = await db.execute(
            select(Table).where(Table.store_id == store_id, Table.table_number == table_number)
        )
        return result.scalar_one_or_none()

    async def get_by_store(self, db: AsyncSession, store_id: int) -> list[Table]:
        """Get all tables for a store."""
        result = await db.execute(
            select(Table)
            .where(Table.store_id == store_id, Table.is_active.is_(True))
            .order_by(Table.table_number)
        )
        return list(result.scalars().all())
