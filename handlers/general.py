from actions_lib import process_cancel_command_callback
from misc import dp


# previous command
# remove last record in a sheet
dp.register_message_handler(process_cancel_command_callback(), commands='cancel', state='*')
