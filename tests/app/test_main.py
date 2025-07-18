from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.asyncio  # type: ignore[misc]
async def test_handle_query_mocked() -> None:
    with patch("main.classify_tool", return_value="math"):
        with patch("main.math_tool.run", new_callable=AsyncMock, return_value="4"):
            response = client.post("/query", json={"query": "2 + 2"})
            assert response.status_code == 200
            data = response.json()
            assert data["tool_used"] == "math"
            assert data["result"] == "4"
