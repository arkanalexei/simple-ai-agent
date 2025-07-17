from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import AIMessage

from tools import math_tool
from utils.errors import ToolError


@pytest.mark.asyncio  # type: ignore[misc]
@patch("tools.math_tool.get_chain")
async def test_math_tool_success(mock_get_chain: MagicMock) -> None:
    mock_chain = AsyncMock()
    mock_chain.ainvoke.return_value = {"messages": [AIMessage(content="42")]}
    mock_get_chain.return_value = mock_chain

    result = await math_tool.run("What is 6 * 7?")
    assert result == "42"


@pytest.mark.asyncio  # type: ignore[misc]
@patch("tools.math_tool.get_chain")
async def test_math_tool_failure(mock_get_chain: MagicMock) -> None:
    mock_chain = AsyncMock()
    mock_chain.ainvoke.side_effect = Exception("LLM failed")
    mock_get_chain.return_value = mock_chain

    with pytest.raises(ToolError) as exc_info:
        await math_tool.run("What is 0 / 0?")

    assert "Math calculation failed" in str(exc_info.value)
