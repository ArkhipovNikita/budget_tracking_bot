import logging

from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

from config import WEBHOOK_URL, WEBHOOK_PATH, APP_PORT
from handlers import dp
from loader import bot


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dispatcher):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host='0.0.0.0',
    #     port=APP_PORT
    # )
