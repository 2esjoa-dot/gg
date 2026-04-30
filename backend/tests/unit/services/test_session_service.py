"""Unit tests for SessionService."""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.session import SessionStatus
from app.services.session_service import SessionService
from app.utils.exceptions import NoActiveSessionError, NotFoundError


@pytest.fixture
def session_service():
    return SessionService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    db.flush = AsyncMock()
    return db


class TestGetOrCreateSession:
    """Tests for session creation and retrieval."""

    @pytest.mark.asyncio
    async def test_returns_existing_active_session(self, session_service, mock_db):
        """Should return existing active session if found."""
        mock_session = MagicMock(
            id=1, store_id=1, table_id=1, status="active",
            started_at=MagicMock(), completed_at=None,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=10)
        )
        session_service.session_repo.get_active_session = AsyncMock(return_value=mock_session)

        result = await session_service.get_or_create_session(mock_db, store_id=1, table_id=1)
        assert result.id == 1

    @pytest.mark.asyncio
    async def test_creates_new_session_when_none_exists(self, session_service, mock_db):
        """Should create a new session when no active session exists."""
        session_service.session_repo.get_active_session = AsyncMock(return_value=None)
        session_service.session_repo.get_expired_active_session = AsyncMock(return_value=None)
        mock_new = MagicMock(
            id=2, store_id=1, table_id=1, status="active",
            started_at=MagicMock(), completed_at=None,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=16)
        )
        session_service.session_repo.create = AsyncMock(return_value=mock_new)

        result = await session_service.get_or_create_session(mock_db, store_id=1, table_id=1)
        assert result.id == 2

    @pytest.mark.asyncio
    async def test_closes_expired_session_and_creates_new(self, session_service, mock_db):
        """Should close expired session and create a new one."""
        expired = MagicMock(
            id=1, status=SessionStatus.ACTIVE,
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1)
        )
        session_service.session_repo.get_active_session = AsyncMock(return_value=None)
        session_service.session_repo.get_expired_active_session = AsyncMock(return_value=expired)
        mock_new = MagicMock(
            id=3, store_id=1, table_id=1, status="active",
            started_at=MagicMock(), completed_at=None,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=16)
        )
        session_service.session_repo.create = AsyncMock(return_value=mock_new)

        result = await session_service.get_or_create_session(mock_db, store_id=1, table_id=1)
        assert expired.status == SessionStatus.COMPLETED
        assert result.id == 3


class TestCompleteSession:
    """Tests for session completion (이용 완료)."""

    @pytest.mark.asyncio
    async def test_complete_session_table_not_found(self, session_service, mock_db):
        """Should raise NotFoundError when table doesn't exist."""
        session_service.table_repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(NotFoundError):
            await session_service.complete_session(mock_db, store_id=1, table_id=999)

    @pytest.mark.asyncio
    async def test_complete_session_no_active(self, session_service, mock_db):
        """Should raise NoActiveSessionError when no active session."""
        mock_table = MagicMock(store_id=1)
        session_service.table_repo.get_by_id = AsyncMock(return_value=mock_table)
        session_service.session_repo.get_active_session = AsyncMock(return_value=None)

        with pytest.raises(NoActiveSessionError):
            await session_service.complete_session(mock_db, store_id=1, table_id=1)

    @pytest.mark.asyncio
    async def test_complete_session_success(self, session_service, mock_db):
        """Should complete the active session."""
        mock_table = MagicMock(store_id=1)
        mock_session = MagicMock(id=1, status=SessionStatus.ACTIVE)
        session_service.table_repo.get_by_id = AsyncMock(return_value=mock_table)
        session_service.session_repo.get_active_session = AsyncMock(return_value=mock_session)

        result = await session_service.complete_session(mock_db, store_id=1, table_id=1)

        assert mock_session.status == SessionStatus.COMPLETED
        assert result.session_id == 1
