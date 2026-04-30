import pytest
from httpx import AsyncClient

from app.utils.security import create_access_token


@pytest.mark.asyncio
async def test_create_store(client: AsyncClient):
    token = create_access_token({"user_id": 1, "store_id": 1, "role": "hq_admin"})

    response = await client.post(
        "/api/hq/stores",
        json={"name": "새매장", "code": "new-store", "address": "서울시 강남구"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "새매장"
    assert data["code"] == "new-store"


@pytest.mark.asyncio
async def test_create_store_duplicate(client: AsyncClient):
    token = create_access_token({"user_id": 1, "store_id": 1, "role": "hq_admin"})

    await client.post(
        "/api/hq/stores",
        json={"name": "매장1", "code": "dup-store"},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = await client.post(
        "/api/hq/stores",
        json={"name": "매장2", "code": "dup-store"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 409
