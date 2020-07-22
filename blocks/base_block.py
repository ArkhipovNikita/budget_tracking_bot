import typing
from abc import ABC, abstractmethod

from aiogram.dispatcher.filters.state import StatesGroup, State, default_state

from utils.extensions import get_obj_attrs


class BaseBlock(ABC):
    def __init__(self,
                 # must be unique within app
                 states_prefix: typing.AnyStr,
                 states: typing.List[typing.AnyStr]):
        self._next_state = default_state
        self._next_state_action = None
        state_group_name = '{}:{}'.format(states_prefix, self.__class__.__name__)
        self._states = type('States', (StatesGroup,), {
            state: State(group_name=state_group_name) for state in states
        })
        self._entry_state = list(filter(lambda x: isinstance(x, State), get_obj_attrs(self._states)))[-1]

    @property
    def entry_state(self):
        return self._entry_state

    @property
    def entry_action(self):
        return self._entry_action

    @property
    def next_state(self):
        return self._next_state

    @next_state.setter
    def next_state(self, value: typing.Union[str, State]):
        self._next_state = value

    @property
    def next_state_action(self):
        return self.next_state_action

    @next_state_action.setter
    def next_state_action(self, value):
        self._next_state_action = value

    @abstractmethod
    def register(self):
        pass
