from . import connection
from . import timestamp

class Room:
  def __init__(self, faculty, code, capacity, resources={}, rid=None):
    self.faculty = faculty
    self.code = code
    self.capacity = capacity
    self.resources = resources
    self.rid = rid

    self._cursor = connection.cursor()

    if self.rid is None:
      self._cursor.execute('''
        INSERT INTO rooms (fid, code, capacity)
        VALUES (?, ?, ?)
      ''', (self.faculty.fid, self.code, self.capacity))
      self.rid = self._cursor.lastrowid
      for resource_type, quantity in self.resources:
        self._cursor.execute('''
          INSERT INTO resources (fid, rid, type, quantity)
          VALUES (?, ?, ?, ?)
        ''', (self.faculty.fid, self.rid, resource_type, quantity))
      connection.commit()

  def is_booked(self, stime, etime):
    self._cursor.execute('''
      SELECT COUNT(*) FROM bookings
      WHERE
        fid = ? AND
        rid = ? AND
        (
          (? >= stime AND ? < etime)
          OR
          (? > stime AND ? <= etime)
        )
    ''', (self.faculty.fid, self.rid, timestamp(stime), timestamp(stime), timestamp(etime), timestamp(etime)))

    if self._cursor.fetchone()[0] > 0:
      return True

  def has_requirements(self, capacity, requirements):
    return False if capacity > self.capacity else False if any([self.resources[req] < num for req, num in requirements.items()]) else True

  @classmethod
  def from_id(cls, faculty, rid):
    from .faculty import Faculty
    cursor = connection.cursor()
    cursor.execute('''
      SELECT code, capacity FROM rooms WHERE fid = ? AND rid = ?
    ''', (faculty.fid, rid))
    row = cursor.fetchone()

    if row is None:
      return None

    code = row[0]
    capacity = row[1]

    cursor.execute('''
      SELECT type, quantity FROM resources WHERE fid = ? AND rid = ?
    ''', (faculty.fid, rid))
    resources = {}
    for r in cursor:
      resources[r[0]] = r[1]

    return cls(Faculty.from_id(faculty.fid), code, capacity, resources, rid)
