import db
import os.path
import tornado.ioloop
import uimodules

from htmlutil import deserialize_tags
from parse import parse, to_text
from tornado.web import Application, RequestHandler


class MainHandler(RequestHandler):

    def get(self):
        notes = db.find_notes(query={})
        state = self._get_state(notes)
        self.render("task.html", state=state)

    def _get_state(self, notes):

        tasks = []
        for note in notes:
            if "parent_id" not in note:
                tasks.append(note)

        comments = {task["note_id"]:[] for task in tasks}
        for note in notes:
            if "parent_id" in note:
                comments[note["parent_id"]].append(note)

        return dict(
            tasks=tasks,
            comments=comments,
        )

class PeopleHandler(RequestHandler):

    def get(self, user):
        notes = db.find_notes(query={"owner": user})
        state = self._get_state(notes)
        self.render("task.html", state=state)

    def _get_state(self, notes):

        tasks = []
        for note in notes:
            if "parent_id" not in note:
                tasks.append(note)

        comments = {task["note_id"]:[] for task in tasks}
        for note in notes:
            if "parent_id" in note:
                comments[note["parent_id"]].append(note)

        return dict(
            tasks=tasks,
            comments=comments,
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
        self.render("compose.html", text=text, tags=tags_argument)

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
        (r"/", MainHandler),
        (r"/compose", ComposeHandler),
        (r"/people/(.*)", PeopleHandler),
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
