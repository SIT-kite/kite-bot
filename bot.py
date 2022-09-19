from telebot.async_telebot import AsyncTeleBot
from telebot.types import *
from telebot import asyncio_helper

from config import KiteBotConfig

with open('config.json') as f:
    current_config = KiteBotConfig.fromJson(f.read())

asyncio_helper.proxy = current_config.proxy

bot = AsyncTeleBot(current_config.token)


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    await bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
async def echo_all(message: Message):
    print(message.chat.type)
    print(message)
    await bot.reply_to(message, message.text)


async def set_bot_commands():
    await bot.delete_my_commands()
    await bot.set_my_commands(
        commands=[
            BotCommand('command1', 'command1 description'),
            BotCommand('command2', 'command2 description'),
            BotCommand('start', 'start description'),
        ]
    )


async def send_text_message(text: str):
    await bot.send_message(
        chat_id=current_config.chat_id,
        text=text,
    )


async def polling():
    await bot.polling()


async def bot_main():
    await set_bot_commands()
    await send_text_message('KiteBot started!!!')
    await polling()


__all__ = [
    'bot',
    'send_text_message',
    'bot_main'
]
