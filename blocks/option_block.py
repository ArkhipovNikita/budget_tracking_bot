from typing import List, Callable

from actions import process_option_selection_callback, send_options_keyboard_callback, typing
from blocks.base_block import BaseBlock
from loader import dp


class OptionBlock(BaseBlock):
    def __init__(self,
                 states_prefix,
                 options: typing.Union[List[str], Callable[[], List[str]]],
                 option_name,
                 entry_message,
                 send_or_edit_entry_action=0):
        super().__init__(states_prefix, ['choose', 'process'])
        self.__option_name = option_name
        self.__options = options
        self.__using_options = []

        send_options_keyboard = send_options_keyboard_callback(
            options=self.__using_options,
            text=entry_message,
            send_or_edit=send_or_edit_entry_action,
            next_state=self._states.process
        )

        async def __entry_action(query, state):
            self.__get_options()
            await send_options_keyboard(query, state)

        self._entry_action = __entry_action

    def __get_options(self):
        # () return iter
        self.__using_options.clear()
        self.__using_options.extend(self.__options() if callable(self.__options) else self.__options)

    def register(self):
        dp.register_callback_query_handler(
            process_option_selection_callback(option_name=self.__option_name,
                                              options=self.__using_options,
                                              next_state=self._next_state,
                                              next_state_action=self._next_state_action),
            state=self._states.process
        )
