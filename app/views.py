from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from os.path import isfile
from re import split

from app import app, bcrypt, db, lm
from .email_ import start_mail_thread
from .forms import AccountForm, EmailForm, LoginForm, SearchForm, SignupForm
from .models import User
from .mp_scanner import *

_ERROR = 'danger'
_NOTIFICATION = 'info'


@app.before_first_request
def before_first_request():
    pass
    # TODO make this initialize db is db isnt initalized


@app.before_request
def before_request():
    g.user = current_user


# Routing functions
@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/search/', methods=['GET', 'POST'])
@login_required
def search():
    user = g.user
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('results', search_terms=form.search_terms.data))
    if request.method == 'POST':
        flash('Empty Search', _ERROR)
    return render_template('search.html',
                           title='Search',
                           form=form,
                           user=user)


@app.route('/results')
@app.route('/results/<string:search_terms>/')
@login_required
def results(search_terms=None):
    if search_terms == None:
        flash("Please search to see results", _ERROR)
        return redirect(url_for('search'))
    # TODO modify this so that it can be used to return multiple pages:
    search_term_list = parse_terms(search_terms)
    posts = get_matching_posts(search_term_list, get_forum_page(1))
    return render_template('results.html',
                           title='search results',
                           posts=posts,
                           search_terms=search_terms)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if g.user is not None and g.user.is_authenticated:
        flash("Already signed in", _NOTIFICATION)
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = User.query.get(str(form.email.data))
        login_user(user, remember=True)
        session['remember_me'] = form.remember_me.data
        return redirect(url_for('search'))

    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup/', methods=['GET', 'POST'])
def sign_up():
    # redirect signed in users away from sign up page
    if g.user is not None and g.user.is_authenticated:
        flash("Already signed in ", _NOTIFICATION)
        return redirect(url_for('index'))

    form = SignupForm()

    if form.validate_on_submit():

        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('You may now log in', _NOTIFICATION)
        return redirect(url_for('login'))

    return render_template('sign_up.html',
                           title='Sign Up',
                           form=form)


@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    account_form = AccountForm()
    email_form = EmailForm(search_terms=g.user.search_terms, email_opt_in=g.user.email_opt_in)
    return render_template('account.html',
                           title='Account Settings',
                           account_form=account_form,
                           email_form=email_form)


@app.route('/update_credentials/', methods=['POST'])
@login_required
def update_credentials():

    user = g.user
    account_form = AccountForm()

    if account_form.validate_on_submit():
        # TODO move validation to AccountForm class

        if account_form.new_email.data:
            user.set_email(account_form.new_email.data)
            flash('Email Updated', _NOTIFICATION)

        if account_form.new_password.data:
            user.set_password(account_form.new_password.data)
            flash('Password Updated', _NOTIFICATION)

        db.session.commit()
        return redirect(url_for('logout'))

    return redirect(url_for('account'))


@app.route('/update_email_settings/', methods=['POST'])
@login_required
def update_email_settings():

    user = g.user
    form = EmailForm()

    if form.validate_on_submit():

        if form.email_opt_in.data != user.email_opt_in:
            if form.email_opt_in.data:
                flash('Subscribed to Emails', _NOTIFICATION)
            else:
                flash('Unsubscribed from Emails', _NOTIFICATION)

            user.set_email_opt_in(form.email_opt_in.data)

        if form.search_terms.data and form.search_terms.data != user.search_terms:
            user.set_search_terms(form.search_terms.data)
            flash('Subscribed Search Updated', _NOTIFICATION)

        db.session.commit()

    return redirect(url_for('account'))


@lm.user_loader
def load_user(email):
    return User.query.get(email)


def parse_terms(str_):
    return list(filter(bool, split('[.,\s]', str(str_))))
