import requests
import os
from dotenv import load_dotenv
import sys

# Load your API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    data = response.json()

    # 5. Extract key info
    city_name = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]

    # 6. Print
    print(f"In {city_name}, it is {temp}\u00B0C with {humidity}% humidity and {description}")

if (len(sys.argv) == 2):
    get_weather(sys.argv[1])
else:
    example = 'python weather_app.py "New York"'
    print(f"Please pass only one argument. Example: {example}")
