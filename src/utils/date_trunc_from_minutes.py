from datetime import datetime


def date_trunc_from_minutes(datetime: datetime) -> str:
    return datetime.strftime("%Y/%m/%d %H:%M:00.000")
