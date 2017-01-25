from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from re import split
from app import app, bcrypt, db, lm
from .forms import AccountForm, LoginForm, SearchForm, SignupForm
from .models import User
from .mp_scanner import get_matching_posts


@app.before_request
def before_request():
    g.user = current_user


# Routing functions
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    user = g.user
    form = SearchForm()
    if form.validate_on_submit():
        user.search_terms = str(form.search_terms.data)
        db.session.commit()
        session['search_terms'] = parse_terms(form.search_terms.data)
        return redirect(url_for('results'))
    if request.method == 'POST':
        flash('Empty Search')
    return render_template('search.html',
                           title='Search',
                           form=form,
                           user=user)


@app.route('/results')
@login_required
def results():
    posts = get_matching_posts(session['search_terms'])
    return render_template('results.html',
                           title='search results',
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        flash("Already signed in ")
        return redirect(url_for('search'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)

        if user and bcrypt.check_password_hash(user.password, str(form.password.data)):
            # TODO move validation to LoginForm class
            login_user(user, remember=True)
            session['remember_me'] = form.remember_me.data
            session['search_terms'] = parse_terms(user.search_terms)
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
    form = AccountForm()
    if form.validate_on_submit() and (bool(form.new_email.data) or bool(form.new_password.data)) \
            and bcrypt.check_password_hash(user.password, str(form.current_password.data)):
        # TODO move validation to AccountForm class
        if form.new_email.data:
            user.set_email(form.new_email.data)
            flash('Email Updated')
        if form.new_password.data:
            user.set_password(form.new_password.data)
            flash('Password Updated')
        db.session.commit()
    return render_template('account.html',
                           title='Account Settings',
                           form=form)



@lm.user_loader
def load_user(email):
    return User.query.get(email)


def parse_terms(str_):
    return list(filter(bool, split('[.,\s]', str(str_))))
