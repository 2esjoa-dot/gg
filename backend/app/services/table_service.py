"""Table management service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.table_repository import TableRepository
from app.schemas.table import TableCreateRequest, TableListResponse, TableResponse
from app.utils.exceptions import DuplicateError, NotFoundError
from app.utils.security import hash_password


class TableService:
    """Handles table CRUD operations."""

    def __init__(self):
        self.table_repo = TableRepository()

    async def create_table(
        self, db: AsyncSession, store_id: int, request: TableCreateRequest
    ) -> TableResponse:
        """Create a new table for a store."""
        existing = await self.table_repo.get_by_store_and_number(db, store_id, request.table_number)
        if existing:
            raise DuplicateError("테이블 번호")

        table = await self.table_repo.create(
            db,
            store_id=store_id,
            table_number=request.table_number,
            password_hash=hash_password(request.password),
        )
        await db.commit()
        return TableResponse.model_validate(table)

    async def get_table(self, db: AsyncSession, store_id: int, table_id: int) -> TableResponse:
        """Get a table by ID with store isolation."""
        table = await self.table_repo.get_by_id(db, table_id)
        if not table or table.store_id != store_id:
            raise NotFoundError("테이블")
        return TableResponse.model_validate(table)

    async def list_tables(self, db: AsyncSession, store_id: int) -> TableListResponse:
        """List all active tables for a store."""
        tables = await self.table_repo.get_by_store(db, store_id)
        return TableListResponse(
            tables=[TableResponse.model_validate(t) for t in tables],
            total=len(tables),
        )
