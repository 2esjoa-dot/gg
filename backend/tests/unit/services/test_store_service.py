"""Unit tests for StoreService."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.schemas.store import StoreCreateRequest
from app.services.store_service import StoreService
from app.utils.exceptions import DuplicateError, NotFoundError


@pytest.fixture
def store_service():
    return StoreService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    return db


class TestCreateStore:
    """Tests for store creation."""

    @pytest.mark.asyncio
    async def test_create_store_duplicate_code(self, store_service, mock_db):
        """Should raise DuplicateError for existing store code."""
        store_service.store_repo.get_by_code = AsyncMock(return_value=MagicMock())
        request = StoreCreateRequest(name="Test", code="existing-code")

        with pytest.raises(DuplicateError):
            await store_service.create_store(mock_db, request)

    @pytest.mark.asyncio
    async def test_create_store_success(self, store_service, mock_db):
        """Should create a new store."""
        store_service.store_repo.get_by_code = AsyncMock(return_value=None)
        mock_store = MagicMock(
            id=1, name="New Store", code="new-store",
            address=None, is_active=True,
            created_at=MagicMock(), updated_at=MagicMock()
        )
        store_service.store_repo.create = AsyncMock(return_value=mock_store)
        request = StoreCreateRequest(name="New Store", code="new-store")

        result = await store_service.create_store(mock_db, request)
        assert result.name == "New Store"


class TestGetStore:
    """Tests for store retrieval."""

    @pytest.mark.asyncio
    async def test_get_store_not_found(self, store_service, mock_db):
        """Should raise NotFoundError for non-existent store."""
        store_service.store_repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(NotFoundError):
            await store_service.get_store(mock_db, store_id=999)

    @pytest.mark.asyncio
    async def test_get_store_success(self, store_service, mock_db):
        """Should return store details."""
        mock_store = MagicMock(
            id=1, name="Store", code="store-1",
            address="Seoul", is_active=True,
            created_at=MagicMock(), updated_at=MagicMock()
        )
        store_service.store_repo.get_by_id = AsyncMock(return_value=mock_store)

        result = await store_service.get_store(mock_db, store_id=1)
        assert result.id == 1
