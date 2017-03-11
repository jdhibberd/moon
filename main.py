import db
import notetree
import os.path
import tornado.ioloop
import uimodules

from htmlutil import deserialize_tags
from parse import parse, to_text
from tornado.web import Application, RequestHandler


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


class ComposeHandler(RequestHandler):

    def get(self):
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
        )

    def post(self):
        # TODO: perhaps rename `message` to `text`
        message = self.get_argument("message")
        tags_argument = self.get_argument("tags")
        tags = deserialize_tags(tags_argument)
        note = parse(message, tags)
        db.write_note(note)
        self.redirect("/")


def make_app():
    handlers = [
        (r"/", TaskHandler),
        (r"/compose", ComposeHandler),
        (r"/people/(.*)", PeopleHandler),
        (r"/projects/(.*)", ProjectsHandler),
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
