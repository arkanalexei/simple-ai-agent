from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import httpx
import os

# TODO: Refactor the math tool for modularity

load_dotenv()

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherQuery(BaseModel):
  city: str

parser = PydanticOutputParser(pydantic_object=WeatherQuery)

prompt = PromptTemplate.from_template("""
Extract the city name from the user's query

Query: {query}
{format_instructions}
""").partial(format_instructions=parser.get_format_instructions())

model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

chain = prompt | model | parser

def extract_city(query: str) -> str:
  """
  Extract the city name from the query using the LLM.
  """
  try:
    result = chain.invoke({"query": query})
    return result.city
  except Exception:
    return "San Francisco"

async def run(query: str) -> str:
  """
  Run the weather tool to get the weather for the specified city.
  """
  city = extract_city(query)
  params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
  }
  
  try:
    async with httpx.AsyncClient() as client:
      
      response = await client.get(BASE_URL, params=params, timeout=10)
      response.raise_for_status()
      data = response.json()
      temp = data["main"]["temp"]
      weather = data["weather"][0]["description"]
      return f"It's {weather} and {temp}°C in {city}."
  except Exception as e:
    return f"Error fetching weather data for {city}: {str(e)}"
