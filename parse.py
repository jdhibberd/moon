from bson.objectid import ObjectId

_DEFAULT_VALUE = 1
_TAG_DELIMITER = "."
_TEXT_DELIMITER = "//"



# TODO: pass in tags to automatically be added?
def parse(text, tags):
    note = tags.copy()
    i = text.rfind(_TEXT_DELIMITER)
    if i == -1:
        note["message"] = text.rstrip()
    else:
        note["message"] = text[:i].rstrip()
        attributes = text[i + len(_TEXT_DELIMITER):].lstrip()
        for attr in attributes.split():
            if _TAG_DELIMITER in attr:
                k, v = attr.split(_TAG_DELIMITER, maxsplit=1)
            else:
                k, v = attr, _DEFAULT_VALUE
            note[k] = v
    return note

# TODO: there should be a list of system fields
def to_text(note):
    string_buffer = [note["message"]]
    if len(note.keys()) > 3:  # id and message
        string_buffer.append(" {0}".format(_TEXT_DELIMITER))
        for k in note.keys():
            if k in {"message", "note_id", "last_modified"}:
                continue
            string_buffer.append(" {0}".format(k))
            value = note[k]
            if value is not None:
                string_buffer.append("{0}{1}".format(_TAG_DELIMITER, value))
    return ''.join(string_buffer)
