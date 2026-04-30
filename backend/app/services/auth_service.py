from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import UserRole
from app.repositories.store_repository import StoreRepository
from app.repositories.user_repository import UserRepository
from app.repositories.table_repository import TableRepository
from app.schemas.auth import TokenResponse
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.exceptions import AuthInvalidError, AuthLockedError, DuplicateError


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.store_repo = StoreRepository(db)
        self.user_repo = UserRepository(db)
        self.table_repo = TableRepository(db)

    async def login_admin(self, store_code: str, username: str, password: str) -> TokenResponse:
        store = await self.store_repo.get_by_code(store_code)
        if not store:
            raise AuthInvalidError()

        user = await self.user_repo.get_by_credentials(store.id, username)
        if not user:
            raise AuthInvalidError()

        # Check lock
        if user.locked_until and user.locked_until > datetime.utcnow():
            minutes = int((user.locked_until - datetime.utcnow()).total_seconds() / 60) + 1
            raise AuthLockedError(minutes)

        # Verify password
        if not verify_password(password, user.password_hash):
            user.login_attempts += 1
            if user.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                from datetime import timedelta
                user.locked_until = datetime.utcnow() + timedelta(minutes=settings.LOCK_DURATION_MINUTES)
            await self.user_repo.update(user)
            raise AuthInvalidError()

        # Success - reset attempts
        user.login_attempts = 0
        user.locked_until = None
        await self.user_repo.update(user)

        token = create_access_token({"user_id": user.id, "store_id": store.id, "role": user.role.value})
        return TokenResponse(access_token=token, expires_in=settings.JWT_EXPIRE_HOURS * 3600)

    async def login_tablet(self, store_code: str, table_number: int, password: str) -> TokenResponse:
        store = await self.store_repo.get_by_code(store_code)
        if not store:
            raise AuthInvalidError()

        table = await self.table_repo.get_by_store_and_number(store.id, table_number)
        if not table:
            raise AuthInvalidError()

        if not verify_password(password, table.password_hash):
            raise AuthInvalidError()

        token = create_access_token({"table_id": table.id, "store_id": store.id, "role": "tablet"})
        return TokenResponse(access_token=token, expires_in=settings.JWT_EXPIRE_HOURS * 3600)
