from aiogram.dispatcher.filters.state import default_state

from actions import save_data_callback
from blocks import OptionBlock, AnyInputBlock, NumberInputBlock, DateBlock
from branches.base import BaseBranch
from loader import dp
from utils import Account, Income, IncomeCategory


class AddingIncomeBranch(BaseBranch):
    prefix = 'income'
    exit_point = save_data_callback(Income)
    category = OptionBlock(
        states_prefix=f'{prefix}:category',
        options=IncomeCategory.get_categories,
        option_name='category',
        entry_message='Choose category of an income',
        send_or_edit_entry_action=0,
    )
    date = DateBlock(
        states_prefix=f'{prefix}:date',
    )
    amount = NumberInputBlock(
        states_prefix=f'{prefix}:amount',
        input_name='amount',
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
        options=Account.get_account_names,
        option_name='account',
        entry_message='Choose account to whose the income was received',
        send_or_edit_entry_action=0,
    )


dp.register_message_handler(
    AddingIncomeBranch.category.entry_action,
    commands='add_income', state=default_state
)
