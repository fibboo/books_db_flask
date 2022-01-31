from flask_wtf import FlaskForm
from wtforms import fields, validators

from .models import Author


class BookForm(FlaskForm):
    isbn = fields.IntegerField('ISBN',[validators.input_required()])
    title = fields.StringField('Title', [validators.input_required(),
                                         validators.Length(max=120)])
    number_of_pages = fields.IntegerField(
        'Number of pages', [validators.input_required()]
    )
    review = fields.TextAreaField('Review', [validators.input_required()])
    # author = QuerySelectField(query_factory=lambda: Author.query.all())
