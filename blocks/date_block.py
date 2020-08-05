from datetime import datetime, timedelta

from pytz import timezone

from actions import send_options_keyboard_callback
from actions.common import ActionResult, set_next_state_and_call_on_entry, send_or_edit_message
from blocks.base_block import BaseBlock
from keyboards import calendar
from loader import bot, dp


class DateBlock(BaseBlock):
    options = ['Today', 'Yesterday', 'Custom date']

    def __init__(self,
                 states_prefix,
                 send_or_edit_entry_action=1):
        super().__init__(states_prefix, ['date', 'custom_date'])
        self._entry_action = send_options_keyboard_callback(
            options=DateBlock.options,
            text='Choose date of the expense',
            send_or_edit=send_or_edit_entry_action,
            next_state=self._states.date
        )

    def register(self):
        dp.register_callback_query_handler(
            self.process_today_callback(),
            lambda x: x.data == str(DateBlock.options.index('Today')), state=self._states.date
        )
        dp.register_callback_query_handler(
            self.process_yesterday_callback(),
            lambda x: x.data == str(DateBlock.options.index('Yesterday')), state=self._states.date
        )
        dp.register_callback_query_handler(
            self.send_custom_date_callback(),
            lambda x: x.data == str(DateBlock.options.index('Custom date')), state=self._states.date
        )
        dp.register_callback_query_handler(
            self.process_custom_date_callback(),
            state=self._states.custom_date
        )

    def process_today_callback(self):
        @set_next_state_and_call_on_entry(self._next_state, self._next_state_action)
        async def process_today_option(query, state):
            today = datetime.now(tz=timezone('Europe/Moscow')).strftime('%d.%m.%Y')
            await state.update_data(date=today)
            return ActionResult.SUCCESS

        return process_today_option

    def process_yesterday_callback(self):
        @set_next_state_and_call_on_entry(self._next_state, self._next_state_action)
        async def process_yesterday_option(query, state):
            yesterday = (datetime.now(tz=timezone('Europe/Moscow')) - timedelta(days=1)).strftime('%d.%m.%Y')
            await state.update_data(date=yesterday)
            return ActionResult.SUCCESS

        return process_yesterday_option

    def send_custom_date_callback(self):
        @set_next_state_and_call_on_entry(self._states.custom_date)
        async def send_custom_date_options(query, state):
            await send_or_edit_message(query, send_or_edit=1, text='Choose date of the expense',
                                       reply_markup=calendar.create_calendar())
            return ActionResult.SUCCESS

        return send_custom_date_options

    def process_custom_date_callback(self):
        @set_next_state_and_call_on_entry(self._next_state, self._next_state_action)
        async def process_custom_date_option(query, state):
            selected, date = await calendar.process_calendar_selection(bot, query)
            if not selected:
                return ActionResult.FAILED
            await state.update_data(date=date.strftime('%m.%d.%Y'))
            return ActionResult.SUCCESS

        return process_custom_date_option
