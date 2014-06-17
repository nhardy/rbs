import tornado.template
from ..db.user import User
from datetime import timedelta

template_loader = tornado.template.Loader('./rbs/templates')

## Function to get current user object from secure cookie
def current_user(handler):
  username = handler.get_secure_cookie('username')
  if username is None:
    return None
  return User.from_username(username.decode())

## Function to round a timedelta to nearest 5 minutes
def round_time(time_delta, increment=300):
  return timedelta(0, int(round(time_delta.total_seconds()/increment)*increment))

## Function to add 'st', 'nd', 'rd', 'th' after day number in month
def _day(n):
  n = int(n)
  r = n % 10
  return str(n) + ('th' if n in (11,12,13) else ('st' if r == 1 else ('nd' if r == 2 else ('rd' if r == 3 else 'th'))))

## FUnction to change a datetime object to English-readable string
def format_datetime(datetime):
  return '{}, {} of {}'.format(datetime.strftime('%A'), _day(datetime.strftime('%d')), datetime.strftime('%B, %Y - %I:%M%p'))

## Function to build a querystring, given keyword arguments
def querystring(**kwargs):
  if any(kwargs.values()):
    return '?' + '&'.join([k + '=' + v for k, v in kwargs.items() if v is not None])
  else:
    return ''
