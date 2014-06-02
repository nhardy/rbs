import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.user import User

class LoginHandler(tornado.web.RequestHandler):
  def get(self, errors=False):
    if current_user(self):
      self.redirect('/')
    self.write(template_loader.load('login.html').generate(user=None, page=Page('Login'), errors=errors))
  def post(self):
    entered_username = self.get_argument('username')
    entered_password = self.get_argument('password')

    user = User.login(entered_username, entered_password)
    if not user:
      self.get(['Incorrect user or password'])
    self.set_secure_cookie('username', user.username)
    self.redirect('/')