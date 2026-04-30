"""Store management service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store_repository import StoreRepository
from app.schemas.store import StoreCreateRequest, StoreListResponse, StoreResponse
from app.utils.exceptions import DuplicateError, NotFoundError


class StoreService:
    """Handles store CRUD operations."""

    def __init__(self):
        self.store_repo = StoreRepository()

    async def create_store(self, db: AsyncSession, request: StoreCreateRequest) -> StoreResponse:
        """Create a new store."""
        existing = await self.store_repo.get_by_code(db, request.code)
        if existing:
            raise DuplicateError("매장 코드")

        store = await self.store_repo.create(
            db, name=request.name, code=request.code, address=request.address
        )
        await db.commit()
        return StoreResponse.model_validate(store)

    async def get_store(self, db: AsyncSession, store_id: int) -> StoreResponse:
        """Get a store by ID."""
        store = await self.store_repo.get_by_id(db, store_id)
        if not store:
            raise NotFoundError("매장")
        return StoreResponse.model_validate(store)

    async def list_stores(self, db: AsyncSession) -> StoreListResponse:
        """List all active stores."""
        stores = await self.store_repo.get_active_stores(db)
        return StoreListResponse(
            stores=[StoreResponse.model_validate(s) for s in stores],
            total=len(stores),
        )
