import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.user import User
from ..db.booking import Booking

class BookingsHandler(tornado.web.RequestHandler):
  def page(self, user):
    self.write(template_loader.load('bookings.html').generate(user=user, bookings=[], page=Page('Bookings')))
  def get(self):
    user = current_user(self)
    if not user:
      self.redirect('/')
    else:
      self.page(user)
