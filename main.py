import tornado.ioloop
import tornado.web
import tornado.template
from rbs.objects.page import Page
from rbs.db.user import User
from rbs.handlers.login import LoginHandler
from rbs.handlers.includes import template_loader, current_user
import random, string

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write(template_loader.load('content.html').generate(page=Page('Home',content='<p>Username:{}</p>'.format(current_user(self)))))

handlers = [
  (r'/', MainHandler),
  (r'/login', LoginHandler),
  (r'/styles/(.*)',tornado.web.StaticFileHandler, {'path': './rbs/static/styles/'}),
  (r'/images/(.*)',tornado.web.StaticFileHandler, {'path': './rbs/static/images/'}),
  (r'/fonts/(.*)',tornado.web.StaticFileHandler, {'path': './rbs/static/fonts/'})
]

application = tornado.web.Application(handlers, cookie_secret=''.join([random.choice(string.printable) for _ in range(63)]))

if __name__ == '__main__':
  print('Server starting...')
  application.listen(8080)
  tornado.ioloop.IOLoop.instance().start()
  exit()
