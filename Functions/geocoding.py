import requests
import json
import os
from dotenv import load_dotenv


load_dotenv('../Data/.env')
WEATHER_KEY = os.getenv('OPENWEATHER_API_KEY')


def get_coordinates(city, country, key):
    req = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=5&appid={key}')
    data = req.json()
    coordinates = data[0]['lat'], data[0]['lon']
    return coordinates


def get_city(lat, lon, key):
    req = requests.get(f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=5&appid={key}')
    data = req.json()
    return data


if __name__ == "__main__":
    print(get_coordinates('Kyiv', 'Ukraine', WEATHER_KEY))
    # print(get_city(50.45, 30.52, API_KEY))