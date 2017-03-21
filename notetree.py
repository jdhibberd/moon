import db

from operator import itemgetter


class NoteTree(object):

    def __init__(self, tag=None, highlight=False):
        self._tag = tag
        self._highlight = highlight

    def build(self):

        notes = self._get_notes()
        notes_by_id = self._get_notes_by_id(notes)
        self._assign_children_notes(notes, notes_by_id)
        self._sort_children_notes_chronologically(notes)
        self._add_last_modified_human_attribute_to_children_notes(notes)
        matching_notes = self._get_matching_notes(notes)
        root_notes = self._get_root_notes(matching_notes, notes_by_id)

        if self._highlight:
            self._set_css_class(notes, "secondary-note")
            self._set_css_class(matching_notes, "primary-note")
        else:
            self._set_css_class(notes, "primary-note")

        return root_notes

    def _get_notes(self):
        return db.read_all_notes(query_archive=False)

    def _get_notes_by_id(self, notes):
        return {note["note_id"]: note for note in notes}

    def _get_root_notes(self, notes, notes_by_id):
        root_note_ids = set()
        for note in notes:
            root_note_ids.add(self._get_root_note_id(note))
        return [notes_by_id[k] for k in root_note_ids]

    def _get_notes_with_tag(self, notes, tag):
        return [note for note in notes if tag in note.items()]

    def _set_css_class(self, notes, css_class):
        for note in notes:
            note["css_class"] = css_class

    def _assign_children_notes(self, notes, notes_by_id):
        for note in notes:
            parent_id = note.get("parent_id")
            if parent_id:
                parent_note = notes_by_id[parent_id]
                parent_note.setdefault("children", []).append(note)

    def _sort_children_notes_chronologically(self, notes):
        for note in notes:
            if "children" in note:
                note["children"] = sorted(
                    note["children"],
                    key=itemgetter("last_modified"),
                    reverse=True,
                )

    def _add_last_modified_human_attribute_to_children_notes(self, notes):
        for note in notes:
            if "parent_id" in note:
                last_modified_human = note["last_modified"].strftime("%b-%d")
                note["last_modified_human"] = last_modified_human

    def _get_matching_notes(self, notes):
        if self._tag:
            return self._get_notes_with_tag(notes, self._tag)
        else:
            return notes

    def _get_root_note_id(self, note):
        if "parent_id" in note:
            return note["parent_id"]
        else:
            return note["note_id"]
