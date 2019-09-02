from datetime import datetime, timedelta


def to_first_day_session_if_needed(date: datetime):
    if date.hour < 9 or (date.hour == 9 and date.minute < 30):
        return first_day_session(date)
    return date


def to_last_day_session_if_needed(date: datetime):
    if date.hour > 15:
        return last_day_session(date)
    return date


def to_next_day_session_if_needed(date: datetime):
    if date.hour > 15:
        return next_day(date)
    return date


def to_previous_day_session_if_needed(date: datetime):
    if date.hour < 9 or (date.hour == 9 and date.minute < 30):
        return previous_day(date)
    return date


def first_day_session(date: datetime):
    return datetime(date.year, date.month, date.day, 9, 31, 0)


def last_day_session(date: datetime):
    return datetime(date.year, date.month, date.day, 14, 59, 0)


def next_day(date: datetime):
    date += timedelta(days=1)
    date = datetime(date.year, date.month, date.day, 9, 31, 0)
    return date


def previous_day(date: datetime):
    date -= timedelta(days=1)
    date = datetime(date.year, date.month, date.day, 14, 59, 0)
    return date
