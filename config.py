import os

WEBHOOK_PATH = os.environ.get('WEBHOOK_PATH')
WEBHOOK_PORT = os.environ.get('WEBHOOK_PORT', 443)
WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST')
APP_PORT = os.environ.get('PORT', 8080)
BOT_TOKEN = os.environ.get('TOKEN')
ACCESS_ID = int(os.environ.get('ACCESS_ID'))
WEBHOOK_URL = 'https://{}:{}/{}'.format(WEBHOOK_HOST, WEBHOOK_PORT, WEBHOOK_PATH)
