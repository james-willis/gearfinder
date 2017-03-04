web: gunicorn app:app
worker: celery -A app.celery worker
beat: celery -A app.celery beat
init: python db_create.py
upgrade: python db_upgrade.py
