from flask import Blueprint, jsonify, make_response, request, abort
from flask_jwt import jwt_required, current_identity

from api import serializers
from api import validators

from api.permissions import check_object_permission, check_self_permission
from books.models import Book, Author
from users.models import User

api = Blueprint('api', __name__)


@api.route('/api/books', methods=('GET',))
def get_books():
    with_author = request.values.get('with_author')
    books = Book.query.all()
    serialized_data = [serializers.book_serializer(obj, with_author)
                       for obj in books]
    return jsonify(serialized_data)


@api.route('/api/books/<int:book_id>', methods=('GET',))
def get_book(book_id):
    no_author = request.values.get('no_author')
    book = Book.get_or_404(book_id)
    return jsonify(serializers.book_serializer(book, no_author))


@api.route('/api/books', methods=('POST',))
@jwt_required()
def create_book():
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    book = Book.create(
        owner=current_identity,
        **validators.book_validator(request.json)
    )
    return jsonify(serializers.book_serializer(book, True)), 201


@api.route('/api/books/<int:book_id>', methods=('PUT',))
@jwt_required()
def update_book(book_id):
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    book = Book.get_or_404(book_id)
    check_object_permission(current_identity, book)
    book.update(**validators.book_validator(request.json, True, book))
    return jsonify(serializers.book_serializer(book)), 201


@api.route('/api/books/<int:book_id>', methods=('DELETE',))
@jwt_required()
def delete_book(book_id):
    book = Book.get_or_404(book_id)
    check_object_permission(current_identity, book)
    book.delete()
    return make_response(
        jsonify(message=f"Book '{book.title}' has been deleted"), 204
    )


@api.route('/api/authors', methods=('GET',))
def get_authors():
    authors = Author.query.all()
    serialized_data = [serializers.author_serializer(obj)
                       for obj in authors]
    return jsonify(serialized_data)


@api.route('/api/authors/<int:author_id>', methods=('GET',))
def get_author(author_id):
    author = Author.get_or_404(author_id)
    return jsonify(serializers.author_serializer(author))


@api.route('/api/authors', methods=('POST',))
@jwt_required()
def create_author():
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    author = Author.create(
        owner=current_identity, **validators.author_validator(request.json)
    )
    return jsonify(serializers.author_serializer(author)), 201


@api.route('/api/authors/<int:author_id>', methods=('PUT',))
@jwt_required()
def update_author(author_id):
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    author = Author.get_or_404(author_id)
    check_object_permission(current_identity, author)
    author.update(**validators.author_validator(request.json, True, author))
    return jsonify(serializers.author_serializer(author)), 201


@api.route('/api/authors/<int:author_id>', methods=('DELETE',))
@jwt_required()
def delete_author(author_id):
    author = Author.get_or_404(author_id)
    check_object_permission(current_identity, author)
    author.delete()
    return make_response(
        jsonify(message=f"Author '{author.fio}' has been deleted"), 204
    )


@api.route('/api/users', methods=('GET',))
def get_users():
    users = User.query.all()
    with_authors = request.values.get('with_authors')
    with_books = request.values.get('with_books')
    serialized_data = [serializers.user_serializer(
        obj, with_authors, with_books) for obj in users]
    return jsonify(serialized_data)


@api.route('/api/users/<int:user_id>', methods=('GET',))
def get_user(user_id):
    user = User.get_or_404(user_id)
    with_authors = request.values.get('with_authors')
    with_books = request.values.get('with_books')
    serialized_data = serializers.user_serializer(
        user, with_authors, with_books
    )
    return jsonify(serialized_data)


@api.route('/api/users', methods=('POST',))
def create_user():
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    author = User.create(**validators.user_validator(request.json))
    return jsonify(serializers.user_serializer(author)), 201


@api.route('/api/users/<int:user_id>', methods=('PUT',))
@jwt_required()
def update_user(user_id):
    if not request.json:
        abort(make_response(jsonify({'400': 'Bad request, not a JSON'}), 400))
    user = User.get_or_404(user_id)
    check_self_permission(current_identity, user)
    user.update(**validators.user_validator(request.json, True, user))
    return jsonify(serializers.user_serializer(user)), 201


@api.route('/api/users/<int:user_id>', methods=('DELETE',))
@jwt_required()
def delete_user(user_id):
    user = User.get_or_404(user_id)
    check_self_permission(current_identity, user)
    user.delete()
    return make_response(
        jsonify(message=f"Author '{user.name}' has been deleted"), 204
    )


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
