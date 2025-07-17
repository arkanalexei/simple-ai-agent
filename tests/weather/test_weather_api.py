from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tools import weather_api
from utils.errors import ToolError


@pytest.mark.asyncio  # type: ignore[misc]
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_get_weather_success(mock_get: AsyncMock) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "main": {"temp": 20},
        "weather": [{"description": "clear sky"}],
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = await weather_api.get_weather("Madrid")
    assert "Madrid" in result
    assert "clear sky" in result


@pytest.mark.asyncio  # type: ignore[misc]
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_get_weather_failure(mock_get: AsyncMock) -> None:
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = Exception("404")
    mock_get.return_value = mock_response

    with pytest.raises(ToolError):
        await weather_api.get_weather("Atlantis")
