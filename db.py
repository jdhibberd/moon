import datetime

from bson.objectid import ObjectId
from pymongo import MongoClient


def get_distinct_tag_values(tag):
    return _get_collection().distinct(tag)

def find_notes(query):
    notes = []
    for note in _get_collection().find(query):
        notes.append(_decode_objectids(note))
    return notes

def read_note(note_id):
    note = _get_collection().find_one({'_id': ObjectId(note_id)})
    note = _decode_objectids(note)
    return note

def write_note(note):
    note = _update_last_modified(note)
    note = _encode_objectids(note)
    _get_collection().save(note)

def _update_last_modified(note):
    updated_note = note.copy()
    updated_note["last_modified"] = datetime.datetime.utcnow()
    return updated_note

# TODO: abstract this to config file
def _get_collection():
    return MongoClient().chuliwenti.note

def _encode_objectids(note):
    encoded_note = note.copy()
    if not is_new_note(note):
        encoded_note["_id"] = ObjectId(note["note_id"])
        del encoded_note["note_id"]
    if "parent_id" in note:
        encoded_note["parent_id"] = ObjectId(note["parent_id"])
    return encoded_note

def _decode_objectids(note):
    decoded_note = note.copy()
    decoded_note["note_id"] = str(note["_id"])
    del decoded_note["_id"]
    if "parent_id" in note:
        decoded_note["parent_id"] = str(note["parent_id"])
    return decoded_note

def is_new_note(note):
    return 'note_id' not in note
