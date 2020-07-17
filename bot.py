import logging

import os

from aiogram.utils.executor import start_webhook

from misc import dp, bot
import handlers

WEBHOOK_URL = 'https://{}:{}/{}'.format(os.environ['WEBHOOK_HOST'], os.environ['WEBHOOK_PORT'],
                                        os.environ['WEBHOOK_PATH'])


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=os.environ['WEBHOOK_PATH'],
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=os.environ['PORT']
    )
