from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
import logging


debug = getenv('DEBUG', 'false').lower()
if debug not in ['true', 'false']:
    raise RuntimeError('Unknown debug state')
debug = True if debug == 'true' else False
if debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

bot = Bot(getenv('TG_TOKEN'))

storage_type = getenv('STORAGE_TYPE', 'memory').lower()
if storage_type == 'memory':
    storage = MemoryStorage()
elif storage_type == 'redis':
    storage = RedisStorage(host=getenv('REDIS_HOST', 'localhost'),
                           port=int(getenv('REDIS_PORT', '6379')),
                           db=int(getenv('REDIS_STORAGE_DB', 2)),
                           password=None if getenv('REDIS_PASSWORD', None) == '' else getenv('REDIS_PASSWORD', None))
else:
    raise RuntimeError('Unknown storage')

dp = Dispatcher(bot, storage=storage)
