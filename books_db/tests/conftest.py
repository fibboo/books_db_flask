import os
import tempfile

import pytest

from app import create_app
from data import db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            db.create_all(app=app)
        yield client

    os.close(db_fd)
    os.unlink(db_path)
