from .models import User
from flask import flash, g
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class AccountForm(FlaskForm):
    #TODO make stricter validation requirements
    new_email = StringField('email')
    current_password = PasswordField('current_password')
    new_password = PasswordField('new_password')
    confirm = PasswordField('Repeat Password')
    
    def validate(self):
        user = g.user

        if not (self.new_password.data or self.new_email.data):
            return False
        if not user.compare_password(self.current_password.data):
            flash("Password Incorrect", 'danger')
            return False
        if self.new_password.data != self.confirm.data:
            flash("New passwords must match", 'danger')
            return False
        return True



class EmailForm(FlaskForm):
    search_terms = StringField('search_terms')
    email_opt_in = BooleanField('email_opt_in', default=True)
    # def __init__(self, search_terms='', opt_in=False, *args, **kwargs):
    #     super(EmailForm, self).__init__(*args, **kwargs)
    #     self.search_terms.default = search_terms
    #     self.email_opt_in.default = opt_in
    #     self.process()


class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    remember_me = BooleanField('remember_me', default=False)

    def validate(self):
        user = User.query.get(str(self.email.data))
        if user and user.compare_passwords(self.password.data):
            return True
        flash("Wrong Password/Username Combination", 'danger')
        return False


class SignupForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    confirm = PasswordField('Repeat Password')

    def validate(self):
        user = User.query.get(str(self.email.data))
        if user is not None:
            flash("Username already taken", 'danger')
            return False
        if self.password.data != self.confirm.data:
            flash("Passwords must match", 'danger')
            return False
        return True

class SearchForm(FlaskForm):
    search_terms = StringField('search_terms', validators=[DataRequired()])

