import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.faculty import Faculty
from ..db.room import Room
from ..db.user import User
from ..db.booking import Booking
from datetime import datetime, date

class BookingsHandler(tornado.web.RequestHandler):
  def page(self, user, bookings=[]):
    self.write(template_loader.load('bookings.html').generate(user=user, bookings=bookings, page=Page('Bookings')))
  def get(self):
    user = current_user(self)
    if not user:
      self.redirect('/')
    else:
      try:
        faculty = Faculty.from_id(int(self.get_argument('fid','')))
      except ValueError:
        faculty = None
      room = None
      if faculty is not None:
        try:
          room = Room.from_id(faculty.fid, int(self.get_argument('rid','')))
        except (ValueError, AttributeError):
          pass
      for_user = user
      if user.utype == 0:
        try:
          for_user = User.from_id(int(self.get_argument('uid','')))
        except ValueError:
          pass

      bookings = Booking.get_bookings(faculty, room, for_user, date.today())

      self.page(user, bookings)
