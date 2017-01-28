from app import db, bcrypt
from re import split

class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(120), index=True, unique=True, primary_key=True)
    password = db.Column(db.String(128))
    search_terms = db.Column(db.String(120))
    email_opt_in = db.Column(db.Boolean)
    posts = db.relationship('Post', backref='recipient', lazy='dynamic')


    def __init__(self, email, password):
        self.set_email(email)
        self.set_password(password)
        self.set_search_terms('')
        self.set_email_opt_in(False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

    def get_search_terms_str(self):
        return self.search_terms

    def get_search_terms(self):
        return list(filter(bool, split('[.,\s]', str(self.search_terms))))

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password)

    def set_email(self, email):
        self.email = email

    def set_search_terms(self, terms):
        self.search_terms = terms

    def set_email_opt_in(self, bool):
        self.email_opt_in = bool

    def __repr__(self):
        return '<User %r>' % self.email


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.email'))
    title = db.Column(db.String(600))
    link = db.Column(db.String(600))
    sent = db.Column(db.Boolean)

    def __init__(self, owner, title, link):
        self.owner = owner
        self.title = title
        self.link = link
        self.sent = False
