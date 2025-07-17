from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tools import llm_tool
from utils.errors import ToolError


@pytest.mark.asyncio  # type: ignore[misc]
@patch("tools.llm_tool.get_llm")
async def test_llm_tool_success(mock_get_llm: MagicMock) -> None:
    mock_llm = AsyncMock()
    mock_llm.ainvoke.return_value = SimpleNamespace(content=" Paris ")
    mock_get_llm.return_value = mock_llm

    result = await llm_tool.run("What is the capital of France?")
    assert result == "Paris"


@pytest.mark.asyncio  # type: ignore[misc]
@patch("tools.llm_tool.get_llm")
async def test_llm_tool_failure(mock_get_llm: MagicMock) -> None:
    mock_llm = AsyncMock()
    mock_llm.ainvoke.side_effect = Exception("Timeout")
    mock_get_llm.return_value = mock_llm

    with pytest.raises(ToolError) as exc_info:
        await llm_tool.run("What's 2 + 2?")

    assert "failed to process" in str(exc_info.value).lower()
