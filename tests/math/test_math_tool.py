from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import AIMessage
from langgraph.graph.state import CompiledStateGraph

from tools import math_tool
from tools.math_tool import get_chain
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


def test_math_tool_get_chain_builds_graph() -> None:
    chain = get_chain()
    assert isinstance(chain, CompiledStateGraph)


@pytest.mark.asyncio  # type: ignore[misc]
@patch("tools.math_tool.get_llm")
async def test_math_tool_acall(mock_get_llm: MagicMock) -> None:
    mock_llm = MagicMock()

    mock_llm_with_tools = MagicMock()
    mock_llm_with_tools.ainvoke = AsyncMock(return_value=AIMessage(content="intermediate"))
    mock_llm.bind_tools.return_value = mock_llm_with_tools

    mock_llm.ainvoke = AsyncMock(return_value=AIMessage(content="100"))

    mock_get_llm.return_value = mock_llm

    result = await math_tool.run("What is 50 + 50?")
    assert result == "100"
