import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = 'books_db_flask'

DEBUG = os.getenv("DEBUG", default=False)

SECRET_KEY = os.getenv(
    "SECRET_KEY", default='flask-session-insecure-secret-key'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
WTF_CSRF_SECRET_KEY = os.getenv(
    "WTF_CSRF_SECRET_KEY", default='this-is-not-random-but-it-should-be'
)
JWT_EXPIRATION_DELTA = timedelta(days=33)

if DEBUG:
    DB_ROOT = os.path.dirname(BASE_DIR)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_ROOT, "books.db")
else:
    POSTGRES_USER = os.getenv('POSTGRES_USER', default='user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', default='password')
    DB_NAME = os.getenv('DB_NAME', default='books_db')
    DB_HOST = os.getenv('DB_HOST', default='db')
    DB_PORT = os.getenv('DB_PORT', default='5432')
    SQLALCHEMY_DATABASE_URI = ('postgresql://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME)  # noqa: E501
