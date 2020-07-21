import typing
from abc import ABC, abstractmethod

from aiogram.dispatcher.filters.state import StatesGroup, State, default_state

from utils.extensions import get_obj_attrs


class BaseBlock(ABC):
    def __init__(self,
                 states_prefix: typing.AnyStr,
                 states: typing.List[typing.AnyStr],
                 next_state: typing.Union[typing.AnyStr, State] = default_state,
                 next_state_action=None,
                 **next_state_action_kwargs):
        # must be unique within app
        self.states_prefix = states_prefix
        self.next_state = next_state
        self.next_state_action = next_state_action
        self.next_state_action_kwargs = next_state_action_kwargs
        state_group_name = '{}:{}'.format(states_prefix, self.__class__.__name__)
        self.states = type('States', (StatesGroup, ), {
            state: State(group_name=state_group_name) for state in states
        })
        self.entry_state = list(filter(lambda x: isinstance(x, State), get_obj_attrs(self.states)))[-1]

    @abstractmethod
    def register(self):
        pass
