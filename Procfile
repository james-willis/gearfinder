web: gunicorn app:app
worker: celery -A app.celery worker -B --loglevel=info
init: python db_create.py
upgrade: python db_upgrade.py
