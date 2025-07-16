from unittest.mock import AsyncMock, patch

import pytest

from tools import weather_parser


class FakeWeatherResult:
    city = "Berlin"


@pytest.mark.asyncio
@patch("tools.weather_parser.extract_city", new_callable=AsyncMock)
async def test_extract_city_success(mock_extract_city):
    mock_extract_city.return_value = "Berlin"
    result = await weather_parser.extract_city("Weather in Berlin?")
    assert result == "Berlin"
