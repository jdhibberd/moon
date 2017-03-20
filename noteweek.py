import notetree

from datetime import datetime, timedelta


_WINDOW_DAYS = 7


def build(start_date):
    notes_by_date = _get_notes_by_date(start_date)
    notes_by_date = _format_dates(notes_by_date)
    return notes_by_date


def _get_notes_by_date(start_date):
    notes_by_date = []
    for date in _get_window_dates(start_date):
        notes_by_date.append((
            date,
            notetree.build(tag=("date", date), highlight=True),
        ))
    return notes_by_date


def _get_window_dates(start_date):
    dates = []
    for i in range(_WINDOW_DAYS):
        dates.append((start_date.date() + timedelta(days=i)).isoformat())
    return dates


def _format_dates(notes_by_date):
    def transform(date):
        return datetime.strptime(date, "%Y-%m-%d").strftime("%b-%d")
    return [(transform(date), notes) for date, notes in notes_by_date]
