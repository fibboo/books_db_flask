from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now())
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return self.username


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now())
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    fio = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Author %r>' % self.fio

    def __str__(self):
        return self.fio


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now())
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text(), nullable=False)
    # author_id = db.Column(
    #     db.Integer, db.ForeignKey('author.id'), nullable=False)
    # author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return '<Book %r>' % self.title

    def __str__(self):
        return self.title
