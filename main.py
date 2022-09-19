import telebot
from telebot import apihelper

apihelper.proxy = {
    'http':'http://127.0.0.1:7890',
    'https':'http://127.0.0.1:7890',
}

bot = telebot.TeleBot("", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()