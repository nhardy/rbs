from . import connection

class User:
  def __init__(self, username, utype=1, uid=None):
    self.username = username
    self.utype = utype
    self.uid = uid

    self._cursor = connection.cursor()

    if self.uid is None:
      self._cursor.execute('''
        INSERT INTO users (username, utype)
        VALUES (?, ?)
      ''', (self.username, self.utype))
      self.uid = self._cursor.lastrowid
      connection.commit()
