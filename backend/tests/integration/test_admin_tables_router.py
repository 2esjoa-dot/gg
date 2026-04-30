"""Integration tests for admin table management API."""

from datetime import datetime, timedelta, timezone

import pytest

from app.models.session import SessionStatus
from app.repositories.session_repository import SessionRepository
from app.repositories.store_repository import StoreRepository
from app.repositories.table_repository import TableRepository
from app.utils.security import create_access_token, hash_password


class TestAdminTablesRouter:
    """Tests for /api/admin/tables endpoints."""

    @pytest.mark.asyncio
    async def test_create_table(self, client, db_session):
        """Should create a new table. (US-A04)"""
        store_repo = StoreRepository()
        store = await store_repo.create(db_session, name="Table Store", code="tbl-store")
        await db_session.commit()

        token = create_access_token(
            {"user_id": 1, "store_id": store.id, "role": "store_admin"}
        )
        response = await client.post(
            "/api/admin/tables",
            json={"table_number": 1, "password": "pass1234"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["table_number"] == 1

    @pytest.mark.asyncio
    async def test_list_tables(self, client, db_session):
        """Should list all tables for a store. (US-A04)"""
        store_repo = StoreRepository()
        table_repo = TableRepository()
        store = await store_repo.create(db_session, name="List Store", code="list-store")
        await db_session.flush()
        await table_repo.create(
            db_session, store_id=store.id, table_number=1, password_hash=hash_password("p")
        )
        await db_session.commit()

        token = create_access_token(
            {"user_id": 1, "store_id": store.id, "role": "store_admin"}
        )
        response = await client.get(
            "/api/admin/tables", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["total"] >= 1

    @pytest.mark.asyncio
    async def test_complete_table_session(self, client, db_session):
        """Should complete the active session. (US-A06)"""
        store_repo = StoreRepository()
        table_repo = TableRepository()
        session_repo = SessionRepository()

        store = await store_repo.create(db_session, name="Comp Store", code="comp-store")
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
            {"user_id": 1, "store_id": store.id, "role": "store_admin"}
        )
        response = await client.post(
            f"/api/admin/tables/{table.id}/complete",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "이용 완료 처리되었습니다"
