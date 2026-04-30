"""User repository for database operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User entity operations."""

    def __init__(self):
        super().__init__(User)

    async def get_by_store_and_username(
        self, db: AsyncSession, store_id: int, username: str
    ) -> User | None:
        """Find a user by store_id and username."""
        result = await db.execute(
            select(User).where(User.store_id == store_id, User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_store(self, db: AsyncSession, store_id: int) -> list[User]:
        """Get all users for a store."""
        result = await db.execute(
            select(User).where(User.store_id == store_id).order_by(User.created_at.desc())
        )
        return list(result.scalars().all())
