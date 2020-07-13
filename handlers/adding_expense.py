from aiogram.dispatcher.filters.state import StatesGroup, State, default_state

from actions_lib import send_options_keyboard_callback, process_option_selection_callback, DATE_OPTIONS, \
    process_today_callback, send_or_edit_message_callback, process_yesterday_callback, send_custom_date_callback, \
    process_custom_date_callback, save_data_callback
from actions_lib.write_description import process_writing_desc_callback
from actions_lib.write_sum import process_writing_sum_callback
from misc import dp


class AddingExpense(StatesGroup):
    choosing_date = State()
    choosing_custom_date = State()
    choosing_category = State()
    choosing_sum = State()
    choosing_description = State()
    choosing_account = State()


# взять с таблицы бюджета
EXPENSE_CATEGORIES = [
    'дом',
    'машина',
    '...',
]
ACCOUNT_OPTIONS = ['Счет1', 'Счет2', '...']

# CHOOSE CATEGORY
dp.register_message_handler(
    send_options_keyboard_callback(options=EXPENSE_CATEGORIES,
                                   text='Choose category of an expense',
                                   next_state=AddingExpense.choosing_category),
    commands='add_expense', state=default_state
)
dp.register_callback_query_handler(
    process_option_selection_callback(opt_key='category',
                                      next_state=AddingExpense.choosing_date,
                                      next_action=send_options_keyboard_callback(
                                          options=DATE_OPTIONS,
                                          text='Choose date of the expense',
                                          send_or_edit=1,
                                      )),
    state=AddingExpense.choosing_category
)

# CHOOSE DATE
dp.register_callback_query_handler(
    process_today_callback(next_state=AddingExpense.choosing_sum,
                           next_action=send_or_edit_message_callback(send_or_edit=1,
                                                                     text='Write sum')),
    lambda x: x.data == 'Today', state=AddingExpense.choosing_date
)
dp.register_callback_query_handler(
    process_yesterday_callback(next_state=AddingExpense.choosing_sum,
                               next_action=send_or_edit_message_callback(send_or_edit=1,
                                                                         text='Write sum')),
    lambda x: x.data == 'Yesterday', state=AddingExpense.choosing_date
)
dp.register_callback_query_handler(
    send_custom_date_callback(send_or_edit=1,
                              next_state=AddingExpense.choosing_custom_date),
    lambda x: x.data == 'Custom date', state=AddingExpense.choosing_date
)
dp.register_callback_query_handler(
    process_custom_date_callback(next_state=AddingExpense.choosing_sum,
                                 next_action=send_or_edit_message_callback(send_or_edit=1,
                                                                           text='Write sum')),
    state=AddingExpense.choosing_custom_date
)

# WRITE SUM
dp.register_message_handler(
    process_writing_sum_callback(next_state=AddingExpense.choosing_description,
                                 next_action=send_or_edit_message_callback(text='Write description')),
    state=AddingExpense.choosing_sum
)

# WRITE DESCRIPTION
dp.register_message_handler(
    process_writing_desc_callback(next_state=AddingExpense.choosing_account,
                                  next_action=send_options_keyboard_callback(
                                      options=ACCOUNT_OPTIONS,
                                      text='Choose account from whose the expense was charged')),
    state=AddingExpense.choosing_description
)

# CHOOSE ACCOUNT
dp.register_callback_query_handler(
    process_option_selection_callback(opt_key='account',
                                      next_state=default_state,
                                      next_action=save_data_callback()),
    state=AddingExpense.choosing_account
)

# error_handler
