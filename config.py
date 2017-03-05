from datetime import timedelta

import os

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
	SECRET_KEY = 'top-secret-key'

basedir = os.path.abspath(os.path.dirname(__file__))

# Database
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
        			'?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# Email Server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
SENDING_EMAIL = 'jimwillis95@gmail.com'
if not (MAIL_USERNAME and MAIL_PASSWORD):
	raise TypeError("MAIL_USERNAME and MAIL_PASSWORD must be defined")

# Celery / Redis
CELERYBEAT_SCHEDULE = {
    'email-updates': {
        'task': 'app.email_.email_new_posts',
        'schedule': timedelta(seconds=3)
    },
}

if not os.environ.get('REDIS_URL'):
	CELERY_BROKER_URL = 'redis://localhost:6379/0'
	CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
else:
	CELERY_BROKER_URL = os.environ['REDIS_URL']
	CELERY_RESULT_BACKEND = os.environ['REDIS_URL']

