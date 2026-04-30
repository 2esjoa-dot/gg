"""Integration tests for admin authentication API."""

import pytest

from app.models.user import UserRole
from app.repositories.store_repository import StoreRepository
from app.repositories.user_repository import UserRepository
from app.utils.security import create_access_token, hash_password


class TestAdminAuthRouter:
    """Tests for /api/admin/auth endpoints."""

    @pytest.mark.asyncio
    async def test_admin_login_success(self, client, db_session):
        """Should return JWT token on valid login. (US-A01)"""
        store_repo = StoreRepository()
        user_repo = UserRepository()
        store = await store_repo.create(db_session, name="Auth Store", code="auth-store")
        await db_session.flush()
        await user_repo.create(
            db_session,
            store_id=store.id, username="admin",
            password_hash=hash_password("pass1234"),
            role=UserRole.STORE_ADMIN,
        )
        await db_session.commit()

        response = await client.post(
            "/api/admin/auth/login",
            json={"store_code": "auth-store", "username": "admin", "password": "pass1234"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_admin_login_wrong_password(self, client, db_session):
        """Should return 401 on wrong password. (US-A01)"""
        store_repo = StoreRepository()
        user_repo = UserRepository()
        store = await store_repo.create(db_session, name="Auth Store 2", code="auth-store-2")
        await db_session.flush()
        await user_repo.create(
            db_session,
            store_id=store.id, username="admin",
            password_hash=hash_password("correct"),
            role=UserRole.STORE_ADMIN,
        )
        await db_session.commit()

        response = await client.post(
            "/api/admin/auth/login",
            json={"store_code": "auth-store-2", "username": "admin", "password": "wrong"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_register_admin(self, client, db_session):
        """Should register a new admin account. (US-A10)"""
        store_repo = StoreRepository()
        store = await store_repo.create(db_session, name="Reg Store", code="reg-store")
        await db_session.commit()

        token = create_access_token(
            {"user_id": 1, "store_id": store.id, "role": "store_admin"}
        )
        response = await client.post(
            "/api/admin/auth/register",
            json={"username": "newadmin", "password": "pass1234"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newadmin"
