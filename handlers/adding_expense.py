from aiogram.dispatcher.filters.state import StatesGroup, State, default_state

from handlers.helpers import *
from misc import dp


class AddingExpense(StatesGroup):
    choosing_category = State()
    choosing_date = State()
    choosing_custom_date = State()
    choosing_sum = State()
    choosing_description = State()
    choosing_account = State()


# взять с таблицы бюджета
expense_categories = [
    'дом',
    'машина',
    '...',
]

dp.register_message_handler(
    send_options_keyboard_callback(options=expense_categories,
                                   text='Choose category of an expense',
                                   next_state=AddingExpense.choosing_category),
    commands='add_expense', state=default_state
)
dp.register_callback_query_handler(
    process_option_selection_callback(options=expense_categories,
                                      opt_key='category',
                                      previous_state=AddingExpense.choosing_category,
                                      next_state=AddingExpense.choosing_date,
                                      next_state_on_entry_action=send_options_keyboard_callback(
                                          options=date_options,
                                          text='Choose date of the expense',
                                          send_or_edit=1,
                                      )),
    state=AddingExpense.choosing_category
)
dp.register_callback_query_handler(
    process_today_callback(next_state=AddingExpense.choosing_sum,
                           next_state_on_entry_action=send_message_callback(send_or_edit=1,
                                                                            text='Write sum')),
    lambda x: x.data == 'CHOSEN;Today', state=AddingExpense.choosing_date
)
dp.register_callback_query_handler(
    process_yesterday_callback(next_state=AddingExpense.choosing_sum,
                               next_state_on_entry_action=send_message_callback(send_or_edit=1,
                                                                                text='Write sum')),
    lambda x: x.data == 'CHOSEN;Yesterday', state=AddingExpense.choosing_date
)
dp.register_callback_query_handler(
    send_custom_date_callback(send_or_edit=1,
                              next_state=AddingExpense.choosing_custom_date),
    lambda x: x.data == 'CHOSEN;Custom date', state=AddingExpense.choosing_date
)
dp.register_callback_query_handler(
    process_custom_date_callback(next_state=AddingExpense.choosing_sum,
                                 next_state_on_entry_action=send_message_callback(send_or_edit=1,
                                                                                  text='Write sum')),
    state=AddingExpense.choosing_custom_date
)
