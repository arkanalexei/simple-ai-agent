from tools.weather_parser import extract_city
from tools.weather_api import get_weather

async def run(query: str) -> str:
    city = await extract_city(query)
    print("city", city)
    try:
        return await get_weather(city)
    except Exception as e:
        return f"Error fetching weather for {city}: {str(e)}"
