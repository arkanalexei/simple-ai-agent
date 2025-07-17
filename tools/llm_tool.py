from langchain_core.messages import AIMessage

from utils.errors import ToolError
from utils.llm import get_llm
from utils.logging import get_logger

logger = get_logger("llm_tool")


async def run(query: str) -> str:
    llm = get_llm()

    try:
        response: AIMessage = await llm.ainvoke(query)
        return str(response.content.strip())
    except Exception as e:
        logger.error(f"LLM failed to process query '{query}': {e}")
        raise ToolError(f"LLM failed to process query '{query}': {e}")
