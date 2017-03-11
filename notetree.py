import db

from operator import itemgetter


def build(tag=None, highlight=False):

    notes = db.read_all_notes()
    notes_by_id = _get_notes_by_id(notes)
    _assign_children_notes(notes, notes_by_id)
    _sort_children_notes_chronologically(notes)
    _add_last_modified_human_attribute_to_children_notes(notes)

    if tag:
        matching_notes = _get_notes_with_tag(notes, tag)
        root_notes = _get_root_notes(matching_notes, notes_by_id)
    else:
        root_notes = _get_root_notes(notes, notes_by_id)

    if tag and highlight:
        _set_css_class(notes, "secondary-note")
        _set_css_class(matching_notes, "primary-note")
    else:
        _set_css_class(notes, "primary-note")

    return root_notes

def _get_notes_by_id(notes):
    return {note["note_id"]: note for note in notes}

def _get_root_notes(notes, notes_by_id):
    root_note_ids = set()
    for note in notes:
        root_note_ids.add(_get_root_note_id(note))
    return [notes_by_id[k] for k in root_note_ids]

def _get_notes_with_tag(notes, tag):
    return [note for note in notes if tag in note.items()]

def _set_css_class(notes, css_class):
    for note in notes:
        note["css_class"] = css_class

def _assign_children_notes(notes, notes_by_id):
    for note in notes:
        parent_id = note.get("parent_id")
        if parent_id:
            parent_note = notes_by_id[parent_id]
            parent_note.setdefault("children", []).append(note)

def _sort_children_notes_chronologically(notes):
    for note in notes:
        if "children" in note:
            note["children"] = sorted(
                note["children"],
                key=itemgetter("last_modified"),
                reverse=True,
            )

def _add_last_modified_human_attribute_to_children_notes(notes):
    for note in notes:
        if "parent_id" in note:
            last_modified_human = note["last_modified"].strftime("%b-%d")
            note["last_modified_human"] = last_modified_human

def _get_root_note_id(note):
    if "parent_id" in note:
        return note["parent_id"]
    else:
        return note["note_id"]
