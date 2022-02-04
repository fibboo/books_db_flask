from flask import Flask

from api.views import api
from auth import login_manager
from books.views import books_db
from data import db
from users.views import users

app = Flask(__name__)
app.config.from_object('config')


db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(books_db)
app.register_blueprint(users)
app.register_blueprint(api)
