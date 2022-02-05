from flask import jsonify, abort, make_response

from books.models import Author, Book
from users.models import User


def is_unique(query):
    if len(query) > 0:
        return False
    return True


def validate_required_fields(required_fields, json_data):
    wrong_fields = []
    for field, tp in required_fields.items():
        if field not in json_data:
            wrong_fields.append({field: 'Field is required'})
        elif not isinstance(json_data[field], tp):
            wrong_fields.append(
                {field: f"Field must be of type '{tp.__name__}'"}
            )
    if len(wrong_fields) > 0:
        abort(make_response(jsonify(wrong_fields), 400))


def book_validator(json_data, is_update=False, book=None):
    required_fields = {
        'isbn': int, 'title': str, 'number_of_pages': int,
        'review': str, 'author': int,
    }
    validate_required_fields(required_fields, json_data)

    if not is_update:
        if not is_unique(Book.query.filter_by(isbn=json_data['isbn']).all()):
            abort(make_response(
                jsonify({'isbn': 'Field must be unique'}), 400)
            )
    elif book.isbn != json_data['isbn']:
        if not is_unique(Book.query.filter_by(isbn=json_data['isbn']).all()):
            abort(make_response(
                jsonify({'isbn': 'Field must be unique'}), 400)
            )

    author = Author.get_or_404(json_data['author'])
    json_data['author'] = author
    return json_data


def author_validator(json_data, is_update=False, author=None):
    required_fields = {'isbn': int, 'fio': str}
    validate_required_fields(required_fields, json_data)

    if not is_update:
        if not is_unique(Author.query.filter_by(isbn=json_data['isbn']).all()):
            abort(make_response(
                jsonify({'isbn': 'Field must be unique'}), 400)
            )
    elif author.isbn != json_data['isbn']:
        if not is_unique(Author.query.filter_by(isbn=json_data['isbn']).all()):
            abort(make_response(
                jsonify({'isbn': 'Field must be unique'}), 400)
            )

    return json_data


def user_validator(json_data, is_update=False, user=None):
    required_fields = {'name': str, 'email': str}
    validate_required_fields(required_fields, json_data)

    if not is_update:
        if not is_unique(
                User.query.filter_by(email=json_data['email']).all()
        ):
            abort(
                make_response(jsonify({'email': 'Field must be unique'}), 400)
            )
    elif user.email != json_data['email']:
        if not is_unique(User.query.filter_by(email=json_data['email']).all()):
            abort(make_response(
                jsonify({'email': 'Field must be unique'}), 400)
            )

    return json_data
