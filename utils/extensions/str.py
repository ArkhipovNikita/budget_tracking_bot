import string


def ascii_letters_range(start: str, end: str):
    start_idnx, end_idnx = string.ascii_letters.index(start), string.ascii_letters.index(end)
    return string.ascii_letters[start_idnx:end_idnx + 1]
