from unittest.mock import AsyncMock, patch

import pytest

from tools import weather_parser


class FakeWeatherResult:
    city = "Berlin"
    
class EmptyWeatherResult:
    city = None


@pytest.mark.asyncio
@patch("langchain_core.runnables.base.RunnableSequence.ainvoke", new_callable=AsyncMock)
async def test_extract_city_success(mock_ainvoke):
    mock_ainvoke.return_value = FakeWeatherResult()
    result = await weather_parser.extract_city("Weather in Berlin?")
    
    assert result == "Berlin"
    mock_ainvoke.assert_awaited_once_with({"query": "Weather in Berlin?"})
    
@pytest.mark.asyncio
@patch("langchain_core.runnables.base.RunnableSequence.ainvoke", new_callable=AsyncMock)
@patch("tools.weather_parser.logger")
async def test_extract_city_fallback_on_exception(mock_logger, mock_ainvoke):
    mock_ainvoke.side_effect = RuntimeError("LLM crashed")
    result = await weather_parser.extract_city("What's the weather in Atlantis?")
    
    assert result == "San Francisco"

    mock_logger.error.assert_called_once()
    logged_msg = mock_logger.error.call_args[0][0]
    assert "Failed to extract city" in logged_msg
    assert "Atlantis" in logged_msg
    
    
@pytest.mark.asyncio
@patch("langchain_core.runnables.base.RunnableSequence.ainvoke", new_callable=AsyncMock)
@patch("tools.weather_parser.logger")
async def test_extract_city_no_city_given(mock_logger, mock_ainvoke):
    mock_ainvoke.return_value = EmptyWeatherResult()
    result = await weather_parser.extract_city("What's the weather?")
    
    assert result == "San Francisco"

    mock_logger.error.assert_called_once()
    logged_msg = mock_logger.error.call_args[0][0]
    assert "No city extracted" in logged_msg