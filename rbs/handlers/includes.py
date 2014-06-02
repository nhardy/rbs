import tornado.template
from ..db.user import User

template_loader = tornado.template.Loader('./rbs/templates')

def current_user(handler):
  username = handler.get_secure_cookie('username')
  if username is None:
    return None
  return User.from_username(username.decode())