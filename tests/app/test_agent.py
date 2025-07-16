from agent import classify_tool
from unittest.mock import patch
from types import SimpleNamespace


@patch("agent.get_chain")
def test_mock_classify_tool_math(mock_chain_func):
  mock_chain = mock_chain_func.return_value
  mock_chain.invoke.return_value = SimpleNamespace(content="math")
  assert classify_tool("What is 2 + 2?") == "math"
    
@patch("agent.get_chain")
def test_mock_classify_tool_weather(mock_chain_func):
  mock_chain = mock_chain_func.return_value
  mock_chain.invoke.return_value = SimpleNamespace(content="weather")
  assert classify_tool("What's the weather in San Francisco?") == "weather"

@patch("agent.get_chain")
def test_mock_classify_tool_llm(mock_chain_func):
  mock_chain = mock_chain_func.return_value
  mock_chain.invoke.return_value = SimpleNamespace(content="llm")
  assert classify_tool("What is the capital of France?") == "llm"