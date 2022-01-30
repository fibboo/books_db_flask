from flask import render_template, request, url_for, flash, redirect

from froms import BookForm
from models import *
from config import app


@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/<int:book_id>')
def book_page(book_id):
    book = Book.query.get(book_id)
    return render_template('book.html', book=book)


@app.route('/add-book', methods=('GET', 'POST'))
def add_book():
    form = BookForm()
    if request.method == 'POST':
        if form.validate():
            book = Book()
            form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            flash('Book added')
            return redirect(url_for('index'))

    return render_template('add_book.html', form=form)


# @app.route('/<int:book_id>/edit', methods=('GET', 'POST'))
# def edit_book(book_id):
#     book = get_book(book_id)
#
#     if request.method == 'POST':
#         if form_is_valid(request.form):
#             db_connection = get_db_connection()
#             db_connection.execute(
#                 'UPDATE books  SET title = ?, number_of_pages = ?, review = ? '
#                 'WHERE id = ?', (request.form['title'],
#                                  request.form['number_of_pages'],
#                                  request.form['review'], book_id)
#             )
#             db_connection.commit()
#             db_connection.close()
#             return redirect(url_for('book_page', book_id=book_id))
#
#     return render_template('edit_book.html', book=book)
#
#
# @app.route('/<int:book_id>/delete', methods=('POST',))
# def delete(book_id):
#     book = get_book(book_id)
#     db_connection = get_db_connection()
#     db_connection.execute('DELETE FROM books WHERE id = ?', (book_id,))
#     db_connection.commit()
#     db_connection.close()
#     flash(f'"{book["title"]}" was successfully deleted!')
#     return redirect(url_for('index'))
