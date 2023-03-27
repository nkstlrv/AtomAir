import telebot
from telebot import types
import requests
from dotenv import load_dotenv
import os

load_dotenv('Data/.env')

TOKEN = os.getenv("ATOMAIR_TOKEN")
AQI_API = os.getenv("AIRVISUAL_API_KEY")

bot = telebot.TeleBot(TOKEN)


class SourceCodeMarkup:
    b1 = types.InlineKeyboardButton(text="Source code", url='https://github.com/nkstlrv/Atomair')
    markup = types.InlineKeyboardMarkup(row_width=2).add(b1)


@bot.message_handler(commands=['start'])
def start_func(message):

    bot.send_message(message.from_user.id, f"Hello there, <b>{message.from_user.first_name}</b>! 👋", parse_mode='html')
    bot.send_message(message.from_user.id, f"My name is <b>Atomair</b> telegram bot 🤖",
                     parse_mode='html',
                     reply_markup=SourceCodeMarkup.markup)
    bot.send_message(message.from_user.id, f"My mission is to help you get information about current <b>AQI</b> ",
                     parse_mode='html')
    bot.send_message(message.from_user.id, f"Use /help to see a list of all available commands 🔍\n"
                                           f"And /info to get more information about this bot"
                                           f"", parse_mode='html')


bot.infinity_polling()