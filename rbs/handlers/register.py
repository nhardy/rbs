import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page
from ..db.user import User
import re

class RegisterHandler(tornado.web.RequestHandler):
  def page(self, errors=False):
    self.write(template_loader.load('register.html').generate(user=None, page=Page('Register'), errors=errors))
  def get(self):
    if current_user(self):
      self.redirect('/')
    self.page(False)
  def post(self):
    desired_username = self.get_argument('username')
    desired_password = self.get_argument('password')
    confirm_password = self.get_argument('confirm_password')

    errors = []
    if not re.search(r'^[a-z0-9][a-z0-9_.-]{3,28}[a-z0-9]$', desired_username) or re.search(r'[_.-]{2}', desired_username):
      errors.append('Your desired username is invalid.')
    elif User.from_username(desired_username) is not None:
      errors.append('Your desired username is already in use.')
    if desired_password != confirm_password:
      errors.append('Entered passwords do not match.')
    elif not (8 <= len(desired_password) <= 32):
      errors.append('Your password is either too long or too short. Please used between 8 and 32 characters, inclusive.')

    if errors:
      self.page(errors)
    else:    
      User.create(desired_username, 1, desired_password)
      user = User.login(desired_username, desired_password)
      self.set_secure_cookie('username', user.username)
      self.redirect('/')