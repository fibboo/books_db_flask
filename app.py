import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


def get_db_connection():
    db_connection = sqlite3.connect('database.db')
    db_connection.row_factory = sqlite3.Row
    return db_connection


@app.route('/')
def index():
    db_connection = get_db_connection()
    books = db_connection.execute('SELECT * FROM books').fetchall()
    db_connection.close()
    return render_template('index.html', books=books)


def get_book(book_id):
    db_connection = get_db_connection()
    book = db_connection.execute('SELECT * FROM books WHERE id = ?',
                                 (book_id,)).fetchone()
    db_connection.close()
    if book is None:
        abort(404)
    return book


@app.route('/<int:book_id>')
def book_page(book_id):
    book = get_book(book_id)
    print(book)
    return render_template('book.html', book=book)


@app.route('/add-book', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        print(request.form)
        for key in request.form:
            if not request.form[key]:
                print(f'not {key}')
                flash(f'{key} is required!')
                break
            else:
                db_connection = get_db_connection()
                db_connection.execute(
                    'INSERT INTO books (title, number_of_pages, review)'
                    'VALUES (?, ?, ?)', (request.form['title'],
                                         request.form['number_of_pages'],
                                         request.form['review'])
                )
                db_connection.commit()
                db_connection.close()
                return redirect(url_for('index'))

    return render_template('add_book.html')
