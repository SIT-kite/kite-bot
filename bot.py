import asyncio

from telebot.async_telebot import AsyncTeleBot, asyncio_filters
from telebot.types import *
from telebot import asyncio_helper
import database

import bot_message as bm
import sys_info
from config import current_config
import nginx_log as nl
from datetime import timedelta
from kite_server_status import invoke_simple_cmd

bot_config = current_config.bot

asyncio_helper.proxy = bot_config.proxy
bot = AsyncTeleBot(bot_config.token)
chat_id = bot_config.chat_id


@bot.message_handler(chat_id=[chat_id], commands=['now'])
async def send_current_time(message: Message):
    await bot.reply_to(message, bm.build_current_time())


@bot.message_handler(chat_id=[chat_id], commands=['database'])
async def send_database_option(message: Message):
    await bot.reply_to(
        message=message,
        text='可用操作如下：',
        reply_markup=InlineKeyboardMarkup(
            keyboard=[
                [InlineKeyboardButton(text='查询前三条公告', callback_data='select_top_3_notice'),
                 InlineKeyboardButton(text='查询目前总用户数', callback_data='select_user_count')],
                [InlineKeyboardButton(text='照片墙随机选择图片', callback_data='select_board_picture_random'),
                 InlineKeyboardButton(text='卧槽', callback_data='open')],
                [InlineKeyboardButton(text='统计各学院登录比', callback_data='select_college_rate')]
            ]
        ),
    )


@bot.message_handler(chat_id=[chat_id], commands=['server'])
async def send_server_option(message: Message):
    await bot.reply_to(
        message=message,
        text='查看服务器状态：',
        reply_markup=InlineKeyboardMarkup(
            keyboard=[
                [InlineKeyboardButton(text='内存', callback_data='get_memory_info'),
                 InlineKeyboardButton(text='磁盘', callback_data='get_disks_info')],
                [InlineKeyboardButton(text='登录用户', callback_data='get_users_info'),
                 InlineKeyboardButton(text='后端服务状态', callback_data='backend_service_status')],
            ]
        ),
    )


@bot.message_handler(chat_id=[chat_id], commands=['nginx'])
async def send_nginx_option(message: Message):
    await bot.reply_to(
        message=message,
        text='Nginx统计分析：',
        reply_markup=InlineKeyboardMarkup(
            keyboard=[
                [InlineKeyboardButton(text='近十分钟的请求次数', callback_data='query_recently_10min'),
                 InlineKeyboardButton(text='近一小时的请求次数', callback_data='query_recently_1hour')],
                [InlineKeyboardButton(text='近一天的请求次数', callback_data='query_recently_1day'),
                 InlineKeyboardButton(text='近24小时请求折线图', callback_data='draw_recently_24hour')],
            ]
        ),
    )


@bot.callback_query_handler(func=lambda x: x.data == 'backend_service_status')
async def backend_service_status(query: CallbackQuery):
    result = await invoke_simple_cmd('systemctl status kite2.service')
    await send_text_message(f'@{query.from_user.username} \n {result}')


@bot.callback_query_handler(func=lambda x: x.data == 'draw_recently_24hour')
async def draw_recently_24hour(query: CallbackQuery):
    with nl.draw_recently_24hour() as f:
        await send_text_message(f'@{query.from_user.username}')
        await bot.send_photo(
            chat_id=query.message.chat.id,
            photo=f,
        )


@bot.callback_query_handler(func=lambda x: x.data == 'query_recently_10min')
async def query_recently_10min(query: CallbackQuery):
    ss = f'@{query.from_user.username} \n 近十分钟的API请求次数: {nl.count_request_num(timedelta(minutes=10))} '
    await send_text_message(ss)


@bot.callback_query_handler(func=lambda x: x.data == 'query_recently_1hour')
async def query_recently_1hour(query: CallbackQuery):
    ss = f'@{query.from_user.username} \n 近一小时的API请求次数: {nl.count_request_num(timedelta(hours=1))}'
    await send_text_message(ss)


@bot.callback_query_handler(func=lambda x: x.data == 'query_recently_1day')
async def query_recently_1day(query: CallbackQuery):
    ss = f'@{query.from_user.username} \n 近一天的API请求次数: {nl.count_request_num(timedelta(days=1))}'
    await send_text_message(ss)


@bot.callback_query_handler(func=lambda x: x.data == 'get_memory_info')
async def get_memory_info(query: CallbackQuery):
    ss = f'@{query.from_user.username} \n {sys_info.get_memory_info()}'
    await send_text_message(ss)


@bot.callback_query_handler(func=lambda x: x.data == 'get_disks_info')
async def get_disks_info(query: CallbackQuery):
    ss = f'@{query.from_user.username} \n {sys_info.get_disks_info()}'
    await send_text_message(ss)


@bot.callback_query_handler(func=lambda x: x.data == 'get_users_info')
async def get_users_info(query: CallbackQuery):
    ss = f'@{query.from_user.username} \n {sys_info.get_users_info()}'
    await send_text_message(ss)


@bot.callback_query_handler(func=lambda x: x.data == 'select_college_rate')
async def select_college_rate_button_handler(query: CallbackQuery):
    result = await database.select_college_rate()
    ss = f'@{query.from_user.username} 当前学院注册统计：\n'
    for r in result:
        ss += f'{r.rate}   {r.college}   {r.use_count}/{r.total}\n'
    await send_text_message(ss)


@bot.callback_query_handler(func=lambda x: x.data == 'select_top_3_notice')
async def select_top_3_notice_button_handler(query: CallbackQuery):
    result = await database.select_top_3_notice()
    ss = f'@{query.from_user.username} 公告消息：\n\n'
    for r in result:
        ss += f'{r.title}\n{r.content}\n{r.publish_time}\n\n'
    await send_text_message(ss)


@bot.callback_query_handler(func=lambda x: x.data == 'select_user_count')
async def select_user_count_button_handler(query: CallbackQuery):
    await send_text_message(f'@{query.from_user.username} 目前已注册小风筝账户的总用户数：{await database.select_user_count()}')


@bot.callback_query_handler(func=lambda x: x.data == 'select_board_picture_random')
async def select_board_picture_random_button_handler(query: CallbackQuery):
    record = await database.select_board_picture_random()
    if record is None:
        await bot.reply_to(query.message, f'@{query.from_user.username} 找不到图片')
        return

    await bot.send_photo(
        chat_id=chat_id,
        photo=record.path,
        reply_to_message_id=query.message.message_id,
    )


@bot.callback_query_handler(func=lambda x: x.data == 'open')
async def button_handler(query: CallbackQuery):
    await send_text_message(f'@{query.from_user.username} 卧槽按钮被点击了：{query.data}')


async def set_bot_commands():
    await bot.delete_my_commands()
    await bot.set_my_commands(
        commands=[
            BotCommand('now', '获取当前时间'),
            BotCommand('database', '数据库相关查询'),
            BotCommand('server', '服务器信息查询'),
            BotCommand('nginx', 'Nginx统计分析'),
        ]
    )


async def send_text_message(text: str):
    await bot.send_message(
        chat_id=chat_id,
        text=text,
    )


async def polling():
    await bot.polling(
        non_stop=True,
        interval=1,
    )


async def bot_main():
    await database.connect()
    await set_bot_commands()
    await send_text_message(f'KiteBot started at {bm.build_current_time()}!!!')
    bot.add_custom_filter(asyncio_filters.ChatFilter())
    await polling()


if __name__ == '__main__':
    asyncio.run(bot_main())

__all__ = [
    'bot',
    'send_text_message',
    'bot_main'
]
