from . import connection

class Room:
  def __init__(self, fid=1, code='', capacity=20, resources={}, rid=None):
    self.fid = fid
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

  @classmethod
  def from_id(cls, fid, rid):
    cursor = connection.cursor()
    cursor.execute('''
      SELECT code, capacity FROM rooms WHERE fid = ? AND rid = ?
    ''', (fid, rid))
    row = cursor.fetchone()

    if row is None:
      return None

    code = row[0]
    capacity = row[1]

    cursor.execute('''
      SELECT type, quantity FROM resources WHERE fid = ? AND rid = ?
    ''', (fid, rid))
    resources = {}
    for r in cursor:
      resources[r[0]] = r[1]

    return cls(fid, code, capacity, resources, rid)
