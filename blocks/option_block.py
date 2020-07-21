from actions import process_option_selection_callback, send_options_keyboard_callback
from blocks.base_block import BaseBlock
from loader import dp


class OptionBlock(BaseBlock):
    def __init__(self,
                 states_prefix,
                 options,
                 option_name,
                 entry_message,
                 send_or_edit_entry_action=0,
                 next_state=None,
                 next_state_action=None,
                 **next_state_action_kwargs):
        super().__init__(states_prefix,
                         ['choose', 'process'],
                         next_state,
                         next_state_action,
                         **next_state_action_kwargs)
        self.option_name = option_name
        self.options = options
        self.entry_action = send_options_keyboard_callback(
            options=self.options,
            text=entry_message,
            send_or_edit=send_or_edit_entry_action,
            next_state=self.states.process
        )

    def register(self):
        dp.register_callback_query_handler(
            process_option_selection_callback(opt_key=self.option_name,
                                              options=self.options,
                                              next_state=self.next_state,
                                              next_action=self.next_state_action),
            state=self.states.process
        )
