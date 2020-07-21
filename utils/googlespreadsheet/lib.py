import string

from utils.googlespreadsheet.loader import spreadsheet


class InvalidRangeError(Exception):
    def __init__(self, diapason):
        self.message = "Range %s does't represent one row or column" % diapason


def is_col_or_row(diapason):
    col, row = range(2)
    _from, _to = diapason.split(':')
    if _from[0] == _to[0]:
        return col
    if _from[0] != _to[0] and _from[1] == _to[1]:
        return row
    raise InvalidRangeError(diapason)


def get_options(wks_name, diapason):
    wks = spreadsheet.worksheet(wks_name)
    c_o_r = is_col_or_row(diapason)
    res = wks.get(diapason)
    if not c_o_r:
        return list(map(lambda x: x[0], res))
    return res[0]


def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


def find_first_empty_row(wks, column):
    str_list = list(filter(None, wks.col_values(col2num(column))))
    return str(len(str_list) + 1)


def save_data(data, table):
    fields = table.fields()
    if len(data.keys()) != len(fields):
        raise ValueError('Tables fields and data keys must be equaled')
    wks = spreadsheet.worksheet(table.sheet_name)
    ordered_adr_val = sorted([(field.address, data[field.name]) for field in fields],
                             key=lambda x: (len(x[0]), x[0]))
    ordered_adrs, ordered_vals = zip(*ordered_adr_val)
    first_empty_row = find_first_empty_row(wks, ordered_adrs[0])
    wks.update(f'{ordered_adrs[0]}{first_empty_row}:{ordered_adrs[-1]}{first_empty_row}', [ordered_vals], raw=False)
