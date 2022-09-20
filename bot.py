from telebot.async_telebot import AsyncTeleBot
from telebot.types import *
from telebot import asyncio_helper

from config import KiteBotConfig

import bot_message as bm

from config import current_config

import database

asyncio_helper.proxy = current_config.proxy

bot = AsyncTeleBot(current_config.token)


@bot.message_handler(commands=['now'])
async def send_current_time(message: Message):
    await bot.reply_to(message, bm.build_current_time())


@bot.message_handler(commands=['database'])
async def send_database_option(message: Message):
    await bot.send_message(
        chat_id=current_config.chat_id,
        text='可用操作如下：',
        reply_markup=InlineKeyboardMarkup(
            keyboard=[
                [InlineKeyboardButton(text='查询前三条公告', callback_data='select_top_3_notice'),
                 InlineKeyboardButton(text='查询目前总用户数', callback_data='select_user_count')],
                [InlineKeyboardButton(text='卧槽', callback_data='open'),
                 InlineKeyboardButton(text='卧槽', callback_data='open')]
            ]
        ),
    )


@bot.callback_query_handler(func=lambda x: x.data == 'select_top_3_notice')
async def select_top_3_notice_button_handler(query: CallbackQuery):
    await send_text_message(f'公告消息：{await database.select_top_3_notice()}')


@bot.callback_query_handler(func=lambda x: x.data == 'select_user_count')
async def select_user_count_button_handler(query: CallbackQuery):
    await send_text_message(f'目前总用户数：{await database.select_user_count()}')


@bot.callback_query_handler(func=lambda x: x.data == 'open')
async def button_handler(query: CallbackQuery):
    await send_text_message(f'卧槽按钮被点击了：{query.data}')


@bot.message_handler(func=lambda m: True)
async def reply_txc_message(message: Message):
    reply_to_message = message.reply_to_message.text
    if '兔小巢消息' not in reply_to_message:
        return
    # 获取消息url
    post_url = reply_to_message.splitlines()[3].split(': ')[1].strip()
    await bot.reply_to(
        message=message,
        text=f'您正在回复帖子：{post_url}, 内容为：{message.text}',
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
            BotCommand('database', '数据库相关查询'),
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
    await database.connect()
    await set_bot_commands()
    await send_text_message(f'KiteBot started at {bm.build_current_time()}!!!')
    await polling()


__all__ = [
    'bot',
    'send_text_message',
    'bot_main'
]
