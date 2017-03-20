import parse
import urllib.parse

from config import config


COMPOSE_SYMBOL = "&#9634;"


def serialize_tags(tags):
    return ','.join(["{0}{1}{2}".format(k, parse._TAG_DELIMITER, v) for k, v in tags.items()])


def deserialize_tags(tags):
    result = {}
    if tags:
        for pair in tags.split(","):
            k, v = pair.split(parse._TAG_DELIMITER)
            result[k] = v
    return result


def get_task_link(task_number):
    uri_template = config["Enterprise"]["TaskURITemplate"]
    attributes = {
        "target": "_blank",
        "href": uri_template.format(task_number),
    }
    return _get_html_element_string("a", attributes, task_number)


# TODO: tags k+v should not include ':' or ',' or '?' or '='
# TODO: tag value can't be "null"


def get_compose_link(tags=None, content=COMPOSE_SYMBOL):
    if tags is None:
        tags = []
    tags = serialize_tags(tags)
    query_string = urllib.parse.urlencode({"tags": tags}) if tags else None
    attributes = {
        "class": "compose",
        "href": "/compose" + ("?" + query_string if query_string else ""),
    }
    attributes["class"] = "compose"
    return _get_html_element_string("a", attributes, content)


class ActiveLinkHighlight(object):

    def __init__(self, current_path):
        self._current_path = current_path

    def apply(self, path, label):
        if path == self._current_path:
            return "<b>{0}</b>".format(label)
        else:
            return label


def _get_html_element_string(name, attributes, content):
    return "<{0}{1}>{2}</{0}>".format(
        name,
        ''.join([" {0}=\"{1}\"".format(k, v) for k, v in attributes.items()]),
        content,
    )
