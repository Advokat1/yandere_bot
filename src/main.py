#!venv/bin/python
from aiogram import executor
from os import getenv
import logging as log

from config import *
from handlers import *

__all__ = ['app', 'default_handler']


async def on_shutdown(callback):
    if getenv('STORAGE_TYPE') == 'redis':
        log.info('Closing redis connection')
        await app.storage.close()
        await app.storage.wait_closed()
        log.info('Redis connection was stopped.')
    return callback


async def on_startup(callback):
    from config.app import bot
    from config.commands import commands
    await bot.set_my_commands(commands)

    return callback


if __name__ == '__main__':
    executor.start_polling(app.dp, skip_updates=True, on_shutdown=on_shutdown, on_startup=on_startup)
