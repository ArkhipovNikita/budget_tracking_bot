from aiogram.dispatcher.filters.state import default_state

from actions import save_data_callback
from blocks.date_block import DateBlock
from blocks.input_block import NumberInputBlock, AnyInputBlock
from blocks.option_block import OptionBlock
from loader import dp
from utils.googlespreadsheet import CATEGORIES_WKS_NAME, EXPENSE_CATEGORIES_RANGE, ACCOUNTS_WKS_NAME, \
    ACCOUNT_OPTIONS_RANGE
from utils.googlespreadsheet.lib import get_options


# update values when requested
EXPENSE_CATEGORIES = get_options(CATEGORIES_WKS_NAME, EXPENSE_CATEGORIES_RANGE)
ACCOUNT_OPTIONS = get_options(ACCOUNTS_WKS_NAME, ACCOUNT_OPTIONS_RANGE)
PREFIX = 'expense'

account = OptionBlock(
    states_prefix=PREFIX + ':account',
    options=ACCOUNT_OPTIONS,
    option_name='account',
    entry_message='Choose account from whose the expense was charged',
    send_or_edit_entry_action=0,
    next_state=default_state,
    next_state_action=save_data_callback()
)
description = AnyInputBlock(
    states_prefix=PREFIX + ':description',
    input_name='description',
    entry_message='Write description',
    send_or_edit_entry_action=0,
    next_state=account.entry_state,
    next_state_action=account.entry_action
)
amount = NumberInputBlock(
    states_prefix=PREFIX + ':sum',
    input_name='sum',
    entry_message='Write sum',
    send_or_edit_entry_action=1,
    next_state=description.entry_state,
    next_state_action=description.entry_action
)
date = DateBlock(
    states_prefix=PREFIX,
    next_state=amount.entry_state,
    next_state_action=amount.entry_action
)
category = OptionBlock(
    states_prefix=PREFIX + ':category',
    options=EXPENSE_CATEGORIES,
    option_name='category',
    entry_message='Choose category of an expense',
    send_or_edit_entry_action=0,
    next_state=date.entry_state,
    next_state_action=date.entry_action,
)

date.register()
category.register()
account.register()
description.register()
amount.register()

# CHOOSE CATEGORY
dp.register_message_handler(
    category.entry_action,
    commands='add_expense', state=default_state
)

# error_handler