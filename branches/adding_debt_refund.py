from aiogram.dispatcher.filters.state import default_state

from actions import save_data_callback
from blocks import OptionBlock, AnyInputBlock, NumberInputBlock, DateBlock
from branches.base import BaseBranch
from loader import dp
from utils import Account, DebtRefund


class AddingDebtRefundBranch(BaseBranch):
    prefix = 'debt_refund'
    exit_point = save_data_callback(DebtRefund)
    who = AnyInputBlock(
        states_prefix=f'{prefix}:who',
        input_name='who',
        entry_message="Write a person's name who refunded money",
        send_or_edit_entry_action=0,
    )
    date = DateBlock(
        states_prefix=f'{prefix}:date',
        send_or_edit_entry_action=0
    )
    amount = NumberInputBlock(
        states_prefix=f'{prefix}:amount',
        input_name='amount',
        entry_message='Write sum',
        send_or_edit_entry_action=1,
    )
    account = OptionBlock(
        states_prefix=f'{prefix}:account',
        options=Account.get_account_names,
        option_name='account',
        entry_message='Choose account to whose the refund was received',
        send_or_edit_entry_action=0,
    )
    description = AnyInputBlock(
        states_prefix=f'{prefix}:description',
        input_name='description',
        entry_message='Write description',
        send_or_edit_entry_action=1,
    )


dp.register_message_handler(
    AddingDebtRefundBranch.who.entry_action,
    commands='add_debt_refund', state=default_state
)
