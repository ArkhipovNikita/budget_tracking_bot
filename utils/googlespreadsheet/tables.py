from utils.extensions import get_obj_attrs
from utils.googlespreadsheet import TRANSACTIONS_WKS_NAME


def change_fields_addresses(table, addresses):
    fields = table.fields()
    if len(fields) != len(addresses):
        raise ValueError('Amount of fields must equal to amount of addresses.')
    for i, field in enumerate(fields):
        field.address = addresses[i]


class Field:
    def __init__(self, address):
        self.address = address
        self.name = None


class ModelBase(type):
    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs)
        for name, prop in attrs.items():
            if isinstance(prop, Field):
                prop.name = name
        return cls


class Model(metaclass=ModelBase):
    @classmethod
    def fields(cls):
        return list(filter(lambda x: isinstance(x, Field), list(get_obj_attrs(cls))))


class Expense(Model):
    sheet_name = TRANSACTIONS_WKS_NAME
    date = Field('A')
    category = Field('B')
    description = Field('C')
    sum = Field('D')
    account = Field('E')


class Income(Model):
    sheet_name = TRANSACTIONS_WKS_NAME
    date = Field('F')
    category = Field('G')
    description = Field('H')
    sum = Field('I')
    account = Field('J')
