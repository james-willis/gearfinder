from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from os.path import isfile
from re import split

from db_create import create_db
from app import app, bcrypt, db, lm
from .email_ import start_mail_thread
from .forms import AccountForm, EmailForm, LoginForm, SearchForm, SignupForm
from .models import User
from .mp_scanner import *


@app.before_first_request
def before_first_request():
    print('starting mail thread')
    start_mail_thread()
    if not isfile('./app.db'):
        print('initializing database')
        create_db()


@app.before_request
def before_request():
    g.user = current_user


# Routing functions
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    '''
    Renders the home page of the site
    '''
    return render_template('index.html',
                           title='Home')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    '''
    Renders the search page where the user can search with the search form or see the results of their email
    '''
    user = g.user
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('results', search_terms=form.search_terms.data))
    if request.method == 'POST':
        flash('Empty Search')
    return render_template('search.html',
                           title='Search',
                           form=form,
                           user=user)


@app.route('/results')
@app.route('/results/<string:search_terms>')
@login_required
def results(search_terms=None):
    if search_terms == None:
        search_terms = g.user.get_search_terms_str
    # TODO fix default term
    # TODO modify this so that it can be used to return multiple pages:
    search_term_list = parse_terms(search_terms)
    posts = get_matching_posts(search_term_list, get_forum_page(1))
    return render_template('results.html',
                           title='search results',
                           posts=posts,
                           search_terms=search_terms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        flash("Already signed in ")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user and bcrypt.check_password_hash(user.password, str(form.password.data)):
            # TODO move validation to LoginForm class
            login_user(user, remember=True)
            session['remember_me'] = form.remember_me.data
            return redirect(url_for('search'))
        else:
            flash('Wrong username/password combination')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if g.user is not None and g.user.is_authenticated:
        flash("Already signed in ")
        return redirect(url_for('search'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You may now log in')
        return redirect(url_for('login'))
    return render_template('sign_up.html',
                           title='Sign Up',
                           form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = g.user
    account_form = AccountForm()
    email_form = EmailForm()
    if account_form.validate_on_submit() and (bool(account_form.new_email.data) or bool(account_form.new_password.data)) \
            and bcrypt.check_password_hash(user.password, str(account_form.current_password.data)):
        # TODO move validation to AccountForm class
        if account_form.new_email.data:
            user.set_email(account_form.new_email.data)

            flash('Email Updated')
        if account_form.new_password.data:
            user.set_password(account_form.new_password.data)
            flash('Password Updated')
        db.session.commit()
        return redirect(url_for('logout'))
    return render_template('account.html',
                           title='Account Settings',
                           account_form=account_form,
                           email_form=email_form)


@app.route('/update_email', methods=['POST'])
@login_required
def update_email():
    user = g.user
    form = EmailForm()
    if form.validate_on_submit():
        # TODO make validation function that makes sure if opted in then you need to have non nulll search terms either
        # in db or on form
        if form.search_terms.data:
            user.set_search_terms(form.search_terms.data)
            flash('search terms updated to {}'.format(form.search_terms.data))
        user.set_email_opt_in(form.email_opt_in.data)
        db.session.commit()
    return redirect(url_for('account'))


@lm.user_loader
def load_user(email):
    return User.query.get(email)


def parse_terms(str_):
    return list(filter(bool, split('[.,\s]', str(str_))))
