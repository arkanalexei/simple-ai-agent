from unittest.mock import AsyncMock, patch

import pytest
from langchain_core.messages import AIMessage

from tools import math_tool
from utils.errors import ToolError


@pytest.mark.asyncio
@patch("tools.math_tool.chain.ainvoke", new_callable=AsyncMock)
async def test_math_tool_success(mock_ainvoke):
    mock_ainvoke.return_value = {"messages": [AIMessage(content="42")]}

    result = await math_tool.run("What is 6 * 7?")
    assert result == "42"


@pytest.mark.asyncio
@patch("tools.math_tool.chain.ainvoke", new_callable=AsyncMock)
async def test_math_tool_failure(mock_ainvoke):
    mock_ainvoke.side_effect = Exception("LLM failed")

    with pytest.raises(ToolError) as exc_info:
        await math_tool.run("What is 0 / 0?")

    assert "Math calculation failed" in str(exc_info.value)
