from aiogram.dispatcher.filters.state import default_state

from actions import save_data_callback
from blocks import OptionBlock, AnyInputBlock, NumberInputBlock, DateBlock
from branches.base import BaseBranch
from loader import dp
from utils import get_options, CATEGORIES_WKS_NAME, EXPENSE_CATEGORIES_RANGE, ACCOUNT_OPTIONS_RANGE, \
    ACCOUNTS_WKS_NAME, Expense

EXPENSE_CATEGORIES = get_options(CATEGORIES_WKS_NAME, EXPENSE_CATEGORIES_RANGE)
ACCOUNT_OPTIONS = get_options(ACCOUNTS_WKS_NAME, ACCOUNT_OPTIONS_RANGE)


class AddingExpenseBranch(BaseBranch):
    prefix = 'expense'
    exit_point = save_data_callback(Expense)
    category = OptionBlock(
        states_prefix=f'{prefix}:category',
        options=EXPENSE_CATEGORIES,
        option_name='category',
        entry_message='Choose category of an expense',
        send_or_edit_entry_action=0,
    )
    date = DateBlock(
        states_prefix=f'{prefix}',
    )
    amount = NumberInputBlock(
        states_prefix=f'{prefix}:amount',
        input_name='sum',
        entry_message='Write sum',
        send_or_edit_entry_action=1,
    )
    description = AnyInputBlock(
        states_prefix=f'{prefix}:description',
        input_name='description',
        entry_message='Write description',
        send_or_edit_entry_action=0,
    )
    account = OptionBlock(
        states_prefix=f'{prefix}:account',
        options=ACCOUNT_OPTIONS,
        option_name='account',
        entry_message='Choose account from whose the expense was charged',
        send_or_edit_entry_action=0,
    )


dp.register_message_handler(
    AddingExpenseBranch.category.entry_action,
    commands='add_expense', state=default_state
)
