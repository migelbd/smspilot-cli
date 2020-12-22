from typing import Union


def get_row_data(item, fields_data: Union[list, tuple]) -> list:
    row = []
    for attr in fields_data:
        value = '-'
        if hasattr(item, attr):
            value = getattr(item, attr)
            if callable(value):
                value = value()
        row.append(str(value))
    return row
