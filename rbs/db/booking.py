from . import connection
from datetime import datetime
from . import timestamp

class Booking:
  def __init__(self, fid, rid, user, stime, etime, bid=None):
    self.fid = fid
    self.rid = rid
    self.user = user
    self.stime = stime
    self.etime = etime

    if self.bid is None:
      self._cursor.execute('''
        INSERT INTO bookings (fid, rid, uid, stime, etime)
        VALUES (?, ?, ?, ?, ?)
      ''', (self.fid, self.rid, self.uid, timestamp(self.stime), timestamp(self.etime))
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

    return cls(row[0], row[1], row[2], datetime.fromtimestamp(row[3]), datetime.fromtimestamp(row[4]), bid)

  @classmethod
  def attempt_booking(cls, fid, user, stime, etime, requirements={}):
    cursor = connection.cursor()
    for r in Faculty.from_id(fid).get_rooms():
      pass
