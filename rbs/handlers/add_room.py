import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.faculty import Faculty
from ..db.room import Room
import re
import sqlite3

class AddRoomHandler(tornado.web.RequestHandler):
  def page(self, user, faculty, errors=[]):
    self.write(template_loader.load('addroom.html').generate(user=user, faculty=faculty, errors=errors, page=Page('Add a Room')))
  def success(self, user, room):
    self.write(template_loader.load('addroomsuccess.html').generate(user=user, room=room, page=Page('Room Added')))
  def get(self, fid):
    user = current_user(self)
    if not user or user.utype != 0:
      self.redirect('/')
    else:
      faculty = Faculty.from_id(int(fid))
      if faculty is None:
        raise tornado.web.HTTPError(404)
      else:
        self.page(user, faculty)
  def post(self, fid):
    user = current_user(self)
    if not user or user.utype != 0:
      self.redirect('/')
    else:
      faculty = Faculty.from_id(int(fid))
      if faculty is None:
        raise tornado.web.HTTPError(404)
      else:
        errors = []
        code = self.get_argument('code','')
        if not re.search(r'^[A-Za-z0-9._-]{1,10}$', code):
          errors.append('Invalid room code.')
        try:
          capacity = int(self.get_argument('capacity',''))
        except ValueError:
          capacity = 20
          errors.append('Invalid capacity.')
        if not errors:
          try:
            room = Room(faculty, code, capacity)
          except sqlite3.IntegrityError:
            errors.append('Room code already in use.')
        if errors:
          self.page(user, faculty, errors)
        else:
          self.success(user, room)
