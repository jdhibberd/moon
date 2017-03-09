import db


def build(tag=None):

    notes = db.read_all_notes()
    notes_by_id = _get_notes_by_id(notes)
    _assign_children_notes(notes, notes_by_id)

    if tag:
        matching_notes = _get_notes_with_tag(notes, tag)
        root_notes = _get_root_notes(matching_notes, notes_by_id)
        _set_css_class(notes, "secondary-note")
        _set_css_class(matching_notes, "primary-note")

    else:
        root_notes = _get_root_notes(notes, notes_by_id)
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

def _get_root_note_id(note):
    if "parent_id" in note:
        return note["parent_id"]
    else:
        return note["note_id"]
