"""Base repository with common CRUD operations."""

from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic base repository providing common database operations."""

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, record_id: int) -> ModelType | None:
        """Get a single record by primary key."""
        result = await db.execute(select(self.model).where(self.model.id == record_id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, **filters: Any) -> list[ModelType]:
        """Get all records matching the given filters."""
        query = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count(self, db: AsyncSession, **filters: Any) -> int:
        """Count records matching the given filters."""
        query = select(func.count(self.model.id))
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
        result = await db.execute(query)
        return result.scalar_one()

    async def create(self, db: AsyncSession, **kwargs: Any) -> ModelType:
        """Create a new record."""
        instance = self.model(**kwargs)
        db.add(instance)
        await db.flush()
        await db.refresh(instance)
        return instance

    async def update(self, db: AsyncSession, instance: ModelType, **kwargs: Any) -> ModelType:
        """Update an existing record."""
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        await db.flush()
        await db.refresh(instance)
        return instance

    async def delete(self, db: AsyncSession, instance: ModelType) -> None:
        """Delete a record."""
        await db.delete(instance)
        await db.flush()
