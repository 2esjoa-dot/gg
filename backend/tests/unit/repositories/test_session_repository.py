"""Unit tests for SessionRepository (requires test database)."""

from datetime import datetime, timedelta, timezone

import pytest

from app.models.session import SessionStatus
from app.repositories.session_repository import SessionRepository
from app.repositories.store_repository import StoreRepository
from app.repositories.table_repository import TableRepository


@pytest.fixture
def session_repo():
    return SessionRepository()


@pytest.fixture
def store_repo():
    return StoreRepository()


@pytest.fixture
def table_repo():
    return TableRepository()


class TestSessionRepository:
    """Tests for SessionRepository database operations."""

    @pytest.mark.asyncio
    async def test_get_active_session(self, session_repo, store_repo, table_repo, db_session):
        """Should find the active session for a table."""
        store = await store_repo.create(db_session, name="Store", code="ss1")
        await db_session.flush()
        table = await table_repo.create(
            db_session, store_id=store.id, table_number=1, password_hash="h"
        )
        await db_session.flush()

        session = await session_repo.create(
            db_session,
            store_id=store.id, table_id=table.id,
            status=SessionStatus.ACTIVE,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=16),
        )
        await db_session.commit()

        found = await session_repo.get_active_session(db_session, store.id, table.id)
        assert found is not None
        assert found.id == session.id

    @pytest.mark.asyncio
    async def test_get_active_session_none(self, session_repo, db_session):
        """Should return None when no active session exists."""
        found = await session_repo.get_active_session(db_session, 999, 999)
        assert found is None

    @pytest.mark.asyncio
    async def test_get_expired_active_session(
        self, session_repo, store_repo, table_repo, db_session
    ):
        """Should find expired but still active sessions."""
        store = await store_repo.create(db_session, name="Store", code="ss2")
        await db_session.flush()
        table = await table_repo.create(
            db_session, store_id=store.id, table_number=1, password_hash="h"
        )
        await db_session.flush()

        await session_repo.create(
            db_session,
            store_id=store.id, table_id=table.id,
            status=SessionStatus.ACTIVE,
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )
        await db_session.commit()

        found = await session_repo.get_expired_active_session(db_session, store.id, table.id)
        assert found is not None
