from actions import process_option_selection_callback, send_options_keyboard_callback
from blocks.base_block import BaseBlock
from loader import dp


class OptionBlock(BaseBlock):
    def __init__(self,
                 states_prefix,
                 options,
                 option_name,
                 entry_message,
                 send_or_edit_entry_action=0):
        super().__init__(states_prefix, ['choose', 'process'])
        self.__option_name = option_name
        self.__options = options
        self._entry_action = send_options_keyboard_callback(
            options=self.__options,
            text=entry_message,
            send_or_edit=send_or_edit_entry_action,
            next_state=self._states.process
        )

    def register(self):
        dp.register_callback_query_handler(
            process_option_selection_callback(option_name=self.__option_name,
                                              options=self.__options,
                                              next_state=self._next_state,
                                              next_state_action=self._next_state_action),
            state=self._states.process
        )
