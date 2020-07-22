from itertools import zip_longest

from aiogram.dispatcher.filters.state import default_state

from blocks import BaseBlock


class BranchMeta(type):
    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs)
        cls._blocks = []
        for name, prop in attrs.items():
            if isinstance(prop, BaseBlock):
                cls._blocks.append(prop)
        cls._order()
        cls._register()
        return cls


class BaseBranch(metaclass=BranchMeta):
    @classmethod
    def _order(cls):
        pairs = zip_longest(cls._blocks, cls._blocks[1:])
        for pair in pairs:
            pair[0].next_state = pair[1].entry_state if pair[1] else default_state
            pair[0].next_state_action = pair[1].entry_action if pair[1] else cls.exit_point

    @classmethod
    def _register(cls):
        for block in cls._blocks:
            block.register()
