import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(location: str):
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "your_api_key_here":
        # Return mock data if key not set
        return {"temperature": 28.0, "humidity": 75, "condition": "Clear", "mock": True}
    
    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Celsius
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["main"],
            "mock": False
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        # fallback to mock
        return {"temperature": 22.0, "humidity": 70, "condition": "Clouds", "mock": True, "error": str(e)}
