from . import connection
from datetime import datetime
from . import timestamp

class Booking:
  def __init__(self, faculty, room, user, stime, etime, requirements={}, bid=None):
    self.faculty = faculty
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
      ''', (self.faculty.fid, self.room.rid, self.user.uid, timestamp(self.stime), timestamp(self.etime)))
      self.bid = self._cursor.lastrowid
      connection.commit()

  @classmethod
  def from_id(cls, bid):
    cursor = connection.cursor()
    cursor.execute('''
      SELECT (fid, rid, uid, stime, etime) FROM bookings WHERE bid = ?
    ''', (bid,))
    row = cursor.fetchone()

    if row is None:
      return None

    requirements = {} ## TODO

    return cls(Faculty.from_id(row[0]), Room.from_id(row[0], row[1]), User.from_id(row[2]), datetime.fromtimestamp(row[3]), datetime.fromtimestamp(row[4]), requirements, bid)

  @classmethod
  def attempt_booking(cls, faculty, user, stime, etime, requirements={}):
    for r in faculty.get_rooms():
      if r.is_booked(stime, etime): ## OR not has_requirements()
        continue
      return cls(faculty, r, user, stime, etime, requirements)
    return False
