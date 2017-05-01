from notetree import NoteTree


NONE_STRING = "none"


class FilteredNoteTree(NoteTree):

    def __init__(self, highlight=False):
        super().__init__()
        self._matching_notes = self._get_matching_notes()
        if highlight:
            self._set_css_class(self._notes, "secondary-note")
            self._set_css_class(self._matching_notes, "primary-note")

    def get_root_notes(self):
        return self._get_root_notes(self._matching_notes)

    def _get_matching_notes(self):
        raise NotImplementedError


class TagFilteredNoteTree(FilteredNoteTree):

    def __init__(self, tag, highlight):
        self._tag = tag
        super().__init__(highlight)

    def _get_matching_notes(self):
        tag_key, tag_value = self._tag
        if tag_value == NONE_STRING:
            return [
                note for note in self._notes if tag_key not in note
            ]
        else:
            return [
                note for note in self._notes if self._tag in note.items()
            ]


class PeopleFilteredNoteTree(FilteredNoteTree):

    def __init__(self, person):
        self._person = person
        super().__init__(highlight=True)

    def _get_matching_notes(self):
        if self._person == NONE_STRING:
            return [
                note for note in self._notes if not note["people"]
            ]
        else:
            return [
                note for note in self._notes if self._person in note["people"]
            ]
