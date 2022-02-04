from flask import Blueprint, jsonify

from api import serializers
from books.models import Book, Author

api = Blueprint('api', __name__)


@api.route('/api/books', methods=('GET',))
def get_books():
    return jsonify(serializers.books_serializer(Book.query.all()))


@api.route('/api/books-without-author', methods=('GET',))
def book_without_author():
    return jsonify(
        serializers.books_without_author_serializer(Book.query.all())
    )


@api.route('/api/authors', methods=('GET',))
def authors():
    return jsonify(serializers.authors_serializer(Author.query.all()))
