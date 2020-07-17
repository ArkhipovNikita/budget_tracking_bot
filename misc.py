import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from middlewares import AccessMiddleware

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(AccessMiddleware(int(os.environ['ACCESS_ID'])))
logging.basicConfig(level=logging.INFO)
