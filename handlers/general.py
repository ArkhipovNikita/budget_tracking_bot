from actions_lib import process_cancel_command_callback
from misc import dp


dp.register_message_handler(process_cancel_command_callback(), commands='cancel', state='*')
# dp.register_message_handler('', commands='previous', state='*')
