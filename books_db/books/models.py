from sqlalchemy import func

from data import db, CRUDMixin



class Author(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now())
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    fio = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Author %r>' % self.fio

    def __str__(self):
        return self.fio


class Book(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now())
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text(), nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey(
            'author.id', ondelete='CASCADE'), nullable=False,
    )
    author = db.relationship('Author', backref=db.backref(
        'books', lazy=True, cascade='all, delete-orphan',
    ))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Book %r>' % self.title

    def __str__(self):
        return self.title
