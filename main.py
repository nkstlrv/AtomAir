import telebot
from telebot import types
import requests
from dotenv import load_dotenv
import os
import time


load_dotenv('Data/.env')

TOKEN = os.getenv("ATOMAIR_TOKEN")
AQI_API = os.getenv("AIRVISUAL_API_KEY")

bot = telebot.TeleBot(TOKEN)


class MenuMarkup:
    mb1 = types.InlineKeyboardButton(text="🏙️ AQI by City name", callback_data='city_name')
    mb2 = types.InlineKeyboardButton(text="🛰️ AQI by Location", callback_data='location')
    mb3 = types.InlineKeyboardButton(text="🧭 Show nearest AQI station", callback_data='nearest_station')
    mb4 = types.InlineKeyboardButton(text="📊 Get global AQI city ranking", callback_data='global_ranking')
    mb5 = types.InlineKeyboardButton(text="📍🌍 Get your coordinates", callback_data='coordinates')
    mb6 = types.InlineKeyboardButton(text="☕ Buy a coffee to the Developer ;)", callback_data='coffee')
    mb7 = types.InlineKeyboardButton(text="Source code ", url='https://github.com/nkstlrv/Atomair')
    m_markup = types.InlineKeyboardMarkup(row_width=2).add(mb1, mb2).add(mb3, mb5).row(mb6).row(mb7)


@bot.message_handler(commands=['start'])
def start_func(message):

    bot.send_message(message.from_user.id, f"Hello there, <b>{message.from_user.first_name}</b>! 👋", parse_mode='html')
    bot.send_message(message.from_user.id, f"My name is <b>Atomair</b> telegram bot 🤖", parse_mode='html')
    bot.send_message(message.from_user.id, f"My mission is to help you get information about current <b>AQI</b> ",
                     parse_mode='html')
    bot.send_message(message.from_user.id, f"🔍 Use /help to see a list of all available commands\n"
                                           f"👨‍💻 And /dev to get development information about this bot"
                                           f"", parse_mode='html')
    bot.send_message(message.from_user.id, f"To call <b><i>Functions menu</i></b> press 👉 /menu", parse_mode='html')


@bot.message_handler(commands=['menu'])
def menu_func(message):
    bot.send_message(message.chat.id, "<b>Functions Menu 📲</b>", parse_mode='html', reply_markup=MenuMarkup.m_markup)


bot.infinity_polling()