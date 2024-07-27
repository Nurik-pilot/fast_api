from datetime import datetime

from sqlalchemy import Column


def iso_formatted(
    value: Column[datetime] | datetime,
) -> str:
    left = '.'
    right = '+'
    formatted = value.isoformat()
    left_index = formatted.index(left)
    right_index = formatted.index(right)
    microseconds = formatted[left_index:right_index]
    return formatted.replace(
        microseconds,
        microseconds.rstrip('0'),
    )
