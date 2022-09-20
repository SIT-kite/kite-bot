from telebot.async_telebot import AsyncTeleBot
from telebot.types import *
from telebot import asyncio_helper

from config import KiteBotConfig

import bot_message as bm

with open('config.json') as f:
    current_config = KiteBotConfig.from_json(f.read())

asyncio_helper.proxy = current_config.proxy

bot = AsyncTeleBot(current_config.token)


@bot.message_handler(commands=['now'])
async def send_current_time(message: Message):
    await bot.reply_to(message, bm.build_current_time())


@bot.message_handler(commands=['button'])
async def send_btn_message(message: Message):
    await bot.send_message(
        chat_id=current_config.chat_id,
        text='button test',
        reply_markup=InlineKeyboardMarkup(
            keyboard=[[
                InlineKeyboardButton(
                    text='打开上应小风筝首页',
                    url='https://kite.sunnysab.cn'
                )
            ]]
        ),
    )


@bot.message_handler(func=lambda m: True)
async def echo_all(message: Message):
    print(message)
    await bot.reply_to(message, message.text)


async def set_bot_commands():
    await bot.delete_my_commands()
    await bot.set_my_commands(
        commands=[
            BotCommand('now', '获取当前时间'),
            BotCommand('button', '测试一个按钮'),
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
    await send_text_message(f'KiteBot started at {bm.build_current_time()}!!!')
    await polling()


__all__ = [
    'bot',
    'send_text_message',
    'bot_main'
]
