from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class AccountForm(FlaskForm):
    #TODO make stricter validation requirements
    new_email = StringField('email')
    current_password = PasswordField('current_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class EmailForm(FlaskForm):
    # TODO make it pull optin from db
    search_terms = StringField('search_terms')
    email_opt_in = BooleanField('email_opt_in', default=False)


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SignupForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),
                                                     EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class SearchForm(FlaskForm):
    search_terms = StringField('search_terms', validators=[DataRequired()])

