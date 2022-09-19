import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_helper

from config import KiteBotConfig

with open('config.json') as f:
    current_config = KiteBotConfig.fromJson(f.read())
    
asyncio_helper.proxy = current_config.proxy

bot = AsyncTeleBot(current_config.token)

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
	await bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
async def echo_all(message):
	await bot.reply_to(message, message.text)

async def main():
	await bot.polling()

asyncio.run(main())
