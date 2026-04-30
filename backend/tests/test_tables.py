import pytest
from httpx import AsyncClient

from app.models.store import Store
from app.utils.security import create_access_token


@pytest.mark.asyncio
async def test_create_table(client: AsyncClient, db_session):
    store = Store(name="테스트매장", code="test-store")
    db_session.add(store)
    await db_session.commit()

    token = create_access_token({"user_id": 1, "store_id": store.id, "role": "store_admin"})

    response = await client.post(
        "/api/admin/tables",
        json={"table_number": 1, "password": "1234"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["table_number"] == 1
    assert data["store_id"] == store.id


@pytest.mark.asyncio
async def test_create_table_duplicate(client: AsyncClient, db_session):
    store = Store(name="테스트매장", code="test-store")
    db_session.add(store)
    await db_session.commit()

    token = create_access_token({"user_id": 1, "store_id": store.id, "role": "store_admin"})

    await client.post(
        "/api/admin/tables",
        json={"table_number": 1, "password": "1234"},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = await client.post(
        "/api/admin/tables",
        json={"table_number": 1, "password": "5678"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 409
