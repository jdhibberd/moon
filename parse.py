import datetime

from bson.objectid import ObjectId


_DEFAULT_VALUE = 1
_TAG_DELIMITER = "."
_TEXT_DELIMITER = "**"


# TODO: there should be a list of system fields
def serialize(note):
    string_buffer = [note["message"]]
    if len(note.keys()) > 3:  # id and message
        string_buffer.append(" {0}".format(_TEXT_DELIMITER))
        for k in note.keys():
            if k in {"message", "note_id", "last_modified"}:
                continue
            string_buffer.append(" {0}".format(k))
            v = note[k]
            v_serialized = _serialize_tag_value(k, v)
            if v is not None:
                string_buffer.append(
                    "{0}{1}".format(_TAG_DELIMITER, v_serialized),
                )
    return ''.join(string_buffer)


def deserialize(text, tags):
    note = tags.copy()
    i = text.rfind(_TEXT_DELIMITER)
    if i == -1:
        note["message"] = text.rstrip()
    else:
        note["message"] = text[:i].rstrip()
        attributes = text[i + len(_TEXT_DELIMITER):].lstrip()
        for attribute in attributes.split():
            k, v = _split_attribute(attribute)
            v_deserialized = _deserialize_tag_value(k, v)
            note[k] = v_deserialized
    if "created" not in note:
        note["created"] = datetime.datetime.utcnow()
    return note


def _split_attribute(attribute):
    if _TAG_DELIMITER in attribute:
        k, v = attribute.split(_TAG_DELIMITER, maxsplit=1)
    else:
        k, v = attribute, _DEFAULT_VALUE
    return k, v


def _serialize_tag_value(k, v):
    f = _SERIALIZE_TAG_MAP.get(k)
    return f(v) if f else v


def _deserialize_tag_value(k, v):
    f = _DESERIALIZE_TAG_MAP.get(k)
    return f(v) if f else v


def _serialize_date(v):
    return v.date().isoformat()


def _deserialize_date(v):
    return datetime.datetime.strptime(v, "%Y-%m-%d")


def _serialize_id(v):
    return str(v)


def _deserialize_id(v):
    return ObjectId(v)


_DESERIALIZE_TAG_MAP = {
    "archived": _deserialize_date,
    "created": _deserialize_date,
    "node_id": _deserialize_id,
    "parent_id": _deserialize_id,
}
_SERIALIZE_TAG_MAP = {
    "archived": _serialize_date,
    "created": _serialize_date,
    "node_id": _serialize_id,
    "parent_id": _serialize_id,
}
