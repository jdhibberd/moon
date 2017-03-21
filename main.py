import db
import notetree
import noteweek
import os.path
import tornado.ioloop
import uimodules

from datetime import datetime
from htmlutil import deserialize_tags
from parse import parse, to_text
from tornado.web import Application, HTTPError, RequestHandler


class TaskHandler(RequestHandler):

    def get(self):
        notes = notetree.build()
        self.render(
            "task.html",
            compose_tags={},
            notes=notes,
        )


class PeopleHandler(RequestHandler):

    def get(self, person):
        notes = notetree.build(tag=("owner", person), highlight=True)
        self.render(
            "task.html",
            compose_tags={"owner": person},
            notes=notes,
        )


class ProjectsHandler(RequestHandler):

    def get(self, project):
        notes = notetree.build(tag=("project", project), highlight=False)
        self.render(
            "task.html",
            compose_tags={"project": project},
            notes=notes,
        )


class TimeHandler(RequestHandler):

    def get(self, start_date):
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPError(400, 'Invalid date.')
        notes_by_date = noteweek.build(start_date)
        self.render(
            "week.html",
            compose_tags={},
            notes_by_date=notes_by_date,
        )


class ComposeHandler(RequestHandler):

    _DEFAULT_REFERER = "/"

    def get(self):
        # TODO: this should accept None too
        tags_argument = self.get_argument("tags", "")
        tags = deserialize_tags(tags_argument)
        note_id = tags.get("note_id")
        if note_id is None:
            text = ''
        else:
            note = db.read_note(note_id)
            text = to_text(note)
        self.render(
            "compose.html",
            compose_tags={},
            text=text,
            tags=tags_argument,
            referer=self.get_argument("referer", self._DEFAULT_REFERER),
        )

    def post(self):
        # TODO: perhaps rename `message` to `text`
        message = self.get_argument("message")
        tags_argument = self.get_argument("tags")
        tags = deserialize_tags(tags_argument)
        note = parse(message, tags)
        db.write_note(note)
        self.redirect(self.get_argument("referer"))


def make_app():
    handlers = [
        (r"/", TaskHandler),
        (r"/compose", ComposeHandler),
        (r"/people/(.*)", PeopleHandler),
        (r"/projects/(.*)", ProjectsHandler),
        (r"/time/(.*)", TimeHandler),
    ]
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        ui_modules=uimodules,
        debug=True,
    )
    return Application(handlers, **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(7000)
    tornado.ioloop.IOLoop.current().start()
