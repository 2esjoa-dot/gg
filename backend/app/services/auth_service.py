"""Authentication service for admin and tablet login."""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import UserRole
from app.repositories.store_repository import StoreRepository
from app.repositories.table_repository import TableRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AdminLoginRequest, RegisterAdminRequest, TabletLoginRequest, TokenResponse
from app.utils.exceptions import AccountLockedError, AuthenticationError, DuplicateError
from app.utils.security import create_access_token, hash_password, verify_password

logger = logging.getLogger(__name__)


class AuthService:
    """Handles admin and tablet authentication logic."""

    def __init__(self):
        self.store_repo = StoreRepository()
        self.user_repo = UserRepository()
        self.table_repo = TableRepository()

    async def admin_login(self, db: AsyncSession, request: AdminLoginRequest) -> TokenResponse:
        """Authenticate an admin user and return a JWT token."""
        store = await self.store_repo.get_by_code(db, request.store_code)
        if not store:
            raise AuthenticationError()

        user = await self.user_repo.get_by_store_and_username(db, store.id, request.username)
        if not user:
            raise AuthenticationError()

        # Check account lock
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            remaining = int((user.locked_until - datetime.now(timezone.utc)).total_seconds() / 60) + 1
            raise AccountLockedError(remaining_minutes=remaining)

        # Verify password
        if not verify_password(request.password, user.password_hash):
            user.login_attempts += 1
            if user.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                user.locked_until = datetime.now(timezone.utc) + timedelta(
                    minutes=settings.LOCK_DURATION_MINUTES
                )
                logger.warning("Account locked: store=%s user=%s", store.code, user.username)
            await db.commit()
            raise AuthenticationError()

        # Successful login - reset attempts
        user.login_attempts = 0
        user.locked_until = None
        await db.commit()

        expires_in = settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600
        token = create_access_token(
            data={"user_id": user.id, "store_id": store.id, "role": user.role.value}
        )
        return TokenResponse(access_token=token, expires_in=expires_in)

    async def tablet_login(self, db: AsyncSession, request: TabletLoginRequest) -> TokenResponse:
        """Authenticate a tablet device and return a JWT token."""
        store = await self.store_repo.get_by_code(db, request.store_code)
        if not store:
            raise AuthenticationError()

        table = await self.table_repo.get_by_store_and_number(db, store.id, request.table_number)
        if not table:
            raise AuthenticationError()

        if not verify_password(request.password, table.password_hash):
            raise AuthenticationError()

        expires_in = settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600
        token = create_access_token(
            data={"table_id": table.id, "store_id": store.id, "role": "tablet"}
        )
        return TokenResponse(access_token=token, expires_in=expires_in)

    async def register_admin(
        self, db: AsyncSession, store_id: int, request: RegisterAdminRequest
    ) -> dict:
        """Register a new admin account for a store."""
        existing = await self.user_repo.get_by_store_and_username(db, store_id, request.username)
        if existing:
            raise DuplicateError("사용자명")

        role = UserRole(request.role) if request.role in [r.value for r in UserRole] else UserRole.STORE_ADMIN
        user = await self.user_repo.create(
            db,
            store_id=store_id,
            username=request.username,
            password_hash=hash_password(request.password),
            role=role,
        )
        await db.commit()
        return {"id": user.id, "username": user.username, "role": user.role.value}
