from asyncio import sleep
from enum import Enum

from aiogram.dispatcher.filters.state import default_state

from utils.googlespreadsheet import googlesheet_save_data, Expense
from loader import bot


class ActionResult(Enum):
    SUCCESS = 0,
    FAILED = 1


def set_next_state_and_call_on_entry(next_state, next_action):
    def decorator(func):
        async def wrapper(query, state):
            res = await func(query, state)
            if res == ActionResult.SUCCESS:
                if next_state:
                    await next_state.set()
                if next_action:
                    await next_action(query, state)
        return wrapper
    return decorator


async def send_or_edit_message(query, send_or_edit=0, *args, **kwargs):
    if not send_or_edit:
        await query.answer(*args, **kwargs)
    else:
        await bot.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            *args, **kwargs)


def send_or_edit_message_callback(send_or_edit=0, *args, **kwargs):
    async def send_or_edit_message_wrapped(query, state):
        if not send_or_edit:
            await query.answer(*args, **kwargs)
        else:
            await bot.edit_message_text(
                chat_id=query.from_user.id,
                message_id=query.message.message_id,
                *args, **kwargs)
    return send_or_edit_message_wrapped


async def process_cancel_command(query, state):
    await state.set_state(default_state)
    await state.finish()
    await query.answer('You have canceled the process')


def process_cancel_command_callback():
    return process_cancel_command


async def alert(query, text, sec=2):
    msg = await query.answer(text=text)
    await sleep(sec)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)


# add parameter: func that saves data
def save_data_callback():
    async def save_data(query, state):
        data = await state.get_data()
        await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        googlesheet_save_data(data, Expense)
        await state.finish()
    return save_data


# def process_previous_command_callback(previous_state, previous_state_action):
#     @set_next_state_and_call_on_entry(previous_state, previous_state_action)
#     async def process_previous_command(query, state):
#         return ActionResult.Passed
#     return process_previous_command

