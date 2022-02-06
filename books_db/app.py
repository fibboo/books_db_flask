from flask import Flask
from flask_jwt import JWT
from flask_migrate import Migrate

from api.views import api
from auth import login_manager
from books.views import books_db
from data import db
from users.models import authenticate, identity
from users.views import users


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object('config')
    else:
        # load the test config if passed in
        app.config.update(test_config)

    migrate = Migrate(app, db)  # noqa: F841
    jwt = JWT(app, authenticate, identity)  # noqa: F841

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(books_db)
    app.register_blueprint(users)
    app.register_blueprint(api)
    return app


app = create_app()
