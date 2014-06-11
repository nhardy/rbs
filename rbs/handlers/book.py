import tornado.web
from .includes import template_loader, current_user, round_time
from ..objects.page import Page
from ..db.user import User
from ..db.faculty import Faculty
from ..db.booking import Booking
from datetime import datetime, timedelta

class BookingHandler(tornado.web.RequestHandler):
  def page(self, user, errors=False):
    self.write(template_loader.load('book.html').generate(user=user, faculties=Faculty.list(), page=Page('Booking'), errors=errors))
  def success(self, user, booking):
    self.write(template_loader.load('bookingsuccess.html').generate(user=user, booking=booking, page=Page('Booking Succeeded')))
  def get(self):
    user = current_user(self)
    if not user:
      self.redirect('/')
    else:
      self.page(user, False)
  def post(self):
    errors = []
    user = current_user(self)
    if not user:
      self.redirect('/')
    else:
      try:
        fid = int(self.get_argument('faculty'))
      except ValueError:
        fid = 1
        errors.append('Invalid Faculty ID. (Please report this error as it should not occur under normal circumstances)')
      try:
        capacity = int(self.get_argument('capacity'))
      except ValueError:
        capacity = 1
        errors.append('Invalid Capacity. Please enter a number between 1 and 60.')
      try:
        date = datetime.strptime(self.get_argument('date'), '%Y-%m-%d')
      except ValueError:
        date = datetime.today()
        errors.append('Invalid Date. Your browser should be using \'YYYY-MM-DD\' format.')
      try:
        s = list(map(int,self.get_argument('start_time').split(':')))
        start = date + round_time(timedelta(0, 0, 0, 0, s[1], s[0]))
      except ValueError:
        start = date
        errors.append('Invalid Start Time.')
      try:
        e = list(map(int,self.get_argument('end_time').split(':')))
        end = date + round_time(timedelta(0, 0, 0, 0, e[1], e[0]))
      except ValueError:
        start = date
        errors.append('Invalid End Time.')
      requirements = {} ## TODO

      faculty = Faculty.from_id(fid)
      if faculty is None:
        errors.append('No such faculty with ID: {}.'.format(fid))
      if not (0 < capacity <= 60):
        errors.append('Capacity must be between 1 and 60.')
      if start > end:
        errors.append('Booking may not end before it begins.')

      if errors:
        self.page(user, errors)
      else:
        booking = Booking.attempt_booking(faculty, user, start, end, requirements)
        if not booking:
          self.page(user, ['Unable to make a booking. Is there a conflict or overlap?'])
        else:
          self.success(user, booking)
