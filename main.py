import db
import noteweek
import os.path
import tornado.ioloop
import uimodules

from bson.objectid import ObjectId
from datetime import datetime
from filterednotetree import TagFilteredNoteTree
from htmlutil import deserialize_tags
from notearchive import ArchiveNoteTree
from notetree import NoteTree
from parse import deserialize, serialize
from tornado.web import Application, HTTPError, RequestHandler


class TaskHandler(RequestHandler):

    def get(self):
        notes = NoteTree().get_root_notes()
        self.render(
            "task.html",
            compose_tags={},
            notes=notes,
        )


class PeopleHandler(RequestHandler):

    def get(self, person):
        tree = TagFilteredNoteTree(tag=("owner", person), highlight=True)
        self.render(
            "task.html",
            compose_tags={"owner": person},
            notes=tree.get_root_notes(),
        )


class ProjectsHandler(RequestHandler):

    def get(self, project):
        tree = TagFilteredNoteTree(tag=("project", project), highlight=False)
        self.render(
            "task.html",
            compose_tags={"project": project},
            notes=tree.get_root_notes(),
        )


class TimeHandler(RequestHandler):

    def get(self, date):
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPError(400, 'Invalid date.')
        week_start, notes_by_date = noteweek.build(date)
        self.render(
            "week.html",
            compose_tags={},
            week_start=week_start,
            notes_by_date=notes_by_date,
        )


class ComposeHandler(RequestHandler):

    _DEFAULT_REFERER = "/"

    def get(self):
        # TODO: this should accept None too
        tags_string = self.get_argument("tags", "")
        tags = deserialize_tags(tags_string)
        note_id = tags.get("note_id")
        if note_id is None:
            note = None
            text = ''
        else:
            note = db.read_note(note_id)
            text = serialize(note)
        self.render(
            "compose.html",
            compose_tags={},
            text=text,
            tags_string=tags_string,
            note=note,
            referer=self._get_referer(),
        )

    def _get_referer(self):
        referer = self.get_argument("referer", None)
        if referer in {self.request.path, None}:
            referer = self._DEFAULT_REFERER
        return referer

    def post(self):
        # TODO: perhaps rename `message` to `text`
        message = self.get_argument("message")
        tags_argument = self.get_argument("tags")
        tags = deserialize_tags(tags_argument)
        note = deserialize(message, tags)
        db.write_note(note)
        self.redirect(self.get_argument("referer"))


class ArchiveViewHandler(RequestHandler):

    def get(self):
        tree = ArchiveNoteTree()
        self.render(
            "archive.html",
            compose_tags={},
            notes_by_date=tree.get_notes_by_date(),
        )


class ArchiveActionHandler(RequestHandler):

    def post(self, note_id):
        note_id = ObjectId(note_id)
        note_tree = NoteTree()
        note = note_tree.get_note(note_id)
        self._archive(note, note_tree)

    def _archive(self, note, note_tree):
        for child in note.get("children", []):
            self._archive(child, note_tree)
        if "archived" in note:
            return
        note["archived"] = datetime.utcnow()
        modified_note = NoteTree.remove_generated_columns(note)
        db.write_note(modified_note)


class UnarchiveActionHandler(RequestHandler):

    def post(self, note_id):
        self._unarchive(note_id)

    def _unarchive(self, note_id):
        note = db.read_note(note_id)
        if "archived" in note:
            del note["archived"]
            modified_note = NoteTree.remove_generated_columns(note)
            db.write_note(modified_note)
        parent_id = note.get("parent_id")
        if parent_id:
            self._unarchive(parent_id)


def make_app():
    handlers = [
        (r"/", TaskHandler),
        (r"/compose", ComposeHandler),
        (r"/people/(.*)", PeopleHandler),
        (r"/projects/(.*)", ProjectsHandler),
        (r"/time/(.*)", TimeHandler),
        (r"/archive", ArchiveViewHandler),
        (r"/notes/([0-9a-f]+)/archive", ArchiveActionHandler),
        (r"/notes/([0-9a-f]+)/unarchive", UnarchiveActionHandler),
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
