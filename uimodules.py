import db

from tornado.web import UIModule


class Nav(UIModule):

    def render(self):
        people = db.get_distinct_tag_values("owner")
        return self.render_string("nav.html", people=people)
