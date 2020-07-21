from actions import process_cancel_command_callback
from loader import dp
import aiogram.utils.exceptions as ex

# previous command
# remove last record in a sheet
dp.register_message_handler(process_cancel_command_callback(), commands='cancel', state='*')
