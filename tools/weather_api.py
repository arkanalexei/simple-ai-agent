import httpx
import os
from dotenv import load_dotenv

from utils.errors import ToolError
from utils.logging import get_logger

logger = get_logger("weather_api")

load_dotenv()
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather(city: str) -> str:
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
      desc = data["weather"][0]["description"]
      return f"It's {desc} and {temp}°C in {city}."
  except Exception as e:
    logger.error(f"Weather API failed for city '{city}': {e}")
    raise ToolError(f"Weather API failed for city '{city}': {e}")