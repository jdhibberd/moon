import db

from operator import itemgetter


class NoteTree(object):

    @staticmethod
    def remove_generated_columns(note):
        modified_note = note.copy()
        if "children" in modified_note:
            del modified_note["children"]
        if "css_class" in modified_note:
            del modified_note["css_class"]
        return modified_note

    def __init__(self):
        self._notes = self._read_notes()
        self._get_notes_by_id()
        self._assign_children_notes()
        self._sort_children_notes_chronologically()
        self._set_css_class(self._notes, "primary-note")

    def get_root_notes(self):
        return self._get_root_notes(self._notes)

    def get_note(self, note_id):
        return self._notes_by_id[note_id]

    def _read_notes(self):
        return db.read_all_notes(query_archive=False)

    def _get_notes_by_id(self):
        self._notes_by_id = {note["note_id"]: note for note in self._notes}

    def _assign_children_notes(self):
        for note in self._notes:
            parent_id = note.get("parent_id")
            if parent_id:
                parent_note = self._notes_by_id[parent_id]
                parent_note.setdefault("children", []).append(note)

    def _sort_children_notes_chronologically(self):
        for note in self._notes:
            if "children" in note:
                note["children"] = sorted(
                    note["children"],
                    key=itemgetter("created"),
                    reverse=True,
                )

    def _get_root_notes(self, notes):
        root_note_ids = set()
        for note in notes:
            root_note_ids.add(self._get_root_note_id(note))
        return [self._notes_by_id[k] for k in root_note_ids]

    def _get_root_note_id(self, note):
        if "parent_id" in note:
            return note["parent_id"]
        else:
            return note["note_id"]

    def _set_css_class(self, notes, css_class):
        for note in notes:
            note["css_class"] = css_class
