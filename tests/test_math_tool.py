import pytest

from tools import math_tool


@pytest.mark.asyncio
async def test_basic_math():
    result = await math_tool.run("2 + 2")
    assert result == "4"

@pytest.mark.asyncio
async def test_valid_expression_with_constants():
  result = await math_tool.run("pi * 2")
  assert result.startswith("6.")  # approx 6.28