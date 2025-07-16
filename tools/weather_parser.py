from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


class WeatherQuery(BaseModel):
  city: str

parser = PydanticOutputParser(pydantic_object=WeatherQuery)

prompt = PromptTemplate.from_template("""
Extract the city name from the user's query

Query: {query}
{format_instructions}
""").partial(format_instructions=parser.get_format_instructions())

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

chain = prompt | llm | parser

async def extract_city(query: str) -> str:
  """
  Extract the city name from the query using the LLM.
  """
  try:
    result = await chain.ainvoke({"query": query})
    return result.city
  except Exception as e:
    print(f"Error extracting city: {e}")
    return "San Francisco"  # Default city if extraction fails