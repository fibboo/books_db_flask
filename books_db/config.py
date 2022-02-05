import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'flask-session-insecure-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, "books.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
WTF_CSRF_SECRET_KEY = 'this-is-not-random-but-it-should-be'
JWT_EXPIRATION_DELTA = timedelta(days=33)
