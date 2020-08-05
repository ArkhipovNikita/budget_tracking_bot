from .loader import spreadsheet
from .helpers import find_first_empty_row
from utils.extensions import get_obj_attrs


def change_fields_addresses(table, addresses):
    fields = table.fields()
    if len(fields) != len(addresses):
        raise ValueError('Amount of fields must equal to amount of addresses.')
    for i, field in enumerate(fields):
        field.address = addresses[i]


class Field:
    def __init__(self, address, name=None):
        self.address = address
        self.name = name
        self.value = None

    def __str__(self):
        return '%s' % self.name


class ModelBase(type):
    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs)

        attr_meta = attrs.pop('Meta', None)
        cls._meta = attr_meta
        if cls.__name__ != 'Model' and not attr_meta:
            raise Exception('Meta class is missing!')
        # range
        if cls.__name__ != 'Model':
            fields = cls._sorted_fields()
            cls._meta.range = f'{fields[0].address}{cls._meta.first_row}:{fields[-1].address}'

        for name, prop in attrs.items():
            if isinstance(prop, Field):
                prop.name = name
        return cls


class Model(metaclass=ModelBase):
    @classmethod
    def fields(cls):
        return list(filter(lambda x: isinstance(x, Field), list(get_obj_attrs(cls))))

    @classmethod
    def _sorted_fields(cls):
        return sorted(cls.fields(), key=lambda x: (len(x.address), x.address))

    @classmethod
    def get_values(cls):
        wks = spreadsheet.worksheet(cls._meta.sheet_name)
        return wks.get(cls._meta.range)

    @classmethod
    def save(cls):
        wks = spreadsheet.worksheet(cls._meta.sheet_name)
        fields = cls._sorted_fields()
        first_empty_row = find_first_empty_row(wks, fields[0].address)
        wks.update(f'{fields[0].address}{first_empty_row}:{fields[-1].address}{first_empty_row}',
                   [list(map(lambda x: x.value, fields))], raw=False)

    @classmethod
    def bind_and_save(cls, values):
        cls._bind(values)
        return cls.save()

    @classmethod
    def _bind(cls, values):
        fields = cls.fields()
        if len(values) != len(list(fields)):
            raise ValueError('Tables fields and data keys must be equaled')
        for field in fields:
            field.value = values[field.name]
