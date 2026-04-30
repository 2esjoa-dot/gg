from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, store_id: int, username: str, password_hash: str, role: str) -> User:
        user = User(store_id=store_id, username=username, password_hash=password_hash, role=role)
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_credentials(self, store_id: int, username: str) -> User | None:
        result = await self.db.execute(
            select(User).where(and_(User.store_id == store_id, User.username == username))
        )
        return result.scalar_one_or_none()

    async def update(self, user: User) -> User:
        await self.db.flush()
        return user
