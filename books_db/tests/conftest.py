import os
import tempfile

import pytest

from app import create_app
from books.models import Book, Author
from data import db
from users.models import User


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.app_context():
        db.create_all(app=app)
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def anonymous_client(app):
    """Anonymous test client for the app."""
    return app.test_client()


@pytest.fixture
def test_user1(anonymous_client):
    return User.create(
        username='TestUser1', email='testuser1@books.db',
        password='1234567',
    )


@pytest.fixture
def test_user2(anonymous_client):
    return User.create(
        username='TestUser2', email='testuser2@books.db',
        password='1234567',
    )


@pytest.fixture
def test_author1(anonymous_client, test_user1):
    return Author.create(
        isbn=123456789, fio='TestAuthor', user_id=test_user1.id,
    )


@pytest.fixture
def test_book1(anonymous_client, test_user1):
    return Book.create(
        isbn=987654321, title='TestBook', number_of_pages=123,
        review='TestReview', author_id=test_user1.id, user_id=test_user1.id,
    )


# @pytest.fixture
# def authorized_client(app, anonymous_client, test_user1):
#     payload = {'username': test_user1.username, 'password': '1234567'}
#     response = anonymous_client.post('/auth', json=payload)
#     print(response.json['access_token'])
#     assert app.test_client(headers={"Authorization": "JWT {}".format(
#         response.json['access_token'])})
