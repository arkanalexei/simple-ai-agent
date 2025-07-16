from tools.weather_parser import extract_city
from tools.weather_api import get_weather
from utils.logging import get_logger

logger = get_logger("weather_tool")

async def run(query: str) -> str:
    city = await extract_city(query)
    logger.info(f"Extracted city: {city}")
    try:
      return await get_weather(city)
    except Exception as e:
      logger.error(f"Failed to get weather for city '{city}': {e}")
      return f"Error fetching weather for {city}"
