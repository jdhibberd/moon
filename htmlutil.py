import humanize
import tornado.escape
import json


_TASK_URI_TEMPLATE = "https://our.intern.facebook.com/intern/tasks/?t={0}"


def get_task_link(task_number):
    return "&nbsp;<a href=\"{0}\" target=\"_blank\">({1})</a>".format(
        _TASK_URI_TEMPLATE.format(task_number),
        task_number,
    )

# TODO: tags k+v should not include ':' or ',' or '?' or '='

def get_compose_link(label, **kwargs):
    tags = _serialize_tags(kwargs)
    return "<a href=\"/compose?{0}\">{1}</a>".format(
        "tags={0}".format(tags) if tags else "",
        label,
    )

def _serialize_tags(tags):
    return ','.join(["{0}:{1}".format(k, v) for k, v in tags.items()])

def deserialize_tags(tags):
    result = {}
    if tags:
        for pair in tags.split(","):
            k, v = pair.split(":")
            result[k] = v
    return result

def get_last_modified_string(note):
    return humanize.naturalday(note["last_modified"])
