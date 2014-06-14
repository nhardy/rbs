from . import connection
from .faculty import Faculty
from .room import Room
from .user import User
from datetime import datetime
from . import timestamp

class Booking:
  def __init__(self, room, user, stime, etime, requirements={}, bid=None):
    self.room = room
    self.user = user
    self.stime = stime
    self.etime = etime
    self.requirements = requirements
    self.bid = bid

    self._cursor = connection.cursor()

    if self.bid is None:
      self._cursor.execute('''
        INSERT INTO bookings (fid, rid, uid, stime, etime)
        VALUES (?, ?, ?, ?, ?)
      ''', (self.room.faculty.fid, self.room.rid, self.user.uid, timestamp(self.stime), timestamp(self.etime)))
      self.bid = self._cursor.lastrowid
      connection.commit()

  @classmethod
  def from_id(cls, bid):
    cursor = connection.cursor()
    cursor.execute('''
      SELECT fid, rid, uid, stime, etime FROM bookings WHERE bid = ?
    ''', (bid,))
    row = cursor.fetchone()

    if row is None:
      return None

    requirements = {} ## TODO

    faculty = Faculty.from_id(row[0])
    return cls(faculty, Room.from_id(faculty, row[1]), User.from_id(row[2]), datetime.fromtimestamp(row[3]), datetime.fromtimestamp(row[4]), requirements, bid)

  @classmethod
  def attempt_booking(cls, faculty, user, stime, etime, requirements={}):
    for r in faculty.get_rooms():
      if r.is_booked(stime, etime): ## OR not has_requirements()
        continue
      return cls(r, user, stime, etime, requirements)
    return False

  @classmethod
  def get_bookings(cls, faculty, room, user, date, page=1, limit=10):
    cursor = connection.cursor()
    room = None if faculty is None else room
    arguments = tuple([a for a in [None if faculty is None else faculty.fid, None if room is None else room.rid, None if user is None else user.uid, timestamp(date), limit, (page-1)*limit] if a is not None])
    cursor.execute('''
      SELECT bid FROM bookings
      WHERE
    ''' + ((
    '''    fid = ?
          AND
    ''' if faculty is not None else '') + (
    '''
        rid = ?
          AND
    ''' if room is not None else '')) + (
    '''
        uid = ?
          AND
    ''' if user is not None else '') +
    '''
        stime >= ?
      ORDER BY stime ASC
      LIMIT ? OFFSET ?
    ''', arguments)
    return [cls.from_id(int(b[0])) for b in cursor.fetchall()]
