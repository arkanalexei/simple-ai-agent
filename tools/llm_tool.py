from langchain_openai import ChatOpenAI

from utils.errors import ToolError
from utils.logging import get_logger

logger = get_logger("llm_tool")

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

async def run(query: str) -> str:
  try:
    response = await llm.ainvoke(query)
    return response.content.strip()
  except Exception as e:
    logger.error(f"LLM failed to process query '{query}': {e}")
    raise ToolError(f"LLM failed to process query '{query}': {e}")
