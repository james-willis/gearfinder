from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from re import split
from app import app, bcrypt, db, lm, oid
from .forms import LoginForm, SearchForm, SignupForm
from .models import User
from .mp_scanner import Post, get_matching_posts


@app.before_request
def before_request():
    g.user = current_user


# Routing functions
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = g.user
    form = SearchForm()
    if form.validate_on_submit():
        user.search_terms = str(form.search_terms.data)
        db.session.commit()
        session['search_terms'] = parse_terms(form.search_terms.data)
        return redirect(url_for('results'))
    return render_template('index.html',
                           title='Home',
                           form=form,
                           user=user)


@app.route('/results')
def results():
    posts = get_matching_posts(session['search_terms'])
    return render_template('results.html',
                           title='search results',
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        flash("Already signed in ")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            session['remember_me'] = form.remember_me.data
            session['search_terms'] = parse_terms(user.search_terms)
            return redirect(url_for('index'))
        else:
            flash('Wrong username/password combination')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if g.user is not None and g.user.is_authenticated:
        flash("Already signed in ")
        return redirect(url_for('index'))
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Login functions
@lm.user_loader
def load_user(email):
    return User.query.get(email)


def parse_terms(str_):
    return list(filter(bool, split('[.,\s]', str(str_))))
