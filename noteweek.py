from datetime import datetime, timedelta
from filterednotetree import TagFilteredNoteTree


_WINDOW_DAYS = 7


def build(date):
    week_start = (date - timedelta(days=date.weekday())).date()
    notes_by_date = _get_notes_by_date(week_start)
    notes_by_date = _format_dates(notes_by_date)
    return week_start, notes_by_date


def _get_notes_by_date(start_date):
    notes_by_date = []
    for date in _get_window_dates(start_date):
        tree = TagFilteredNoteTree(tag=("date", date), highlight=True)
        notes_by_date.append((
            date,
            tree.get_root_notes(),
        ))
    return notes_by_date


def _get_window_dates(start_date):
    dates = []
    for i in range(_WINDOW_DAYS):
        dates.append((start_date + timedelta(days=i)).isoformat())
    return dates


def _format_dates(notes_by_date):
    def transform(date):
        return datetime.strptime(date, "%Y-%m-%d").date()
    return [(transform(date), notes) for date, notes in notes_by_date]
