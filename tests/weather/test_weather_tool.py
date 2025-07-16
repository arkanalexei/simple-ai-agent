from unittest.mock import AsyncMock, patch

import pytest

from tools import weather_tool


@pytest.mark.asyncio
@patch("tools.weather_tool.get_weather", new_callable=AsyncMock)
@patch("tools.weather_tool.extract_city", new_callable=AsyncMock)
async def test_weather_tool_success(mock_extract_city, mock_get_weather):
    mock_extract_city.return_value = "Tokyo"
    mock_get_weather.return_value = "It's sunny and 30°C in Tokyo."

    result = await weather_tool.run("What's the weather in Tokyo?")
    assert "Tokyo" in result
    assert "sunny" in result
    mock_extract_city.assert_called_once()
    mock_get_weather.assert_called_once_with("Tokyo")


@pytest.mark.asyncio
@patch("tools.weather_tool.get_weather", new_callable=AsyncMock)
@patch("tools.weather_tool.extract_city", new_callable=AsyncMock)
async def test_weather_tool_failure(mock_extract_city, mock_get_weather):
    mock_extract_city.return_value = "Moon"
    mock_get_weather.side_effect = Exception("City not found")

    result = await weather_tool.run("Weather on the moon?")
    assert "Error fetching weather" in result
    assert "Moon" in result
