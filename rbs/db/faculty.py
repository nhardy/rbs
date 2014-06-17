from . import connection
from .room import Room

class Faculty:
  ## Class constructor for Faculty object
  def __init__(self, name, fid=None):
    self.name = name
    self.fid = fid
    
    self._cursor = connection.cursor()

    if self.fid is None:
      self._cursor.execute('''
        INSERT INTO faculties (name)
        VALUES (?)
      ''', (self.name,))
      self.fid = self._cursor.lastrowid
      connection.commit()

  ## Returns a list of Room objects associated with the faculty .get_rooms() is called on
  def get_rooms(self):
    self._cursor.execute('''
      SELECT rid FROM rooms WHERE fid = ?
    ''', (self.fid,))
    return [Room.from_id(self, r[0]) for r in self._cursor]

  ## Property for total number of rooms associated with a faculty
  @property
  def total_rooms(self):
    return self._cursor.execute('''
      SELECT COUNT(*) FROM rooms WHERE fid = ?
    ''', (self.fid,)).fetchone()[0]

  ## Classmethod for returning a Faculty object, given its fid if it exists
  @classmethod
  def from_id(cls, fid):
    cursor = connection.cursor()
    cursor.execute('''
      SELECT name FROM faculties WHERE fid = ?
    ''', (fid,))
    row = cursor.fetchone()

    if row is None:
      return None

    return cls(row[0], fid)

  ## Classmethod for returning a list of all faculties
  @classmethod
  def list(cls):
    faculties = []
    cursor = connection.cursor()
    cursor.execute('''
      SELECT fid FROM faculties
    ''')
    for f in cursor:
      faculties.append(cls.from_id(f[0]))
    return faculties
