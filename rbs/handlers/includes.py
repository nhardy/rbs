import tornado.template
from ..db.user import User
from datetime import timedelta

template_loader = tornado.template.Loader('./rbs/templates')

def current_user(handler):
  username = handler.get_secure_cookie('username')
  if username is None:
    return None
  return User.from_username(username.decode())

def round_time(time_delta, increment=300):
  return timedelta(0, int(round(time_delta.total_seconds()/increment)*increment))

def _day(n):
  n = int(n)
  r = n % 10
  return str(n) + 'th' if n in (11,12,13) else ('st' if r == 1 else ('nd' if r == 2 else ('rd' if r == 3 else 'th')))

def format_datetime(datetime):
  return '{}, {} of {}'.format(datetime.strftime('%A'), _day(datetime.strftime('%d')), datetime.strftime('%B, %Y - %I:%M%p'))
