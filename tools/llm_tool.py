from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

async def run(query: str) -> str:
  response = await llm.ainvoke(query)
  return response.content.strip()
