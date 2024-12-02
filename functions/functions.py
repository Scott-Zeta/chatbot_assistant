import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city):
    url = "https://api.weatherbit.io/v2.0/current"
    key = os.getenv("WEATHER_API_KEY")
    params = {
        "city": city,
        "key": key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        data = response.json()['data'][0]
        weather = {'description': data['weather']['description'], 'temperature': data['app_temp']}
        return f"The weather is {weather['description']} and {weather['temperature']}°C" 
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None