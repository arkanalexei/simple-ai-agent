from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app
from utils.errors import AppError

client = TestClient(app)


@pytest.mark.asyncio  # type: ignore[misc]
async def test_handle_query_math() -> None:
    with patch("main.classify_tool", return_value="math"):
        with patch("main.math_tool.run", new_callable=AsyncMock, return_value="4"):
            response = client.post("/query", json={"query": "2 + 2"})
            assert response.status_code == 200
            data = response.json()
            assert data["tool_used"] == "math"
            assert data["result"] == "4"


@pytest.mark.asyncio  # type: ignore[misc]
async def test_handle_query_weather() -> None:
    with patch("main.classify_tool", return_value="weather"):
        with patch("main.weather_tool.run", new_callable=AsyncMock, return_value="Sunny"):
            response = client.post("/query", json={"query": "What's the weather in Cairo?"})
            assert response.status_code == 200
            data = response.json()
            assert data["tool_used"] == "weather"
            assert data["result"] == "Sunny"


@pytest.mark.asyncio  # type: ignore[misc]
async def test_handle_query_llm() -> None:
    with patch("main.classify_tool", return_value="llm"):
        with patch(
            "main.llm_tool.run",
            new_callable=AsyncMock,
            return_value="Paris is the capital of France",
        ):
            response = client.post("/query", json={"query": "Where is Paris?"})
            assert response.status_code == 200
            data = response.json()
            assert data["tool_used"] == "llm"
            assert data["result"] == "Paris is the capital of France"


@pytest.mark.asyncio  # type: ignore[misc]
async def test_handle_query_app_error() -> None:
    with patch("main.classify_tool", return_value="math"):
        with patch("main.math_tool.run", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = AppError("Test error")
            response = client.post("/query", json={"query": "invalid"})
            assert response.status_code == 200
            data = response.json()
            assert data["tool_used"] == "none"
            assert data["result"] is None
            assert "Test error" in data["error"]


@pytest.mark.asyncio  # type: ignore[misc]
async def test_llm_websocket() -> None:
    with patch("main.get_llm") as mock_get_llm:
        mock_llm = MagicMock()
        mock_chunk = MagicMock()
        mock_chunk.content = "Hello"

        async def mock_astream(*args: Any, **kwargs: Any) -> AsyncGenerator[MagicMock, None]:
            yield mock_chunk

        mock_llm.astream = mock_astream
        mock_get_llm.return_value = mock_llm

        with client.websocket_connect("/ws/llm") as websocket:
            websocket.send_text("Test message")

            while True:
                data = websocket.receive_text()
                if data == "Hello":
                    break

            data = websocket.receive_text()
            assert data == "Stream completed", f"Expected 'Stream completed', got '{data}'"
