import os, sqlite3

main_dir = '../../' if __name__ == '__main__' else './'

create_database = not os.path.exists('{}database.db'.format(main_dir))

connection = sqlite3.connect('{}database.db'.format(main_dir))

if create_database:
  with open('{}db/createDatabase.sql'.format(main_dir)) as schema:
    statements = schema.read().split(';')
  cursor = connection.cursor()
  for s in statements:
    cursor.execute(s)
  connection.commit()