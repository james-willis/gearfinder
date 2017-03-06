from celery import Celery
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
mail = Mail(app)

from app import views, models

# cli commands are not recognized in the other folder
# keeping here until I figure that out
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import app, db

import imp
import os

@app.cli.command(with_appcontext=False)
def create_db():
	db.create_all()
	if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
	    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
	    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	else:
	    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))


@app.cli.command(with_appcontext=False)
def downgrade_db():
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print('Current database version: ' + str(v))


@app.cli.command(with_appcontext=False)
def upgrade_db():
	api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print('Current database version: ' + str(v))


@app.cli.command(with_appcontext=False)
def migrate_db():
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
	tmp_module = imp.new_module('old_model')
	old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	exec(old_model, tmp_module.__dict__)
	script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
	open(migration, "wt").write(script)
	api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print('New migration saved as ' + migration)
	print('Current database version: ' + str(v))


@app.cli.command()
def start_worker():
	script="celery -A app.celery worker -B"
	os.system(script)


@app.cli.command()
def start_worker_verbose():
	script="celery -A app.celery worker -B --loglevel=info"
	os.system(script)

@app.cli.command(with_appcontext=False)
def start_redis():
	make_update_script_for_model = """
	cd redis-stable
	make
	src/redis-server
	"""
	os.system(script)


@app.cli.command(with_appcontext=False)
def update_requirements():
	script = """
	pip freeze > requirements.txt
	echo "psycopg2==2.4.4" >> requirements.txt
	"""
	os.system(script)
