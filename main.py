import telebot
from telebot import types
import requests
from dotenv import load_dotenv
import os
import time
from Functions import aqi, geocoding
import json
import datetime


load_dotenv('Data/.env')

TOKEN = os.getenv("ATOMAIR_TOKEN")
API_KEY = os.getenv("OPENWEATHER_API_KEY")

bot = telebot.TeleBot(TOKEN)


class MenuMarkup:
    mb1 = types.InlineKeyboardButton(text="🏙️ AQI by City name", callback_data='city_name')
    mb2 = types.InlineKeyboardButton(text="🛰️ AQI by Location", callback_data='location')
    mb3 = types.InlineKeyboardButton(text="🗺️ AQI map", callback_data='nearest_station')
    mb4 = types.InlineKeyboardButton(text="ℹ️ AQI info", callback_data='nearest_station')
    mb5 = types.InlineKeyboardButton(text="☕ Buy a coffee to the Developer ;)", callback_data='coffee')
    mb6 = types.InlineKeyboardButton(text="Source code ", url='https://github.com/nkstlrv/Atomair')
    m_markup = types.InlineKeyboardMarkup(row_width=2).add(mb2, mb1).row(mb3, mb4).row(mb5).row(mb6)


class LocationMarkup:
    l_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    lb = types.KeyboardButton(request_location=True, text='Send location')
    l_markup.add(lb)



@bot.message_handler(commands=['start'])
def start_func(message):
    bot.send_message(message.chat.id, f"Hello there, <b>{message.from_user.first_name}</b>! 👋", parse_mode='html')
    bot.send_message(message.chat.id, f"My name is <b>Atomair</b> telegram bot 🤖", parse_mode='html')
    bot.send_message(message.chat.id, f"My mission is to help you get information about current <b>AQI</b> ",
                     parse_mode='html')
    bot.send_message(message.chat.id, f"🔍 Use /help to see a list of all available commands\n"
                                           f"👨‍💻 And /dev to get development information about this bot"
                                           f"", parse_mode='html')
    bot.send_message(message.chat.id, f"To call <b><i>Functions menu</i></b> press 👉 /menu", parse_mode='html')


@bot.message_handler(commands=['menu'])
def menu_func(message):
    bot.send_message(message.chat.id, "Welcome to the <b>Main menu</b> 📲\n"
                                      "Here you can find <i>Atomair's</i> main "
                                      "functions ⚙️", parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, "<b>Choose an option:</b>", parse_mode='html', reply_markup=MenuMarkup.m_markup)


@bot.callback_query_handler(func=lambda call: True)
def menu_callback(call):
    if call.data == 'location':

        bot.send_message(call.from_user.id, 'Great! 🔥\nNow I need to get your location\n\n'
                                            '<b><i>Note:</i></b> if you are using <b>Telegram Desktop</b>'
                                            ' Location Button will NOT work\n'
                                            'Return to the /menu',
                         reply_markup=LocationMarkup.l_markup, parse_mode='html')


@bot.message_handler(content_types=['location'])
def location_func(message):
    lat = message.location.latitude
    lon = message.location.longitude
    bot.reply_to(message, 'Location received ✅')
    bot.send_message(message.chat.id, "🔃 Performing your data...", reply_markup=types.ReplyKeyboardRemove())

    aqi_data = aqi.get_location_aqi(lat, lon, API_KEY)

    marker = None

    if aqi_data['components']['pm10'] <= 20:
        marker = "Healthy 🟩"
    elif 20 < aqi_data['components']['pm10'] <= 50:
        marker = "Acceptable 🟨"
    elif 50 < aqi_data['components']['pm10'] <= 100:
        marker = "Moderate 🟧"
    elif 100 < aqi_data['components']['pm10'] <= 200:
        marker = "Unhealthy 🟥"
    elif aqi_data['components']['pm10'] > 200:
        marker = "Dangerous 🟪"

    bot.send_message(message.chat.id, f"<b>Air quality in your area:</b>\n\n"
                                      f"{marker} \n<b>{aqi_data['components']['pm10']}AQI</b> \n\n"
                                      f"<b>CO</b> --> <b>{aqi_data['components']['co']}</b>μg/m3\n"
                                      f"<b>NO</b> --> <b>{aqi_data['components']['no']}</b> μg/m3\n"
                                      f"<b>NO₂</b> --> <b>{aqi_data['components']['no2']}</b> μg/m3\n"
                                      f"<b>SO₂</b> --> <b>{aqi_data['components']['so2']}</b> μg/m3\n"
                                      f"<b>O₃</b> --> <b>{aqi_data['components']['o3']}</b> μg/m3\n"
                                      f"<b>PM 2.5</b> --> <b>{aqi_data['components']['pm2_5']}</b> μg/m3\n"
                                      f"<b>PM 10</b> --> <b>{aqi_data['components']['pm10']}</b> μg/m3\n",
                     parse_mode='html')
    bot.send_message(message.chat.id, "Return to the <b>Main menu</b> /menu", parse_mode='html')



bot.infinity_polling()
