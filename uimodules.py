import db
import tornado.web

from collections import Counter, defaultdict
from filterednotetree import NONE_STRING


class Nav(tornado.web.UIModule):

    def render(self, compose_tags):
        notes = db.read_all_notes(query_archive=False)
        people_counts, people_none_count = self._get_people_counts(notes)
        project_counts, project_none_count = self._get_project_counts(notes)
        return self.render_string(
            "nav.html",
            compose_tags=compose_tags,
            people_counts=people_counts,
            people_none_count=people_none_count,
            project_counts=project_counts,
            project_none_count=project_none_count,
            none_string=NONE_STRING,
        )

    def _get_people_counts(self, notes):
        people_counts = Counter()
        none_count = 0
        for note in notes:
            people = note["people"]
            if people:
                people_counts.update(people)
            else:
                none_count += 1
        return sorted(people_counts.items()), none_count

    def _get_project_counts(self, notes):
        project_counts = defaultdict(int)
        none_count = 0
        for note in notes:
            project = note.get("project")
            if project:
                project_counts[project] += 1
            else:
                none_count += 1
        return sorted(project_counts.items()), none_count


class Note(tornado.web.UIModule):

    def render(self, note):
        return self.render_string("note.html", note=note)
