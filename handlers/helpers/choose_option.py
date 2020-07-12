from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.helpers.general import set_next_state_and_call_on_entry, ActionState, send_message
from misc import bot


def create_options_keyboard(options):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    for i, opt in enumerate(options):
        keyboard.add(InlineKeyboardButton(opt, callback_data='CHOSEN;' + opt))
    # keyboard.add(InlineKeyboardButton('Previous step', callback_data='PREVIOUS;0'))
    # keyboard.add(InlineKeyboardButton('Cancel', callback_data='CANCEL;0'))
    return keyboard


def send_options_keyboard_callback(options, text, next_state=None, next_state_on_entry_action=None, send_or_edit=0):
    @set_next_state_and_call_on_entry(next_state, next_state_on_entry_action)
    async def send_options_keyboard(query, state):
        keyboard = create_options_keyboard(options)
        await send_message(query, send_or_edit, text=text, reply_markup=keyboard)
        return ActionState.Passed
    return send_options_keyboard


def process_option_selection_callback(opt_key, options, previous_state, next_state=None, next_state_on_entry_action=None):
    @set_next_state_and_call_on_entry(next_state, next_state_on_entry_action)
    async def process_option_selection(call, fsm_context):
        data = call.data
        # action, index = data.split(';')
        action, opt = data.split(';')
        # index = int(index)
        if action == 'CHOSEN':
            await fsm_context.update_data({opt_key: opt})
        # elif action == 'CANCEL':
        #     await fsm_context.set_state(default_state)
        # elif action == 'PREVIOUS':
        #     await fsm_context.set_state(previous_state)
        else:
            await bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text='Something went wrong!',
            )
        return ActionState.Passed
    return process_option_selection
