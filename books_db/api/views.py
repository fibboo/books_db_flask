from flask import Blueprint, jsonify, make_response, request, abort

from api import serializers
from books.models import Book, Author

api = Blueprint('api', __name__)


@api.route('/api/books', methods=('GET',))
def get_books():
    return jsonify(serializers.books_serializer(Book.query.all()))


@api.route('/api/books/<int:book_id>', methods=('GET',))
def get_book(book_id):
    book = Book.get_or_404(book_id)
    return jsonify(serializers.book_serializer(book))


@api.route('/api/books-without-author', methods=('GET',))
def get_books_without_author():
    books = Book.query.all()
    return jsonify(serializers.books_without_author_serializer(books))


@api.route('/api/books-without-author/<int:book_id>', methods=('GET',))
def get_book_without_author(book_id):
    book = Book.get_or_404(book_id)
    return jsonify(serializers.book_without_author_serializer(book))


# @api.route('/api/books', methods=('POST',))
# def create_book():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     book = Book.create()
#     return jsonify({'task': task}), 201


@api.route('/api/authors', methods=('GET',))
def get_authors():
    authors = Author.query.all()
    return jsonify(serializers.authors_serializer(authors))


@api.route('/api/authors/<int:author_id>', methods=('GET',))
def authors(author_id):
    author = Author.get_or_404(author_id)
    return jsonify(serializers.author_serializer(author))


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
