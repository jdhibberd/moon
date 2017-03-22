import datetime

from bson.objectid import ObjectId
from config import config
from pymongo import MongoClient


def get_distinct_tag_values(tag):
    query = {"archived": {"$exists": False}}
    return sorted(_get_collection().distinct(tag, query))


def read_all_notes(query_archive):
    notes = []
    if query_archive:
        query = {}
    else:
        query = {"archived": {"$exists": False}}
    for note in _get_collection().find(query):
        notes.append(_decode_primary_key(note))
    return notes


def read_note(note_id):
    note = _get_collection().find_one({'_id': ObjectId(note_id)})
    note = _decode_primary_key(note)
    return note


def write_note(note):
    note = _update_last_modified(note)
    note = _encode_primary_key(note)
    _get_collection().save(note)


def _update_last_modified(note):
    updated_note = note.copy()
    updated_note["last_modified"] = datetime.datetime.utcnow()
    return updated_note


def _get_collection():
    db = config["Storage"]["DB"]
    collection = config["Storage"]["Collection"]
    return MongoClient()[db][collection]


def _encode_primary_key(note):
    encoded_note = note.copy()
    if not is_new_note(note):
        encoded_note["_id"] = note["note_id"]
        del encoded_note["note_id"]
    return encoded_note


def _decode_primary_key(note):
    decoded_note = note.copy()
    decoded_note["note_id"] = note["_id"]
    del decoded_note["_id"]
    return decoded_note


def is_new_note(note):
    return 'note_id' not in note
