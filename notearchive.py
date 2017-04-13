import db

from collections import defaultdict
from filterednotetree import FilteredNoteTree


class ArchiveNoteTree(FilteredNoteTree):

    def __init__(self):
        super().__init__(highlight=True)

    def get_notes_by_date(self):
        notes_by_date = defaultdict(list)
        for note in super().get_root_notes():
            archived_date = self._get_most_recent_recursive_archived_date(note)
            notes_by_date[archived_date.date()].append(note)
        return sorted(notes_by_date.items(), reverse=True)

    def _read_notes(self):
        return db.read_all_notes(query_archive=True)

    def _get_matching_notes(self):
        return [note for note in self._notes if "archived" in note]

    def _get_most_recent_recursive_archived_date(self, note):

        def compare(current, candidate):
            if candidate is None:
                return current
            if current is None:
                return candidate
            if candidate > current:
                return candidate
            else:
                return current

        archived_date = compare(None, note.get("archived"))
        for subnote in note.get("children", []):
            archived_date = compare(archived_date, subnote.get("archived"))
        return archived_date
