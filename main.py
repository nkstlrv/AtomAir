import telebot
from telebot import types
import requests
from dotenv import load_dotenv
import os
import time
from Functions import request_aqi, aqi_converter, geocoding
import json
import datetime
import string

load_dotenv('Data/.env')

TOKEN = os.getenv("ATOMAIR_TOKEN")
API_KEY = os.getenv("OPENWEATHER_API_KEY")

bot = telebot.TeleBot(TOKEN)

respond_user = False


class MenuMarkup:
    mb1 = types.InlineKeyboardButton(text="🏙️ AQI by City name", callback_data='city_name')
    mb2 = types.InlineKeyboardButton(text="🛰️ AQI by Location", callback_data='location')
    mb3 = types.InlineKeyboardButton(text="🗺️ AQI map", url="https://www.iqair.com/ru/air-quality-map")
    mb4 = types.InlineKeyboardButton(text="ℹ️ AQI info", callback_data='aqi_info')
    mb5 = types.InlineKeyboardButton(text="☕ Buy a coffee to the Developer ;)", callback_data='coffee')
    mb6 = types.InlineKeyboardButton(text="Source code ", url='https://github.com/nkstlrv/Atomair')
    m_markup = types.InlineKeyboardMarkup(row_width=2).add(mb2, mb1).row(mb3, mb4).row(mb6)


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
    bot.send_message(message.chat.id, "Welcome to the <b>Functions menu</b> 📲\n", parse_mode='html',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, "<b>Choose an option:</b>", parse_mode='html', reply_markup=MenuMarkup.m_markup)


@bot.callback_query_handler(func=lambda call: True)
def menu_callback(call):
    if call.data == 'location':

        bot.send_message(call.from_user.id, 'Great! 🔥\nNow I need to get your location\n\n'
                                            '<b><i>Note:</i></b> if you are using <b>Telegram Desktop</b>'
                                            ' Location Button will NOT work\n\n'
                                            'Return to the /menu',
                         reply_markup=LocationMarkup.l_markup, parse_mode='html')

    elif call.data == 'city_name':
        bot.send_message(call.from_user.id, 'Perfect! 🚀\n\nNow, send me any wished <b>City and Country</b>'
                                            ' in the given format:\n\n'
                                            '<i>Kyiv, Ukraine</i>\n\n'
                                            'Return to the /menu', parse_mode='html')
        global respond_user
        respond_user = True

    elif call.data == 'aqi_info':
        bot.send_message(call.from_user.id, "Here is some information about <b>AQI</b> ℹ️", parse_mode='html')
        bot.send_message(call.from_user.id, "<b>The Air Quality Index (AQI)</b> is a measure of "
                                            "how polluted the air is, ",

                         parse_mode='html')
        bot.send_message(call.from_user.id, "<b><u>The major components of AQI include:</u></b>", parse_mode='html')
        bot.send_message(call.from_user.id, "1. <b>Particulate Matter (PM):</b> This is a "
                                            "mixture of tiny particles and "
                                            "liquid "
                                            "droplets that are suspended in the air. "
                                            "These particles can come from a variety of sources, "
                                            "such as vehicle exhaust, wildfires, and dust storms. \n\n"
                                            "<b><i>PM2.5</i></b> and <b><i>PM10</i></b> are the two main types of "
                                            "particulate matter "
                                            "that are measured for AQI.", parse_mode='html')
        bot.send_message(call.from_user.id, "2. <b>Ozone (O3):</b> Ozone is a gas that is formed when pollutants "
                                            "from sources such as vehicle exhaust and industrial "
                                            "emissions react with sunlight. It is a major component of smog,"
                                            " and it can irritate the eyes, nose, "
                                            "and throat and cause respiratory problems.", parse_mode='html')
        bot.send_message(call.from_user.id, "3. <b>Carbon Monoxide (CO):</b> This is a "
                                            "poisonous gas that is produced when "
                                            "fuels are burned. It can be emitted from vehicles, industrial processes, "
                                            "and wildfires. Exposure to high levels of carbon monoxide can "
                                            "lead to headaches, dizziness, nausea, and even death.", parse_mode='html')
        bot.send_message(call.from_user.id, "4. <b>Sulfur Dioxide (SO2):</b> This is a gas that is "
                                            "produced when fuels that contain sulfur are burned. "
                                            "It can be emitted from power plants and industrial processes. "
                                            "Exposure to high levels of sulfur dioxide can "
                                            "cause respiratory problems and aggravate asthma.", parse_mode='html')
        bot.send_message(call.from_user.id, "5. <b>Nitrogen Dioxide (NO2):</b> This is a gas that is "
                                            "produced when fuels are burned at high temperatures, "
                                            "such as in vehicles and power plants. Exposure to high "
                                            "levels of nitrogen dioxide can cause respiratory problems "
                                            "and aggravate asthma.", parse_mode='html')
        bot.send_message(call.from_user.id, "<b><u>This is a table that shows AQI diapasons:</u></b>",
                         parse_mode='html')
        pic = open("Data/aqi_table.png", 'rb')
        bot.send_photo(call.from_user.id, pic)
        pic.close()
        bot.send_message(call.from_user.id, "Return to the <b>Functions menu</b> /menu", parse_mode='html')


def create_message(data):
    aqi = aqi_converter.pm10_to_aqi(data['components']['pm10'])
    marker = None

    if aqi <= 50:
        marker = "Healthy 🟩"
    elif 50 < aqi <= 100:
        marker = "Acceptable 🟨"
    elif 100 < aqi <= 150:
        marker = "Moderate 🟧"
    elif 150 < aqi <= 200:
        marker = "Unhealthy 🟥"
    elif 200 < aqi <= 300:
        marker = "Very Unhealthy 🟪"
    elif aqi > 300:
        marker = 'Dangerous ⬛💀'

    message = f"<b>Here is your Air quality data:</b>\n\n " \
              f"{marker}\n\n<b>{aqi} AQI</b> \n\n" \
              f"<b>PM 10</b> --> <b>{data['components']['pm10']}</b> μg/m3\n" \
              f"<b>PM 2.5</b> --> <b>{data['components']['pm2_5']}</b> μg/m3\n" \
              f"<b>CO</b> --> <b>{data['components']['co']}</b>μg/m3\n" \
              f"<b>NO</b> --> <b>{data['components']['no']}</b> μg/m3\n" \
              f"<b>NO₂</b> --> <b>{data['components']['no2']}</b> μg/m3\n" \
              f"<b>SO₂</b> --> <b>{data['components']['so2']}</b> μg/m3\n" \
              f"<b>O₃</b> --> <b>{data['components']['o3']}</b> μg/m3\n\n"
    return message


@bot.message_handler(content_types=['location'])
def location_func(message):
    try:
        lat = message.location.latitude
        lon = message.location.longitude
        data = request_aqi.get_location_aqi(lat, lon, API_KEY)
        to_send = create_message(data)

        bot.reply_to(message, 'Location received ✅')
        bot.send_message(message.chat.id, "🔃 Performing your data...", reply_markup=types.ReplyKeyboardRemove())

        bot.send_message(message.chat.id, to_send, parse_mode='html')
        bot.send_message(message.chat.id, "Return to the <b>Functions menu</b> /menu", parse_mode='html')

    except Exception:
        bot.send_message(message.chat.id, "‼️<b>  ERROR </b>️‼️\nCan not find anything by given info 😥\n\n"
                                          " <u>Possible reasons:</u>\n"
                                          "1. Unsupported location\n"
                                          "2. AQI server is not responding\n"
                                          "3. Issues on the Telegram's server\n", parse_mode='html')
        bot.send_message(message.chat.id, "Return to the <b>Functions menu</b> /menu", parse_mode='html')


@bot.message_handler(content_types=['text'])
def city_name_func(message):
    global respond_user
    if respond_user is True:
        usr_list = [w.strip() for w in message.text.split(',')]

        wrong_format_message = "It seems you are using the wrong format 🤔"
        print(usr_list)

        if len(usr_list) != 2:
            print(usr_list)
            bot.reply_to(message, text=wrong_format_message)
            return

        for _ in usr_list:
            if not _.isalpha() and " " not in [c for c in _]:
                bot.reply_to(message, text=wrong_format_message)
                return
            elif _ == " ":
                continue

        bot.reply_to(message, text="Got it ✅")
        bot.send_message(message.chat.id, "🔃 Performing your data...")

        try:
            coordinates = geocoding.get_coordinates(usr_list[0].title(), usr_list[1].title(), API_KEY)
            data = request_aqi.get_location_aqi(coordinates[0], coordinates[1], API_KEY)

            to_send = create_message(data)
            bot.send_message(message.chat.id, to_send, parse_mode='html')
            bot.send_message(message.chat.id, "Return to the <b>Functions menu</b> /menu", parse_mode='html')
            respond_user = False

        except IndexError:
            bot.send_message(message.chat.id, "❗❗❗<b>ERROR </b>️️❗❗❗\nCan not find anything by given info 😥\n\n"
                                              " <u>Possible reasons:</u>\n"
                                              "1. Wrong city or country spelling\n"
                                              "2. Wrong city or country order\n"
                                              "3. AQI server is not responding\n"
                                              "4. Issues on the Telegram's server\n", parse_mode='html')
            bot.send_message(message.chat.id, "Return to the <b>Functions menu</b> /menu", parse_mode='html')

    else:
        return


bot.infinity_polling()
