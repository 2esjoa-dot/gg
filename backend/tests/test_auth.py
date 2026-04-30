import pytest
from httpx import AsyncClient

from app.models.store import Store
from app.models.user import User, UserRole
from app.utils.security import hash_password


@pytest.mark.asyncio
async def test_admin_login_success(client: AsyncClient, db_session):
    # Setup
    store = Store(name="테스트매장", code="test-store")
    db_session.add(store)
    await db_session.flush()

    user = User(
        store_id=store.id,
        username="admin1",
        password_hash=hash_password("pass1234"),
        role=UserRole.STORE_ADMIN,
    )
    db_session.add(user)
    await db_session.commit()

    # Act
    response = await client.post("/api/admin/auth/login", json={
        "store_code": "test-store",
        "username": "admin1",
        "password": "pass1234",
    })

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 57600


@pytest.mark.asyncio
async def test_admin_login_invalid_password(client: AsyncClient, db_session):
    store = Store(name="테스트매장", code="test-store")
    db_session.add(store)
    await db_session.flush()

    user = User(
        store_id=store.id,
        username="admin1",
        password_hash=hash_password("pass1234"),
        role=UserRole.STORE_ADMIN,
    )
    db_session.add(user)
    await db_session.commit()

    response = await client.post("/api/admin/auth/login", json={
        "store_code": "test-store",
        "username": "admin1",
        "password": "wrongpass",
    })

    assert response.status_code == 401
