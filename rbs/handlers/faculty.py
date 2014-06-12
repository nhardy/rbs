import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.faculty import Faculty

class FacultyHandler(tornado.web.RequestHandler):
  def page(self, user, rooms=[]):
    self.write(template_loader.load('faculty.html').generate(user=user, rooms=rooms, page=Page('Faculties')))
  def get(self):
    user = current_user(self)
    if not user:
      self.redirect('/')
    else:
      try:
        faculty = Faculty.from_id(int(self.get_argument('fid','')))
      except ValueError:
        faculty = None
      if faculty is None:
        raise tornado.web.HTTPError(404)
      else:
        self.page(user, faculty.get_rooms())
