from flask import render_template, request, url_for, flash, redirect, Blueprint

from .froms import *
from .models import *

books_db = Blueprint('book_db', __name__)


@books_db.route('/')
def index():
    books = Book.query.all()
    authors = Author.query.all()
    return render_template('index.html', books=books, authors=authors)


@books_db.route('/books/<int:book_id>')
def book_page(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)


@books_db.route('/authors/<int:author_id>')
def author_page(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('author.html', author=author)


@books_db.route('/add-book', methods=('GET', 'POST'))
def add_book():
    form = BookForm()
    if request.method == 'POST':
        flash(form.errors)
        if form.validate_on_submit():
            book = Book()
            form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            flash('Book added')
            return redirect(url_for('.index'))

    return render_template('add_book.html', form=form)


@books_db.route('/add-author', methods=('GET', 'POST'))
def add_author():
    form = AuthorForm()
    if request.method == 'POST':
        flash(form.errors)
        if 'book_id' in request.values:
            book_id = request.values['book_id']
        else:
            book_id = None
        if form.validate_on_submit():
            author = Author()
            form.populate_obj(author)
            db.session.add(author)
            db.session.commit()
            flash('Author added')
            return redirect(url_for(request.values['return'], book_id=book_id))

    return render_template('add_author.html', form=form)


@books_db.route('/books/<int:book_id>/edit', methods=('GET', 'POST'))
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            flash('Book edited')
            return redirect(url_for('.book_page', book_id=book_id))

    return render_template('edit_book.html', book=book, form=form)


@books_db.route('/authors/<int:author_id>/edit', methods=('GET', 'POST'))
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    form = AuthorForm(obj=author)

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(author)
            db.session.add(author)
            db.session.commit()
            flash('Author edited')
            return redirect(url_for('.book_page', author_id=author_id))

    return render_template('edit_author.html', author=author, form=form)


@books_db.route('/<int:book_id>/delete', methods=('POST',))
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f'"{book.title}" was successfully deleted!')
    return redirect(url_for('.index'))
