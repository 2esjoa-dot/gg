"""Unit tests for TableService."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.schemas.table import TableCreateRequest
from app.services.table_service import TableService
from app.utils.exceptions import DuplicateError, NotFoundError


@pytest.fixture
def table_service():
    return TableService()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    return db


class TestCreateTable:
    """Tests for table creation."""

    @pytest.mark.asyncio
    async def test_create_table_duplicate_number(self, table_service, mock_db):
        """Should raise DuplicateError for existing table number."""
        table_service.table_repo.get_by_store_and_number = AsyncMock(return_value=MagicMock())
        request = TableCreateRequest(table_number=1, password="pass1234")

        with pytest.raises(DuplicateError):
            await table_service.create_table(mock_db, store_id=1, request=request)

    @pytest.mark.asyncio
    async def test_create_table_success(self, table_service, mock_db):
        """Should create a new table."""
        table_service.table_repo.get_by_store_and_number = AsyncMock(return_value=None)
        mock_table = MagicMock(
            id=1, store_id=1, table_number=5,
            is_active=True, created_at=MagicMock()
        )
        table_service.table_repo.create = AsyncMock(return_value=mock_table)
        request = TableCreateRequest(table_number=5, password="pass1234")

        result = await table_service.create_table(mock_db, store_id=1, request=request)
        assert result.table_number == 5


class TestGetTable:
    """Tests for table retrieval."""

    @pytest.mark.asyncio
    async def test_get_table_not_found(self, table_service, mock_db):
        """Should raise NotFoundError for non-existent table."""
        table_service.table_repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(NotFoundError):
            await table_service.get_table(mock_db, store_id=1, table_id=999)

    @pytest.mark.asyncio
    async def test_get_table_wrong_store(self, table_service, mock_db):
        """Should raise NotFoundError when table belongs to different store."""
        mock_table = MagicMock(store_id=2)
        table_service.table_repo.get_by_id = AsyncMock(return_value=mock_table)

        with pytest.raises(NotFoundError):
            await table_service.get_table(mock_db, store_id=1, table_id=1)
