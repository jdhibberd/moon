import db

from collections import defaultdict
from notetree import NoteTree


class ArchiveNoteTree(NoteTree):

    def build(self):
        notes_by_date = defaultdict(list)
        for note in super().build():
            archived_date = self._get_most_recent_recursive_archived_date(note)
            notes_by_date[archived_date.date()].append(note)
        return notes_by_date.items()

    def _get_notes(self):
        return db.read_all_notes(query_archive=True)

    def _get_matching_notes(self, notes):
        return [note for note in notes if "archived" in note]

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
