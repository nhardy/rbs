from . import connection

class Room:
  def __init__(self, faculty=0, code='', capacity=20, resources={}, rid=None):
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
      ''', (self.faculty, self.code, self.capacity))
      self.rid = self._cursor.lastrowid
      for resource_type, quantity in self.resources:
        self._cursor.execute('''
          INSERT INTO resources (fid, rid, type, quantity)
          VALUES (?, ?, ?, ?)
        ''', (self.faculty, self.rid, resource_type, quantity))
      connection.commit()