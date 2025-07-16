import pytest
from unittest.mock import AsyncMock, patch
from utils.errors import ToolError
from tools import llm_tool


@pytest.mark.asyncio
@patch("tools.llm_tool.llm", new_callable=AsyncMock)
async def test_llm_tool_success(mock_llm):
    mock_llm.ainvoke = AsyncMock(return_value=type("LLMResponse", (), {"content": " Paris "})())

    result = await llm_tool.run("What is the capital of France?")
    assert result == "Paris"