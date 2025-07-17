from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tools import weather_parser


class FakeWeatherResult:
    city = "Berlin"


class EmptyWeatherResult:
    city = None


@pytest.fixture  # type: ignore[misc]
def mock_weather_parser_chain() -> Any:
    """Fixture that mocks the entire LangChain pipeline."""
    with (
        patch("tools.weather_parser.get_llm") as mock_get_llm,
        patch("tools.weather_parser.parser") as mock_parser,
        patch("tools.weather_parser.prompt") as mock_prompt,
    ):
        mock_chain = AsyncMock()
        mock_prompt.__or__.return_value.__or__.return_value = mock_chain

        yield {
            "mock_chain": mock_chain,
            "mock_get_llm": mock_get_llm,
            "mock_parser": mock_parser,
            "mock_prompt": mock_prompt,
        }


@pytest.mark.asyncio  # type: ignore[misc]
async def test_extract_city_success(mock_weather_parser_chain: dict[str, AsyncMock]) -> None:
    mock_weather_parser_chain["mock_chain"].ainvoke.return_value = FakeWeatherResult()

    result = await weather_parser.extract_city("Weather in Berlin?")
    assert result == "Berlin"
    mock_weather_parser_chain["mock_chain"].ainvoke.assert_awaited_once_with(
        {"query": "Weather in Berlin?"}
    )


@pytest.mark.asyncio  # type: ignore[misc]
@patch("tools.weather_parser.logger")
async def test_extract_city_fallback_on_exception(
    mock_logger: MagicMock, mock_weather_parser_chain: dict[str, AsyncMock]
) -> None:
    mock_weather_parser_chain["mock_chain"].ainvoke.side_effect = RuntimeError("LLM crashed")

    result = await weather_parser.extract_city("What's the weather in Atlantis?")
    assert result == "San Francisco"
    mock_logger.error.assert_called_once()


@pytest.mark.asyncio  # type: ignore[misc]
@patch("tools.weather_parser.logger")
async def test_extract_city_no_city_given(
    mock_logger: MagicMock, mock_weather_parser_chain: dict[str, AsyncMock]
) -> None:
    mock_weather_parser_chain["mock_chain"].ainvoke.return_value = EmptyWeatherResult()

    result = await weather_parser.extract_city("What's the weather?")
    assert result == "San Francisco"
    mock_logger.error.assert_called_once()
