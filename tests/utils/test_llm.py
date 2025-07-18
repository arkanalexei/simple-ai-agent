from unittest.mock import MagicMock, patch

from utils.llm import get_llm


@patch("utils.llm.ChatOpenAI")
def test_get_llm_default_params(mock_chat_openai: MagicMock) -> None:
    get_llm()
    mock_chat_openai.assert_called_once_with(model="gpt-4.1-nano", temperature=0)


@patch("utils.llm.ChatOpenAI")
def test_get_llm_custom_params(mock_chat_openai: MagicMock) -> None:
    get_llm(model="gpt-5", temperature=0.7)
    mock_chat_openai.assert_called_once_with(model="gpt-5", temperature=0.7)
