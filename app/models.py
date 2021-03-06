from app import db, bcrypt
from re import split

class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(120), index=True, unique=True, primary_key=True)
    password = db.Column(db.Binary(128))
    search_terms = db.Column(db.String(120))
    email_opt_in = db.Column(db.Boolean)
    posts = db.relationship('Post', backref='recipient', lazy='dynamic')


    def __init__(self, email, password):
        self.email = email
        self.search_terms = ''
        self.email_opt_in = False
        self.update_password(password)


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

    def update_password(self, raw_password):
        '''
        A function that salt and hashs a new password, and updates the database with the new salted hash
        '''
        
        self.password = bcrypt.generate_password_hash(raw_password.encode('utf-8'))
    
    def get_password(self):
        return self.password

    def compare_passwords(self, password):
        print(type(password))
        return bcrypt.check_password_hash(self.get_password(), str(password).encode('utf-8'))

    def parse_terms(self):
        return list(filter(bool, split('[.,\s]', str(self.search_terms))))

    def __repr__(self):
        return '<User %r>' % self.email


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(120), db.ForeignKey('user.email'))
    title = db.Column(db.String(600))
    link = db.Column(db.String(600))
    sent = db.Column(db.Boolean)

    def __init__(self, owner, title, link):
        self.owner = owner
        self.title = title
        self.link = link
        self.sent = False
