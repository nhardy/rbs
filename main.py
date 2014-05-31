import tornado.ioloop
import tornado.web
import tornado.template
from objects.page import Page
from db.user import User
import random, string

def current_user(handler):
  username = handler.get_secure_cookie('username')
  if username is None:
    return None
  return User.from_username(username.decode())

template_loader = tornado.template.Loader('./templates')

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write(template_loader.load('content.html').generate(page=Page('Home',content='<p>Username:{}</p>'.format(current_user(self)))))

class LoginHandler(tornado.web.RequestHandler):
  def get(self, errors=False):
    if current_user(self):
      self.redirect('/')
    self.write(template_loader.load('login.html').generate(page=Page('Login'), errors=errors))
  def post(self):
    entered_username = self.get_argument('username')
    entered_password = self.get_argument('password')

    user = User.login(entered_username, entered_password)
    if not user:
      self.get(['Incorrect user or password'])
    self.set_secure_cookie('username', user.username)
    self.redirect('/')

handlers = [
  (r'/', MainHandler),
  (r'/login', LoginHandler),
  (r'/styles/(.*)',tornado.web.StaticFileHandler, {'path': './static/styles/'}),
  (r'/images/(.*)',tornado.web.StaticFileHandler, {'path': './static/images/'}),
  (r'/fonts/(.*)',tornado.web.StaticFileHandler, {'path': './static/fonts/'})
]

application = tornado.web.Application(handlers, cookie_secret=''.join([random.choice(string.printable) for _ in range(63)]))

if __name__ == '__main__':
  print('Server starting...')
  application.listen(8080)
  tornado.ioloop.IOLoop.instance().start()
  exit()
