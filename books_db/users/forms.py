from flask_wtf import FlaskForm
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from wtforms import fields, validators, ValidationError
from wtforms.validators import InputRequired, Email

from users.models import User


class LoginForm(FlaskForm):
    email = fields.StringField('Email', validators=[InputRequired(), Email()])
    password = fields.StringField('Password', validators=[InputRequired()])

    def validate_password(self, field):
        try:
            user = User.query.filter(User.email == self.email.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user")
        if user is None:
            raise ValidationError("Invalid user")
        if not user.is_valid_password(self.password.data):
            raise ValidationError("Invalid password")

        self.user = user


class RegistrationForm(FlaskForm):
    name = fields.StringField("Display Name")
    email = fields.StringField('Email', validators=[InputRequired(), Email()])
    password = fields.StringField('Password', validators=[InputRequired()])

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError("A user with that email already exists")
