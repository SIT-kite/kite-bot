import asyncio

from api import run_web_server
import bot 

if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	task = loop.create_task(bot.bot_main())
	run_web_server(loop)
