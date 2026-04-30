from sqlalchemy.ext.asyncio import AsyncSession

from app.models.table import Table
from app.repositories.table_repository import TableRepository
from app.utils.security import hash_password
from app.utils.exceptions import DuplicateError, NotFoundError


class TableService:
    def __init__(self, db: AsyncSession):
        self.table_repo = TableRepository(db)

    async def create_table(self, store_id: int, table_number: int, password: str) -> Table:
        existing = await self.table_repo.get_by_store_and_number(store_id, table_number)
        if existing:
            raise DuplicateError("테이블 번호")
        password_hash = hash_password(password)
        return await self.table_repo.create(store_id=store_id, table_number=table_number, password_hash=password_hash)

    async def get_tables(self, store_id: int) -> list[Table]:
        return await self.table_repo.get_all_by_store(store_id)

    async def get_table(self, table_id: int) -> Table:
        table = await self.table_repo.get_by_id(table_id)
        if not table:
            raise NotFoundError("테이블")
        return table
