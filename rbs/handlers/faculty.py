import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.faculty import Faculty

class FacultyHandler(tornado.web.RequestHandler):
  def page(self, user, faculty):
    self.write(template_loader.load('faculty.html').generate(user=user, faculty=faculty, page=Page('Rooms for {} Faculty'.format(faculty.name))))
  def get(self, fid):
    user = current_user(self)
    if not user:
      self.redirect('/')
    else:
      faculty = Faculty.from_id(int(fid))
      if faculty is None:
        raise tornado.web.HTTPError(404)
      else:
        self.page(user, faculty)
