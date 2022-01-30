from sqlalchemy import func

from settings import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now())
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.username


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now())
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    fio = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.fio


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now())
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    review = db.Column(db.Text(), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return self.title
