from langchain_openai import ChatOpenAI

from utils.errors import ToolError

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

async def run(query: str) -> str:
  try:
    response = await llm.ainvoke(query)
    return response.content.strip()
  except Exception as e:
    raise ToolError(f"LLM failed to process query '{query}': {e}")
