import os
import tempfile

import pytest

from app import create_app
from data import db
from users.models import User


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})
    db.init_app(app)

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
def test_user1():
    return User.create(
        username='TestUser1', email='testuser1@books.db',
        password='1234567',
    )
