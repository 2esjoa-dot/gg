from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password
from app.utils.exceptions import DuplicateError


class AccountService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register_admin(self, store_id: int, username: str, password: str) -> User:
        existing = await self.user_repo.get_by_credentials(store_id, username)
        if existing:
            raise DuplicateError("사용자명")
        password_hash = hash_password(password)
        return await self.user_repo.create(
            store_id=store_id, username=username, password_hash=password_hash, role=UserRole.STORE_ADMIN
        )
