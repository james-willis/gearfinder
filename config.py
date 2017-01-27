import os
import credentials
WTF_CSRF_ENABLED = True
SECRET_KEY = credentials.SECRET_KEY

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = credentials.EMAIL_USERNAME
MAIL_PASSWORD = credentials.EMAIL_PASSWORD

SENDING_EMAIL = 'jimwillis95@gmail.com'
