import tornado.web
from .includes import template_loader, current_user
from ..objects.page import Page

class HomeHandler(tornado.web.RequestHandler):
  def get(self):
    user = current_user(self)
    self.write(template_loader.load('content.html').generate(
      user=current_user(self),
      page=Page('Home',content='<p>Welcome, ' + ('Guest' if user is None else user.username) + '!</p>\n' +
      '''<p>This room booking system has been created by Nathan Hardy for the 2014 Software Design and Development Major Project. For instructional information, see the report or the <a href="https://github.com/nhardy/rbs/wiki">GitHub wiki</a></p>''')
    ))