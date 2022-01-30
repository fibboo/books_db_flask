from wtforms import Form, fields


class BookForm(Form):
    isbn = fields.IntegerField()
    title = fields.StringField()
    number_of_pages = fields.IntegerField()
    review = fields.TextAreaField()
