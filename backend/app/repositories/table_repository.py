from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.table import Table


class TableRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, store_id: int, table_number: int, password_hash: str) -> Table:
        table = Table(store_id=store_id, table_number=table_number, password_hash=password_hash)
        self.db.add(table)
        await self.db.flush()
        return table

    async def get_by_store_and_number(self, store_id: int, table_number: int) -> Table | None:
        result = await self.db.execute(
            select(Table).where(and_(Table.store_id == store_id, Table.table_number == table_number))
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, table_id: int) -> Table | None:
        result = await self.db.execute(select(Table).where(Table.id == table_id))
        return result.scalar_one_or_none()

    async def get_all_by_store(self, store_id: int) -> list[Table]:
        result = await self.db.execute(
            select(Table).where(and_(Table.store_id == store_id, Table.is_active == True))
        )
        return list(result.scalars().all())
