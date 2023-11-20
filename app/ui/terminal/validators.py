from datetime import datetime
from typing import Tuple


def get_valid_date(
    date_string: str, date_format="%Y-%m-%d %H:%M:%S"
) -> Tuple[datetime, bool]:
    try:
        date = datetime.strptime(date_string, date_format)
        return date, True
    except ValueError:
        return datetime.now, False
