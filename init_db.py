import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    'INSERT INTO books (title, number_of_pages, review) VALUES (?, ?, ?)',
    ('First Book', 35,
     'It is the first book on this database and it\'s the best')
)

cur.execute(
    'INSERT INTO books (title, number_of_pages, review) VALUES (?, ?, ?)',
    ('Second Book', 353,
     'It is the second book on this database and it\'s almost the best')
)

connection.commit()
connection.close()
