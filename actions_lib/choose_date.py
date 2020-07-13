from datetime import datetime, timedelta

from pytz import timezone

from actions_lib.general import ActionResult, set_next_state_and_call_on_entry, send_or_edit_message
from misc import bot
from third_party_libs.telegramcalendar import telegramcalendar

DATE_OPTIONS = ['Today', 'Yesterday', 'Custom date']


def process_today_callback(next_state=None, next_action=None):
    @set_next_state_and_call_on_entry(next_state, next_action)
    async def process_today_option(query, state):
        today = datetime.now(tz=timezone('Europe/Moscow')).strftime('%d.%m.%Y')
        await state.update_data(date=today)
        return ActionResult.SUCCESS
    return process_today_option


def process_yesterday_callback(next_state=None, next_action=None):
    @set_next_state_and_call_on_entry(next_state, next_action)
    async def process_yesterday_option(query, state):
        yesterday = (datetime.now(tz=timezone('Europe/Moscow'))-timedelta(days=1)).strftime('%d.%m.%Y')
        await state.update_data(date=yesterday)
        return ActionResult.SUCCESS
    return process_yesterday_option


def send_custom_date_callback(next_state=None, next_action=None, send_or_edit=0):
    @set_next_state_and_call_on_entry(next_state, next_action)
    async def send_custom_date_options(query, state):
        await send_or_edit_message(query, send_or_edit, text='Choose date of the expense',
                                   reply_markup=telegramcalendar.create_calendar())
        return ActionResult.SUCCESS
    return send_custom_date_options


def process_custom_date_callback(next_state=None, next_action=None):
    @set_next_state_and_call_on_entry(next_state, next_action)
    async def process_custom_date_option(query, state):
        selected, date = await telegramcalendar.process_calendar_selection(bot, query)
        if not selected:
            return ActionResult.FAILED
        await state.update_data(date=query.data)
        return ActionResult.SUCCESS
    return process_custom_date_option