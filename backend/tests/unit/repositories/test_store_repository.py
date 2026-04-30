"""Unit tests for StoreRepository (requires test database)."""

import pytest
import pytest_asyncio

from app.models.store import Store
from app.repositories.store_repository import StoreRepository


@pytest.fixture
def store_repo():
    return StoreRepository()


class TestStoreRepository:
    """Tests for StoreRepository database operations."""

    @pytest.mark.asyncio
    async def test_create_and_get_by_id(self, store_repo, db_session):
        """Should create a store and retrieve it by ID."""
        store = await store_repo.create(db_session, name="Test Store", code="test-001")
        await db_session.commit()

        found = await store_repo.get_by_id(db_session, store.id)
        assert found is not None
        assert found.name == "Test Store"
        assert found.code == "test-001"

    @pytest.mark.asyncio
    async def test_get_by_code(self, store_repo, db_session):
        """Should find a store by its unique code."""
        await store_repo.create(db_session, name="Code Store", code="code-store")
        await db_session.commit()

        found = await store_repo.get_by_code(db_session, "code-store")
        assert found is not None
        assert found.name == "Code Store"

    @pytest.mark.asyncio
    async def test_get_by_code_not_found(self, store_repo, db_session):
        """Should return None for non-existent code."""
        found = await store_repo.get_by_code(db_session, "nonexistent")
        assert found is None

    @pytest.mark.asyncio
    async def test_get_active_stores(self, store_repo, db_session):
        """Should return only active stores."""
        await store_repo.create(db_session, name="Active", code="active-1")
        inactive = await store_repo.create(db_session, name="Inactive", code="inactive-1")
        inactive.is_active = False
        await db_session.commit()

        stores = await store_repo.get_active_stores(db_session)
        codes = [s.code for s in stores]
        assert "active-1" in codes
        assert "inactive-1" not in codes
