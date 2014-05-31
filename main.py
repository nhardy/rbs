import tornado.ioloop
import tornado.web
import tornado.template
from objects.page import Page

template_loader = tornado.template.Loader('./templates')

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write(template_loader.load('content.html').generate(page=Page('Home',content='<p>Content</p>''')))


handlers = [
  (r'/', MainHandler),
  (r'/styles/(.*)',tornado.web.StaticFileHandler, {'path': './static/styles/'}),
  (r'/images/(.*)',tornado.web.StaticFileHandler, {'path': './static/images/'}),
  (r'/fonts/(.*)',tornado.web.StaticFileHandler, {'path': './static/fonts/'})
]

application = tornado.web.Application(handlers)

if __name__ == '__main__':
  print('Server starting...')
  application.listen(8080)
  tornado.ioloop.IOLoop.instance().start()
  exit()
