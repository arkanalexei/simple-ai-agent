from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

from utils.llm import get_llm
from utils.logging import get_logger

logger = get_logger("weather_parser")


class WeatherQuery(BaseModel):  # type: ignore[misc]
    city: str


parser = PydanticOutputParser(pydantic_object=WeatherQuery)

prompt = PromptTemplate.from_template(
    """
Extract the city name from the user's query

Query: {query}
{format_instructions}
"""
).partial(format_instructions=parser.get_format_instructions())


async def extract_city(query: str) -> str:
    """
    Extract the city name from the query using the LLM.
    """
    try:
        llm = get_llm()
        chain = prompt | llm | parser
        result: WeatherQuery = await chain.ainvoke({"query": query})

        if not result.city:
            logger.error(f"No city extracted from query: {query}")
            return "San Francisco"

        return result.city
    except Exception as e:
        logger.error(f"Failed to extract city from query '{query}': {e}")
        return "San Francisco"  # Default city if extraction fails
