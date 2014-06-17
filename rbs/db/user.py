from . import connection
import hashlib, random, string

def password_hash(password, salt):
  return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

class User:
  ## Classmethod for creating new users
  @classmethod
  def create(cls, username, utype, password):
    cursor = connection.cursor()

    ## Check if user already exists
    row = cursor.execute('''
      SELECT username FROM users WHERE username = ?
    ''', (username,)).fetchone()
    if row:
      return False

    ## Salt and Hash Password
    salt = ''.join([random.choice(string.printable) for _ in range(32)])
    password = password_hash(password, salt)

    cursor.execute('''
      INSERT INTO users (username, utype, password, salt)
      VALUES (?, ?, ?, ?)
    ''', (username, utype, password, salt))
    connection.commit()
    return cls(username, utype, cursor.lastrowid)

  ## Class constructor for User object
  def __init__(self, username, utype, uid):
    self.username = username
    self.utype = utype
    self.uid = uid

    self._cursor = connection.cursor()

  ## Classmethod for returning a User object if details are correct
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

  ## Classmethod for returning User object with a given username if exists
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

  ## Classmethod for returning a User object with a given uid if exists
  @classmethod
  def from_id(cls, uid):
    cursor = connection.cursor()
    cursor.execute('''
      SELECT username, utype, uid FROM users WHERE uid = ?
    ''', (uid,))
    row = cursor.fetchone()

    if row is None:
      return None

    return cls(row[0], row[1], row[2])
