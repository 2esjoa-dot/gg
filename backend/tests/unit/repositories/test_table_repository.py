"""Unit tests for TableRepository (requires test database)."""

import pytest

from app.repositories.store_repository import StoreRepository
from app.repositories.table_repository import TableRepository


@pytest.fixture
def table_repo():
    return TableRepository()


@pytest.fixture
def store_repo():
    return StoreRepository()


class TestTableRepository:
    """Tests for TableRepository database operations."""

    @pytest.mark.asyncio
    async def test_create_and_get_by_store_number(self, table_repo, store_repo, db_session):
        """Should create a table and find by store+number."""
        store = await store_repo.create(db_session, name="Store", code="ts1")
        await db_session.flush()

        table = await table_repo.create(
            db_session, store_id=store.id, table_number=1, password_hash="hashed"
        )
        await db_session.commit()

        found = await table_repo.get_by_store_and_number(db_session, store.id, 1)
        assert found is not None
        assert found.table_number == 1

    @pytest.mark.asyncio
    async def test_get_by_store(self, table_repo, store_repo, db_session):
        """Should return all active tables for a store."""
        store = await store_repo.create(db_session, name="Store", code="ts2")
        await db_session.flush()

        await table_repo.create(db_session, store_id=store.id, table_number=1, password_hash="h")
        await table_repo.create(db_session, store_id=store.id, table_number=2, password_hash="h")
        await db_session.commit()

        tables = await table_repo.get_by_store(db_session, store.id)
        assert len(tables) == 2
