from flask import render_template, request, url_for, flash, redirect, Blueprint

from books.froms import BookForm, AuthorForm
from books.models import Book, Author
from data import db

books_db = Blueprint('book_db', __name__)


@books_db.route('/')
def index():
    books = Book.query.all()
    authors = Author.query.all()
    return render_template('books/index.html', books=books, authors=authors)


@books_db.route('/books/<int:book_id>')
def book_page(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('books/book.html', book=book)


@books_db.route('/authors/<int:author_id>')
def author_page(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('books/author.html', author=author)


@books_db.route('/add-book', methods=('GET', 'POST'))
def add_book():
    form = BookForm()
    if request.method == 'POST':
        flash(form.errors)
        if form.validate_on_submit():
            book = Book.create(**form.data)
            flash(f'Book "{book.title}" added')
            return redirect(url_for('.index'))

    return render_template('books/add_book.html', form=form)


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
            author = Author.create(**form.data)
            flash(f'Author "{author.fio}" added')
            return redirect(url_for(request.values['return'], book_id=book_id))

    return render_template('books/add_author.html', form=form)


@books_db.route('/books/<int:book_id>/edit', methods=('GET', 'POST'))
def edit_book(book_id):
    book = Book.get_or_404(book_id)
    form = BookForm(obj=book)

    if request.method == 'POST':
        if form.validate_on_submit():
            book.update(**form.data)
            flash(f'Book "{book.title}" edited')
            return redirect(url_for('.book_page', book_id=book_id))

    return render_template('books/edit_book.html', book=book, form=form)


@books_db.route('/authors/<int:author_id>/edit', methods=('GET', 'POST'))
def edit_author(author_id):
    author = Author.get_or_404(author_id)
    form = AuthorForm(obj=author)

    if request.method == 'POST':
        if form.validate_on_submit():
            author.update(**form.data)
            flash(f'Author "{author.fio}" edited')
            return redirect(url_for('.book_page', author_id=author_id))

    return render_template('books/edit_author.html', author=author, form=form)


@books_db.route('/books/<int:book_id>/delete', methods=('POST',))
def book_delete(book_id):
    book = Book.get_or_404(book_id)
    book.delete()
    flash(f'"{book.title}" was successfully deleted!')
    return redirect(url_for('.index'))


@books_db.route('/authors/<int:author_id>/delete', methods=('POST',))
def author_delete(author_id):
    author = Author.get_or_404(author_id)
    author.delete()
    flash(f'"{author.fio}" was successfully deleted!')
    return redirect(url_for('.index'))
