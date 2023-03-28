import requests
import json
import os
from dotenv import load_dotenv
import datetime
from Functions import geocoding


def convert(unix):
    res = datetime.datetime.fromtimestamp(unix).strftime('%H:%M:%S %Y-%m-%d')
    return res


load_dotenv('../Data/.env')
API_KEY = os.getenv("OPENWEATHER_API_KEY")


class IndexConverter:
    pass


def get_location_aqi(lat, lon, key):
    req = requests.get(
        f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}').json()

    data = {
        "components": req['list'][0]['components'],
        "time": convert(req['list'][0]['dt'])
            }

    return data


def get_city_aqi(city, country, key):

    coordinates = geocoding.get_coordinates(city, country, key)

    return get_location_aqi(coordinates[0], coordinates[1], key)



if __name__ == "__main__":

    # 50.391850, 30.629098
    # print(get_location_aqi(50.391850, 30.629098, API_KEY))

    print(get_city_aqi('Kyiv', 'Ukraine', API_KEY))