from rbs.db.user import User
import sqlite3
import re

print('This program will create a new user with admin privelledges.')
print('Please note passwords are not masked.')
print()
while True:
  while True:
    username = input('Enter admin username: ')
    if re.search(r'^[a-z0-9][a-z0-9_.-]{3,28}[a-z0-9]$', username) and not re.search(r'[_.-]{2}', username):
      break
    print('Invalid username. Please try again.')
  while True:
    password = input('Enter desired password for {}: '.format(username))
    if not (8 <= len(password) <= 32):
      print('Invalid password. Must be between 8 and 32 characters.')
      continue
    confirm_password = input('Confirm password for {}: '.format(username))
    if password == confirm_password:
      break
    print('Passwords do not match. Please try again.')

  try:
    admin = User.create(username, 0, password)
    break
  except sqlite3.IntegrityError:
    print('Username taken. Please try again.')
print('User', admin.username, 'successfully created with uid:', admin.uid)
