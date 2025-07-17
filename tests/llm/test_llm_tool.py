from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from tools import llm_tool
from utils.errors import ToolError


@pytest.mark.asyncio
@patch("tools.llm_tool.llm", new_callable=AsyncMock)
async def test_llm_tool_success(mock_llm):
    mock_llm.ainvoke = AsyncMock(return_value=SimpleNamespace(content=" Paris "))

    result = await llm_tool.run("What is the capital of France?")
    assert result == "Paris"


@pytest.mark.asyncio
@patch("tools.llm_tool.llm", new_callable=AsyncMock)
async def test_llm_tool_failure(mock_llm):
    mock_llm.ainvoke = AsyncMock(side_effect=Exception("Timeout"))

    with pytest.raises(ToolError) as exc_info:
        await llm_tool.run("What's 2 + 2?")

    assert "failed to process" in str(exc_info.value).lower()
