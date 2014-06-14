import tornado.ioloop
import tornado.web
import tornado.template
from rbs.objects.page import Page
from rbs.db.user import User
from rbs.handlers.home import HomeHandler
from rbs.handlers.login import LoginHandler
from rbs.handlers.register import RegisterHandler
from rbs.handlers.book import BookingHandler
from rbs.handlers.bookings import BookingsHandler
from rbs.handlers.faculties import FacultiesHandler
from rbs.handlers.faculty import FacultyHandler
from rbs.handlers.add_faculty import AddFacultyHandler
from rbs.handlers.add_room import AddRoomHandler
from rbs.handlers.logout import LogoutHandler
from rbs.handlers.includes import template_loader, current_user
import random, string

import os
import tornado.autoreload

handlers = [
  (r'/', HomeHandler),
  (r'/login', LoginHandler),
  (r'/register', RegisterHandler),
  (r'/book', BookingHandler),
  (r'/bookings', BookingsHandler),
  (r'/faculties', FacultiesHandler),
  (r'/faculties/([0-9]+)', FacultyHandler),
  (r'/faculties/add', AddFacultyHandler),
  (r'/faculties/([0-9]+)/add', AddRoomHandler),
  (r'/logout', LogoutHandler),
  (r'/styles/(.*)',tornado.web.StaticFileHandler, {'path': './rbs/static/styles/'}),
  (r'/images/(.*)',tornado.web.StaticFileHandler, {'path': './rbs/static/images/'}),
  (r'/fonts/(.*)',tornado.web.StaticFileHandler, {'path': './rbs/static/fonts/'})
]

application = tornado.web.Application(handlers, cookie_secret=''.join([random.choice(string.printable) for _ in range(63)]), debug=True)

if __name__ == '__main__':
  print('Server starting...')
  application.listen(8080)

  for (dir_path, _, files) in os.walk('./rbs/templates/'):
    for f in files:
      tornado.autoreload.watch(os.path.join(dir_path, f))
    break
  
  tornado.ioloop.IOLoop.instance().start()
  exit()
