import string


class InvalidRangeError(Exception):
    def __init__(self, diapason):
        self.message = "Range %s does't represent one row or column" % diapason


def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


def find_first_empty_row(wks, column):
    str_list = list(filter(None, wks.col_values(col2num(column))))
    return str(len(str_list) + 1)
