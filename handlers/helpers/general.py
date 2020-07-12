from enum import Enum

from misc import bot


class ActionState(Enum):
    Passed = 0,
    Failed = 1


def set_next_state_and_call_on_entry(next_state, next_state_on_entry_action):
    def decorator(func):
        async def wrapper(query, state):
            res = await func(query, state)
            if res == ActionState.Passed:
                if next_state:
                    await next_state.set()
                if next_state_on_entry_action:
                    await next_state_on_entry_action(query, state)

        return wrapper

    return decorator


async def send_message(query, send_or_edit=0, *args, **kwargs):
    if not send_or_edit:
        await query.answer(*args, **kwargs)
    else:
        await bot.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            *args, **kwargs)


def send_message_callback(send_or_edit=0, *args, **kwargs):
    async def send_message_wrapped(query, state):
        if not send_or_edit:
            await query.answer(*args, **kwargs)
        else:
            await bot.edit_message_text(
                chat_id=query.from_user.id,
                message_id=query.message.message_id,
                *args, **kwargs)

    return send_message_wrapped
