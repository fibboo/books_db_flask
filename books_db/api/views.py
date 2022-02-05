from flask import Blueprint, jsonify, make_response, request, abort

from api import serializers
from api import validators
from books.models import Book, Author
from users.models import User

api = Blueprint('api', __name__)


@api.route('/api/books', methods=('GET',))
def get_books():
    no_author = request.values.get('no_author')
    books = Book.query.all()
    serialized_data = [serializers.book_serializer(obj, no_author)
                       for obj in books]
    return jsonify(serialized_data)


@api.route('/api/books/<int:book_id>', methods=('GET',))
def get_book(book_id):
    no_author = request.values.get('no_author')
    book = Book.get_or_404(book_id)
    return jsonify(serializers.book_serializer(book, no_author))


@api.route('/api/books', methods=('POST',))
def create_book():
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    book = Book.create(
        owner=User.get_or_404(1),
        **validators.book_validator(request.json)
    )
    return jsonify(serializers.book_serializer(book)), 201


@api.route('/api/books/<int:book_id>', methods=('PUT',))
def update_book(book_id):
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    book = Book.get_or_404(book_id)
    book.update(**validators.book_validator(request.json, True, book))
    return jsonify(serializers.book_serializer(book)), 201


@api.route('/api/books/<int:book_id>', methods=('DELETE',))
def delete_book(book_id):
    book = Book.get_or_404(book_id)
    book.delete()
    return make_response(
        jsonify(message=f"Book '{book.title}' has been deleted"), 404
    )


@api.route('/api/authors', methods=('GET',))
def get_authors():
    authors = Author.query.all()
    return jsonify(serializers.authors_serializer(authors))


@api.route('/api/authors/<int:author_id>', methods=('GET',))
def authors(author_id):
    author = Author.get_or_404(author_id)
    return jsonify(serializers.author_serializer(author))


@api.route('/api/authors', methods=('POST',))
def create_author():
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    author = Author.create(
        owner=User.get_or_404(1), **validators.author_validator(request.json)
    )
    return jsonify(serializers.author_serializer(author)), 201


@api.route('/api/authors/<int:author_id>', methods=('PUT',))
def update_author(author_id):
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    author = Author.get_or_404(author_id)
    author.update(**validators.author_validator(request.json, True, author))
    return jsonify(serializers.author_serializer(author)), 201


@api.route('/api/authors/<int:author_id>', methods=('DELETE',))
def delete_author(author_id):
    author = Author.get_or_404(author_id)
    author.delete()
    return make_response(
        jsonify(message=f"Author '{author.fio}' has been deleted"), 404
    )


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
