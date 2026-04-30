"""Integration tests for customer (tablet) authentication API."""

import pytest

from app.repositories.store_repository import StoreRepository
from app.repositories.table_repository import TableRepository
from app.utils.security import hash_password


class TestCustomerAuthRouter:
    """Tests for /api/customer/auth endpoints."""

    @pytest.mark.asyncio
    async def test_tablet_login_success(self, client, db_session):
        """Should return JWT token on valid tablet login. (US-C01)"""
        store_repo = StoreRepository()
        table_repo = TableRepository()
        store = await store_repo.create(db_session, name="Tablet Store", code="tablet-store")
        await db_session.flush()
        await table_repo.create(
            db_session,
            store_id=store.id, table_number=1,
            password_hash=hash_password("tabletpass"),
        )
        await db_session.commit()

        response = await client.post(
            "/api/customer/auth/login",
            json={"store_code": "tablet-store", "table_number": 1, "password": "tabletpass"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    @pytest.mark.asyncio
    async def test_tablet_login_wrong_password(self, client, db_session):
        """Should return 401 on wrong tablet password."""
        store_repo = StoreRepository()
        table_repo = TableRepository()
        store = await store_repo.create(db_session, name="Tablet Store 2", code="tablet-store-2")
        await db_session.flush()
        await table_repo.create(
            db_session,
            store_id=store.id, table_number=1,
            password_hash=hash_password("correct"),
        )
        await db_session.commit()

        response = await client.post(
            "/api/customer/auth/login",
            json={"store_code": "tablet-store-2", "table_number": 1, "password": "wrong"},
        )
        assert response.status_code == 401
