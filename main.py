import asyncio

from api import run_web_server
from bot import bot_main

if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	task = loop.create_task(bot_main())
	run_web_server(loop)
