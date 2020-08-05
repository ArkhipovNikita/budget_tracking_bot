import typing
from enum import Enum

from aiogram.dispatcher.filters.state import State
from aiogram.types import CallbackQuery, Message

import utils.googlespreadsheet as gs
from loader import bot


class ActionResult(Enum):
    SUCCESS = 0,
    FAILED = 1


def set_next_state_and_call_on_entry(next_state: typing.Union[str, State], next_state_action=None):
    def decorator(func):
        async def wrapper(query, state):
            res = await func(query, state)
            if res == ActionResult.SUCCESS:
                if next_state:
                    if next_state is str:
                        await state.set_state(next_state)
                    else:
                        await next_state.set()
                if next_state_action:
                    await next_state_action(query, state)

        return wrapper

    return decorator


def save_data_callback(model: type(gs.Model)):
    async def save_data(query, state):
        data = await state.get_data()
        # Удалить сообщение, если callback
        if isinstance(query, CallbackQuery):
            await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        model.bind_and_save(data)
        await state.finish()
        await bot.send_message(chat_id=query.from_user.id, text='Data has been successfully saved')

    return save_data


async def send_or_edit_message(query, send_or_edit=0, *args, **kwargs):
    if not send_or_edit:
        await query.answer(*args, **kwargs)
    else:
        if isinstance(query, CallbackQuery):
            chat_id = query.from_user.id
            message_id = query.message.message_id
        elif isinstance(query, Message):
            chat_id = query.chat.id
            message_id = query.message_id
        else:
            raise Exception(f'Editing is not supported for {type(query)} type of query.')
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, *args, **kwargs)


def send_or_edit_message_callback(send_or_edit=0, next_state=None, next_state_action=None, *args, **kwargs):
    @set_next_state_and_call_on_entry(next_state, next_state_action)
    async def send_or_edit_message_wrapped(query, state):
        await send_or_edit_message(query, send_or_edit, *args, **kwargs)
        return ActionResult.SUCCESS

    return send_or_edit_message_wrapped
