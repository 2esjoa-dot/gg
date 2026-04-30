"""Unit tests for order number generation."""

import re
from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.utils.order_number import generate_order_number


class TestOrderNumberGeneration:
    """Tests for order number format and generation logic."""

    @pytest.mark.asyncio
    async def test_order_number_format(self):
        """Order number should match ORD-YYYYMMDD-NNNN format."""
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 1
        mock_db.execute.return_value = mock_result

        order_number = await generate_order_number(mock_db, store_id=1)

        today_str = date.today().strftime("%Y%m%d")
        assert order_number == f"ORD-{today_str}-0001"

    @pytest.mark.asyncio
    async def test_order_number_sequential(self):
        """Sequential calls should produce incrementing numbers."""
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 42
        mock_db.execute.return_value = mock_result

        order_number = await generate_order_number(mock_db, store_id=1)

        assert order_number.endswith("-0042")

    @pytest.mark.asyncio
    async def test_order_number_regex_pattern(self):
        """Order number should match the expected regex pattern."""
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 5
        mock_db.execute.return_value = mock_result

        order_number = await generate_order_number(mock_db, store_id=1)

        pattern = r"^ORD-\d{8}-\d{4}$"
        assert re.match(pattern, order_number)
