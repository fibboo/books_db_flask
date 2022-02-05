import random
from hashlib import pbkdf2_hmac
from hmac import compare_digest

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from data import db, CRUDMixin


class User(UserMixin, CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.LargeBinary(120))
    _salt = db.Column(db.String(120))
    books = db.relationship('Book', backref='owner', lazy='dynamic')
    authors = db.relationship('Author', backref='owner', lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if self._salt is None:
            self._salt = bytes(random.randrange(0, 255) for _ in range(128))
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        """
        Ensure that the provided password is valid.

        We are using this instead of a ``sqlalchemy.types.TypeDecorator`` (
        which would let us write ``User.password == password`` and have the
        incoming ``password`` be automatically hashed in a SQLAlchemy query)
        because ``compare_digest`` properly compares **all*** the characters
        of the hash even when they do not match in order to avoid timing
        oracle side-channel attacks.
        """
        new_hash = self._hash_password(password)
        return compare_digest(new_hash, self._password)

    def _hash_password(self, password):
        pwd = password.encode("utf-8")
        salt = bytes(self._salt)
        buff = pbkdf2_hmac("sha512", pwd, salt, iterations=100000)
        return bytes(buff)

    def __repr__(self):
        return "<User #{:d}>".format(self.id)

    def __str__(self):
        return self.username


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.is_valid_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.get_or_404(user_id)
