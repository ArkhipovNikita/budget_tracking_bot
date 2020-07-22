from abc import abstractmethod

import typing

from actions import send_or_edit_message_callback, set_next_state_and_call_on_entry, ActionResult
from blocks import BaseBlock
from loader import dp


class InputBlock(BaseBlock):
    def __init__(self,
                 states_prefix,
                 input_name,
                 entry_message,
                 send_or_edit_entry_action=0):
        super().__init__(states_prefix, ['process'])
        self.__input_name = input_name
        self._entry_action = send_or_edit_message_callback(
            send_or_edit=send_or_edit_entry_action,
            text=entry_message,
            next_state=self._states.process
        )

    def register(self):
        dp.register_message_handler(self.process_input_callback(), state=self._states.process)

    @abstractmethod
    def _validate(self, message: str) -> (bool, typing.Any):
        pass

    def process_input_callback(self):
        @set_next_state_and_call_on_entry(self._next_state, self._next_state_action)
        async def process_input_callback(query, state):
            status, res = self._validate(query.text)
            if not status:
                await query.answer(text=res)
                return ActionResult.FAILED
            else:
                await state.update_data({self.__input_name: res})
                return ActionResult.SUCCESS

        return process_input_callback


class NumberInputBlock(InputBlock):
    def _validate(self, message):
        try:
            if any([sign in message for sign in '.,']):
                num = message
                if ',' in message:
                    num = message.replace(',', '.')
                num = float(num)
            else:
                num = int(message)
        except ValueError:
            return False, 'Please, write a number'
        if num <= 0:
            return False, 'Please, write a positive number'
        return True, num


class AnyInputBlock(InputBlock):
    def _validate(self, message):
        return True, message
