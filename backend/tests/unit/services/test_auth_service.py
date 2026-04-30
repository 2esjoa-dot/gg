"""Unit tests for AuthService."""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.user import User, UserRole
from app.schemas.auth import AdminLoginRequest, RegisterAdminRequest, TabletLoginRequest
from app.services.auth_service import AuthService
from app.utils.exceptions import AccountLockedError, AuthenticationError, DuplicateError


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    return db


class TestAdminLogin:
    """Tests for admin login flow."""

    @pytest.mark.asyncio
    async def test_login_invalid_store_code(self, auth_service, mock_db):
        """Should raise AuthenticationError for invalid store code."""
        auth_service.store_repo.get_by_code = AsyncMock(return_value=None)
        request = AdminLoginRequest(store_code="invalid", username="admin", password="pass")

        with pytest.raises(AuthenticationError):
            await auth_service.admin_login(mock_db, request)

    @pytest.mark.asyncio
    async def test_login_invalid_username(self, auth_service, mock_db):
        """Should raise AuthenticationError for invalid username."""
        mock_store = MagicMock(id=1)
        auth_service.store_repo.get_by_code = AsyncMock(return_value=mock_store)
        auth_service.user_repo.get_by_store_and_username = AsyncMock(return_value=None)
        request = AdminLoginRequest(store_code="store1", username="nouser", password="pass")

        with pytest.raises(AuthenticationError):
            await auth_service.admin_login(mock_db, request)

    @pytest.mark.asyncio
    async def test_login_locked_account(self, auth_service, mock_db):
        """Should raise AccountLockedError when account is locked."""
        mock_store = MagicMock(id=1)
        mock_user = MagicMock()
        mock_user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=10)
        auth_service.store_repo.get_by_code = AsyncMock(return_value=mock_store)
        auth_service.user_repo.get_by_store_and_username = AsyncMock(return_value=mock_user)
        request = AdminLoginRequest(store_code="store1", username="admin", password="pass")

        with pytest.raises(AccountLockedError):
            await auth_service.admin_login(mock_db, request)

    @pytest.mark.asyncio
    async def test_login_wrong_password_increments_attempts(self, auth_service, mock_db):
        """Should increment login_attempts on wrong password."""
        mock_store = MagicMock(id=1)
        mock_user = MagicMock(locked_until=None, login_attempts=0, password_hash="hash")
        auth_service.store_repo.get_by_code = AsyncMock(return_value=mock_store)
        auth_service.user_repo.get_by_store_and_username = AsyncMock(return_value=mock_user)

        with patch("app.services.auth_service.verify_password", return_value=False):
            request = AdminLoginRequest(store_code="store1", username="admin", password="wrong")
            with pytest.raises(AuthenticationError):
                await auth_service.admin_login(mock_db, request)

        assert mock_user.login_attempts == 1

    @pytest.mark.asyncio
    async def test_login_success_resets_attempts(self, auth_service, mock_db):
        """Should reset login_attempts on successful login."""
        mock_store = MagicMock(id=1, code="store1")
        mock_user = MagicMock(
            id=1, locked_until=None, login_attempts=3,
            password_hash="hash", role=UserRole.STORE_ADMIN
        )
        auth_service.store_repo.get_by_code = AsyncMock(return_value=mock_store)
        auth_service.user_repo.get_by_store_and_username = AsyncMock(return_value=mock_user)

        with patch("app.services.auth_service.verify_password", return_value=True):
            request = AdminLoginRequest(store_code="store1", username="admin", password="correct")
            result = await auth_service.admin_login(mock_db, request)

        assert mock_user.login_attempts == 0
        assert result.access_token is not None
        assert result.token_type == "bearer"


class TestRegisterAdmin:
    """Tests for admin registration."""

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, auth_service, mock_db):
        """Should raise DuplicateError for existing username."""
        auth_service.user_repo.get_by_store_and_username = AsyncMock(return_value=MagicMock())
        request = RegisterAdminRequest(username="existing", password="pass1234")

        with pytest.raises(DuplicateError):
            await auth_service.register_admin(mock_db, store_id=1, request=request)

    @pytest.mark.asyncio
    async def test_register_success(self, auth_service, mock_db):
        """Should create a new admin account."""
        auth_service.user_repo.get_by_store_and_username = AsyncMock(return_value=None)
        mock_user = MagicMock(id=1, username="newadmin", role=UserRole.STORE_ADMIN)
        auth_service.user_repo.create = AsyncMock(return_value=mock_user)
        request = RegisterAdminRequest(username="newadmin", password="pass1234")

        result = await auth_service.register_admin(mock_db, store_id=1, request=request)

        assert result["username"] == "newadmin"
