import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.user import User

class LoginHandler(tornado.web.RequestHandler):
  def page(self, errors=False):
    self.write(template_loader.load('login.html').generate(user=None, page=Page('Login'), errors=errors))
  def get(self):
    if current_user(self):
      self.redirect('/')
    self.page(False)
  def post(self):
    entered_username = self.get_argument('username')
    entered_password = self.get_argument('password')

    user = User.login(entered_username, entered_password)
    if not user:
      self.page(['Incorrect user or password'])
    else:
      self.set_secure_cookie('username', user.username)
      self.redirect('/')