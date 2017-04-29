import db
import tornado.web


class Nav(tornado.web.UIModule):

    def render(self, compose_tags):
        people = db.get_distinct_tag_values("people")
        projects = db.get_distinct_tag_values("project")
        return self.render_string(
            "nav.html",
            compose_tags=compose_tags,
            people=people,
            projects=projects,
        )


class Note(tornado.web.UIModule):

    def render(self, note):
        return self.render_string("note.html", note=note)
