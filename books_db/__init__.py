from flask import Flask
from flask_jwt import JWT
from flask_migrate import Migrate

from api.views import api
from auth import login_manager
from books.views import books_db
from data import db
from users.models import authenticate, identity
from users.views import users


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    migrate = Migrate(app, db)
    jwt = JWT(app, authenticate, identity)


    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(books_db)
    app.register_blueprint(users)
    app.register_blueprint(api)
    return app
