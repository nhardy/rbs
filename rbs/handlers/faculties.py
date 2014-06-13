import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.faculty import Faculty

class FacultiesHandler(tornado.web.RequestHandler):
  def page(self, user, faculties):
    self.write(template_loader.load('faculties.html').generate(user=user, faculties=faculties, page=Page('Faculties')))
  def get(self):
    user = current_user(self)
    if not user:
      self.redirect('/')
    else:
      self.page(user, Faculty.list())
