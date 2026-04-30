"""Integration tests for HQ store management API."""

import pytest

from app.utils.security import create_access_token


@pytest.fixture
def hq_token():
    """Generate a valid HQ admin JWT token."""
    return create_access_token({"user_id": 1, "store_id": 1, "role": "hq_admin"})


class TestHQStoreRouter:
    """Tests for /api/hq/stores endpoints."""

    @pytest.mark.asyncio
    async def test_create_store(self, client, hq_token):
        """Should create a new store. (US-H01)"""
        response = await client.post(
            "/api/hq/stores",
            json={"name": "Test Store", "code": "test-store-1"},
            headers={"Authorization": f"Bearer {hq_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Store"
        assert data["code"] == "test-store-1"

    @pytest.mark.asyncio
    async def test_create_store_duplicate_code(self, client, hq_token):
        """Should return 409 for duplicate store code."""
        payload = {"name": "Store", "code": "dup-code"}
        await client.post("/api/hq/stores", json=payload, headers={"Authorization": f"Bearer {hq_token}"})
        response = await client.post(
            "/api/hq/stores", json=payload, headers={"Authorization": f"Bearer {hq_token}"}
        )
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_list_stores(self, client, hq_token):
        """Should list all active stores. (US-H02)"""
        await client.post(
            "/api/hq/stores",
            json={"name": "S1", "code": "list-s1"},
            headers={"Authorization": f"Bearer {hq_token}"},
        )
        response = await client.get(
            "/api/hq/stores", headers={"Authorization": f"Bearer {hq_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client):
        """Should return 401 without token."""
        response = await client.get("/api/hq/stores")
        assert response.status_code == 401
