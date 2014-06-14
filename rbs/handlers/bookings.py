import tornado.web
from .includes import template_loader, current_user, format_datetime, querystring
from ..objects.page import Page
from ..db.faculty import Faculty
from ..db.room import Room
from ..db.user import User
from ..db.booking import Booking
from datetime import datetime, date

class BookingsHandler(tornado.web.RequestHandler):
  def page(self, user, bookings=[]):
    self.write(template_loader.load('bookings.html').generate(user=user, bookings=bookings, page=Page('Bookings'), format_datetime=format_datetime))
  def get(self):
    user = current_user(self)
    if not user:
      self.redirect('/')
    else:
      error = False
      faculty = None
      try:
        fid = self.get_argument('fid','')
        if fid != '':
          faculty = Faculty.from_id(int(fid))
          if faculty is None:
            error = True
      except ValueError:
        error = True
      room = None
      rid = self.get_argument('rid','')
      if faculty is None:
        if rid != '':
          error = True
      else:
        try:
          if rid != '':
            room = Room.from_id(faculty, int(rid))
            if room is None:
              error = True
        except ValueError:
          error = True
      for_user = user
      if user.utype == 0:
        try:
          uid = self.get_argument('uid','')
          if uid == '':
            for_user = None
          else:
            for_user = User.from_id(int(uid))
            if for_user is None:
              error = True
        except ValueError:
          for_user = None
          error = True
      if error:
        self.redirect('/bookings{}'.format(querystring(fid=(None if faculty is None else str(faculty.fid)), rid=(None if room is None else str(room.rid)), uid=(None if for_user is None or (for_user == user and user.utype != 0) else str(for_user.uid)))))
      else:
        bookings = Booking.get_bookings(faculty, room, for_user, date.today())
        self.page(user, bookings)
