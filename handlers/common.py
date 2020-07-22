from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import default_state
from aiogram.types import Message

from loader import dp, bot


@dp.message_handler(commands='cancel', state='*')
async def process_cancel_command(query: Message, state: FSMContext):
    await state.set_state(default_state)
    await state.finish()
    await query.answer('You have canceled the process')
