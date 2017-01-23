from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(120), index=True, unique=True, primary_key=True)
    password = db.Column(db.String(120))
    search_terms = db.Column(db.String(120))
    posts = db.relationship('Post', backref='recipient', lazy='dynamic')


    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

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

    def __repr__(self):
        return '<User %r>' % self.email


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.email'))
    title = db.Column(db.String(600))
    link = db.Column(db.String(600))
