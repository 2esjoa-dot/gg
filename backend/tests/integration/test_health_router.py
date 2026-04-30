"""Integration tests for health check endpoint."""

import pytest


class TestHealthRouter:
    """Tests for /health endpoint."""

    @pytest.mark.asyncio
    async def test_health_check_returns_200(self, client):
        """Health check should return 200 with status info."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "database" in data
