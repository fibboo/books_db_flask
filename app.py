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
    books = db_connection.execute(
        'SELECT * FROM books ORDER BY created DESC'
    ).fetchall()
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


def form_is_valid(form_fields):
    none_fields = []
    for key in form_fields:
        if not form_fields[key]:
            none_fields.append(key)
    if none_fields:
        for field in none_fields:
            flash(f'Field "{field}" is required')
        return False

    return True


@app.route('/add-book', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        if form_is_valid(request.form):
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


@app.route('/<int:book_id>/edit', methods=('GET', 'POST'))
def edit_book(book_id):
    book = get_book(book_id)

    if request.method == 'POST':
        if form_is_valid(request.form):
            db_connection = get_db_connection()
            db_connection.execute(
                'UPDATE books  SET title = ?, number_of_pages = ?, review = ? '
                'WHERE id = ?', (request.form['title'],
                                 request.form['number_of_pages'],
                                 request.form['review'], book_id)
            )
            db_connection.commit()
            db_connection.close()
            return redirect(url_for('book_page', book_id=book_id))

    return render_template('edit_book.html', book=book)


@app.route('/<int:book_id>/delete', methods=('POST',))
def delete(book_id):
    book = get_book(book_id)
    db_connection = get_db_connection()
    db_connection.execute('DELETE FROM books WHERE id = ?', (book_id,))
    db_connection.commit()
    db_connection.close()
    flash(f'"{book["title"]}" was successfully deleted!')
    return redirect(url_for('index'))
