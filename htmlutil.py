import datetime
import parse
import re
import urllib.parse

from config import config


COMPOSE_SYMBOL = "&#9634;"


def serialize_tags(tags):
    if tags is None:
        return None
    return ','.join(["{0}{1}{2}".format(k, parse._TAG_DELIMITER, v) for k, v in tags.items()])


def deserialize_tags(tags):
    result = {}
    if tags:
        for pair in tags.split(","):
            k, v = pair.split(parse._TAG_DELIMITER)
            result[k] = v
    return result



def serialize_people(people):
    return ','.join(people)


def deserialize_people(people):
    people = people.strip()
    if people:
        return people.split(",")
    else:
        return []


def get_task_link(task_number):
    uri_template = config["Enterprise"]["TaskURITemplate"]
    attributes = {
        "target": "_blank",
        "href": uri_template.format(task_number),
    }
    return _get_html_element_string("a", attributes, "t" + task_number)


def get_quip_link(quip_id):
    uri_template = config["Enterprise"]["QuipURITemplate"]
    attributes = {
        "target": "_blank",
        "href": uri_template.format(quip_id),
    }
    return _get_html_element_string("a", attributes, "Quip")


def get_week_link(content, day):
    week_start = day - datetime.timedelta(days=day.weekday())
    attributes = {
        "href": "/time/" + week_start.isoformat(),
    }
    return _get_html_element_string("a", attributes, content)

# TODO: tags k+v should not include ':' or ',' or '?' or '='
# TODO: tag value can't be "null"


def get_compose_link(tags=None, content=COMPOSE_SYMBOL, referer=None):
    tags = serialize_tags(tags)
    args = {"tags": tags, "referer": referer}
    query_string = urllib.parse.urlencode({k: v for k, v in args.items() if v})
    attributes = {
        "class": "compose",
        "href": "/compose" + ("?" + query_string if query_string else ""),
    }
    attributes["class"] = "compose"
    return _get_html_element_string("a", attributes, content)


class ActiveLinkHighlight(object):

    def __init__(self, current_path):
        self._current_path = current_path

    def apply(self, path_pattern, label):
        if re.match(path_pattern, self._current_path):
            return "<b>{0}</b>".format(label)
        else:
            return label


def _get_html_element_string(name, attributes, content):
    return "<{0}{1}>{2}</{0}>".format(
        name,
        ''.join([" {0}=\"{1}\"".format(k, v) for k, v in attributes.items()]),
        content,
    )


def format_datetime(date):
    return date.strftime("%b-%d")


def format_week_date(date):
    formatted_date = format_datetime(date) + date.strftime(", %a")
    if date == datetime.date.today():
        formatted_date = "<b>{0}</b>".format(formatted_date)
    return formatted_date
