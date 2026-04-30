"""Integration tests for customer session API."""

from datetime import datetime, timedelta, timezone

import pytest

from app.models.session import SessionStatus
from app.repositories.session_repository import SessionRepository
from app.repositories.store_repository import StoreRepository
from app.repositories.table_repository import TableRepository
from app.utils.security import create_access_token


class TestCustomerSessionRouter:
    """Tests for /api/customer/session endpoints."""

    @pytest.mark.asyncio
    async def test_get_current_session_exists(self, client, db_session):
        """Should return active session. (US-C02)"""
        store_repo = StoreRepository()
        table_repo = TableRepository()
        session_repo = SessionRepository()

        store = await store_repo.create(db_session, name="Sess Store", code="sess-store")
        await db_session.flush()
        table = await table_repo.create(
            db_session, store_id=store.id, table_number=1, password_hash="h"
        )
        await db_session.flush()
        await session_repo.create(
            db_session,
            store_id=store.id, table_id=table.id,
            status=SessionStatus.ACTIVE,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=16),
        )
        await db_session.commit()

        token = create_access_token(
            {"table_id": table.id, "store_id": store.id, "role": "tablet"}
        )
        response = await client.get(
            "/api/customer/session/current",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "active"

    @pytest.mark.asyncio
    async def test_get_current_session_none(self, client, db_session):
        """Should return null when no active session."""
        store_repo = StoreRepository()
        table_repo = TableRepository()

        store = await store_repo.create(db_session, name="No Sess", code="no-sess")
        await db_session.flush()
        table = await table_repo.create(
            db_session, store_id=store.id, table_number=1, password_hash="h"
        )
        await db_session.commit()

        token = create_access_token(
            {"table_id": table.id, "store_id": store.id, "role": "tablet"}
        )
        response = await client.get(
            "/api/customer/session/current",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json() is None
