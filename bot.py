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


@bot.callback_query_handler(func=lambda x: True)
async def button_handler(query: CallbackQuery):
    await send_text_message(f'按钮被点击：{query.data}')


@bot.message_handler(commands=['button'])
async def send_btn_message(message: Message):
    await bot.send_message(
        chat_id=current_config.chat_id,
        text='button test',
        reply_markup=InlineKeyboardMarkup(
            keyboard=[[
                InlineKeyboardButton(
                    text='打开上应小风筝首页',
                    callback_data='open',
                )
            ]]
        ),
    )


@bot.message_handler(commands=['reply'])
async def reply_txc_message(message: Message):
    reply_to_message = message.reply_to_message.text
    post_url = reply_to_message.splitlines()[3].split(':')[1].strip()
    reply_message = message.text
    await bot.reply_to(
        message=message,
        text=f'您正在回复帖子：{post_url}, 内容为：{reply_message}',
    )


@bot.message_handler(func=lambda m: True)
async def echo_all(message: Message):
    if message.from_user.username == 'NoCodeToday':
        await bot.reply_to(message, '别水群了，快去学Rust')

    await bot.reply_to(message, message.text.replace("吗", "").replace("？", "！"))


async def set_bot_commands():
    await bot.delete_my_commands()
    await bot.set_my_commands(
        commands=[
            BotCommand('now', '获取当前时间'),
            BotCommand('reply', '回复'),
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
