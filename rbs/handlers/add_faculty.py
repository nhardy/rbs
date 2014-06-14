import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.faculty import Faculty
import re
import sqlite3

class AddFacultyHandler(tornado.web.RequestHandler):
  def page(self, user, errors=[]):
    self.write(template_loader.load('addfaculty.html').generate(user=user, errors=errors, page=Page('Add a Faculty')))
  def success(self, user, faculty):
    self.write(template_loader.load('addfacultysuccess.html').generate(user=user, faculty=faculty, page=Page('Faculty Added')))
  def get(self):
    user = current_user(self)
    if not user or user.utype != 0:
      self.redirect('/')
    else:
      self.page(user)
  def post(self):
    user = current_user(self)
    if not user or user.utype != 0:
      self.redirect('/')
    else:
      errors = []
      fname = self.get_argument('name','')
      if not re.search(r'^[A-Za-z0-9._-]{2,50}$', fname):
        errors.append('Invalid faculty name.')
      if not errors:
        try:
          faculty = Faculty(fname)
        except sqlite3.IntegrityError:
          errors.append('Faculty name already in use.')
      if errors:
        self.page(user, errors)
      else:
        self.success(user, faculty)
