from .constants import TRANSACTIONS_WKS_NAME, CATEGORIES_WKS_NAME, ACCOUNTS_WKS_NAME, DEBT_WKS_NAME
from .base_model import Field, Model


class Expense(Model):
    class Meta:
        sheet_name = TRANSACTIONS_WKS_NAME
        first_row = 3

    date = Field('A')
    category = Field('B')
    description = Field('C')
    amount = Field('D')
    account = Field('E')


class Income(Model):
    class Meta:
        sheet_name = TRANSACTIONS_WKS_NAME
        first_row = 3

    date = Field('F')
    category = Field('G')
    description = Field('H')
    amount = Field('I')
    account = Field('J')


class ExpenseCategory(Model):
    class Meta:
        sheet_name = CATEGORIES_WKS_NAME
        first_row = 3

    category = Field('A')
    group = Field('B')

    @classmethod
    def get_categories(cls):
        return map(lambda x: x[0], super().get_values())


class IncomeCategory(Model):
    class Meta:
        sheet_name = CATEGORIES_WKS_NAME
        first_row = 3

    category = Field('C')
    group = Field('D')

    # отелить модель и способ получения данных, чтобы копирования не было
    @classmethod
    def get_categories(cls):
        return map(lambda x: x[0], super().get_values())


class Account(Model):
    class Meta:
        sheet_name = ACCOUNTS_WKS_NAME
        first_row = 2

    name = Field('F')

    @classmethod
    def get_account_names(cls):
        return map(lambda x: x[0], super().get_values())


class DebtLoss(Model):
    class Meta:
        sheet_name = DEBT_WKS_NAME
        first_row = 3

    date = Field('A')
    who = Field('B')
    amount = Field('C')
    description = Field('D')
    account = Field('E')


class DebtRefund(Model):
    class Meta:
        sheet_name = DEBT_WKS_NAME
        first_row = 3

    date = Field('F')
    who = Field('G')
    amount = Field('H')
    description = Field('I')
    account = Field('J')


class Transfer(Model):
    class Meta:
        sheet_name = TRANSACTIONS_WKS_NAME
        first_row = 3

    date = Field('K')
    from_account = Field('L')
    amount = Field('M')
    exchange_rate = Field('N')
    to_account = Field('O')
    description = Field('P')
