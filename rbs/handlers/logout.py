import tornado.web
from .includes import current_user
from ..objects.page import Page

class LogoutHandler(tornado.web.RequestHandler):
  def get(self):
    self.clear_cookie('username')
    self.redirect('/')