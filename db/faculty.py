from . import connection

class Faculty:
  def __init__(self, name='', fid=None):
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
