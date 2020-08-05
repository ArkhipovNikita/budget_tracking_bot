from aiogram.dispatcher.filters.state import default_state

from actions import save_data_callback
from blocks import OptionBlock, AnyInputBlock, NumberInputBlock, DateBlock
from branches.base import BaseBranch
from loader import dp
from utils import Account, Transfer


class TransferBranch(BaseBranch):
    prefix = 'transfer'
    exit_point = save_data_callback(Transfer)
    date = DateBlock(
        states_prefix=f'{prefix}:date',
        send_or_edit_entry_action=0
    )
    from_account = OptionBlock(
        states_prefix=f'{prefix}:from_account',
        options=Account.get_account_names,
        option_name='from_account',
        entry_message='Choose account from whose money was charged',
        send_or_edit_entry_action=1,
    )
    to_account = OptionBlock(
        states_prefix=f'{prefix}:to_account',
        options=Account.get_account_names,
        option_name='to_account',
        entry_message='Choose account to whose money was received',
        send_or_edit_entry_action=1,
    )
    amount = NumberInputBlock(
        states_prefix=f'{prefix}:amount',
        input_name='amount',
        entry_message='Write sum',
        send_or_edit_entry_action=1,
    )
    exchange_rate = NumberInputBlock(
        states_prefix=f'{prefix}:exchange_rate',
        input_name='exchange_rate',
        entry_message='Write exchange rate',
        send_or_edit_entry_action=0,
    )
    description = AnyInputBlock(
        states_prefix=f'{prefix}:description',
        input_name='description',
        entry_message='Write description',
        send_or_edit_entry_action=0,
    )


dp.register_message_handler(
    TransferBranch.date.entry_action,
    commands='add_transfer', state=default_state
)
