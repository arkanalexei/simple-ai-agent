from tools import weather_tool

def test_dummy_weather():
    result = weather_tool.run("What's the weather in San Francisco?")
    assert result == "It's sunny and 24°C in San Francisco"