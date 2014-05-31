from . import connection
import hashlib, random, string

def password_hash(password, salt):
  return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

class User:
  @classmethod
  def create(cls, username, utype, password):
    cursor = connection.cursor()
    row = cursor.execute('''
      SELECT username FROM users WHERE username = ?
    ''', (username,)).fetchone()
    if row:
      return False

    salt = ''.join([random.choice(string.printable) for _ in range(32)])
    password = password_hash(password, salt)
    cursor.execute('''
      INSERT INTO users (username, utype, password, salt)
      VALUES (?, ?, ?, ?)
    ''', (username, utype, password, salt))
    connection.commit()
    return cls(username, utype, cursor.lastrowid)

  def __init__(self, username, utype, uid):
    self.username = username
    self.utype = utype
    self.uid = uid

    self._cursor = connection.cursor()

  @classmethod
  def login(cls, username, password):
    cursor = connection.cursor()
    row = cursor.execute('''
      SELECT uid, utype, password, salt FROM users WHERE username = ?
    ''', (username,)).fetchone()
    if row is None:
      return False

    if row[2] == password_hash(password, row[3]):
      return cls(username, row[1], row[0])
    else:
      return False

  @classmethod
  def from_username(cls, username):
    cursor = connection.cursor()
    cursor.execute('''
      SELECT username, utype, uid FROM users WHERE username = ?
    ''', (username,))
    row = cursor.fetchone()

    if row is None:
      return None

    return cls(row[0], row[1], row[2])
