"""Unit tests for UserRepository (requires test database)."""

import pytest

from app.models.user import UserRole
from app.repositories.store_repository import StoreRepository
from app.repositories.user_repository import UserRepository


@pytest.fixture
def user_repo():
    return UserRepository()


@pytest.fixture
def store_repo():
    return StoreRepository()


class TestUserRepository:
    """Tests for UserRepository database operations."""

    @pytest.mark.asyncio
    async def test_create_and_get_by_store_username(self, user_repo, store_repo, db_session):
        """Should create a user and find by store+username."""
        store = await store_repo.create(db_session, name="Store", code="s1")
        await db_session.flush()

        user = await user_repo.create(
            db_session,
            store_id=store.id, username="admin1",
            password_hash="hashed", role=UserRole.STORE_ADMIN,
        )
        await db_session.commit()

        found = await user_repo.get_by_store_and_username(db_session, store.id, "admin1")
        assert found is not None
        assert found.username == "admin1"

    @pytest.mark.asyncio
    async def test_get_by_store_and_username_not_found(self, user_repo, db_session):
        """Should return None for non-existent user."""
        found = await user_repo.get_by_store_and_username(db_session, 999, "nouser")
        assert found is None
