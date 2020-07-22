from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from actions.common import set_next_state_and_call_on_entry, ActionResult, send_or_edit_message


def create_options_keyboard(options):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    for i, opt in enumerate(options):
        keyboard.add(InlineKeyboardButton(opt, callback_data=str(i)))
    return keyboard


def send_options_keyboard_callback(options, text, next_state=None, next_state_action=None, send_or_edit=0):
    @set_next_state_and_call_on_entry(next_state, next_state_action)
    async def send_options_keyboard(query, state):
        keyboard = create_options_keyboard(options)
        await send_or_edit_message(query, send_or_edit, text=text, reply_markup=keyboard)
        return ActionResult.SUCCESS
    return send_options_keyboard


def process_option_selection_callback(option_name, options, next_state=None, next_state_action=None):
    @set_next_state_and_call_on_entry(next_state, next_state_action)
    async def process_option_selection(query, state):
        await state.update_data({option_name: options[int(query.data)]})
        return ActionResult.SUCCESS
    return process_option_selection
