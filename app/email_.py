from threading import Thread, Timer
from flask import render_template
from flask_mail import Message

from app import app, celery, db, mail
from .models import User
from .mp_scanner import get_forum_page, get_matching_posts

_SUBJECT_LINE = "Gearfinder New Post Alert"
_SENDING_EMAIL = app.config['SENDING_EMAIL']


@celery.task(name="email_new_posts")
def email_new_posts():

    # new posts are always on first page
    tree = get_forum_page(1) 
    users = db.session.query(User).all()
    for user in users:
        posts = get_matching_posts(user.parse_terms(), tree, "n")
        if posts and user.email_opt_in:
            message = {
                "subject": _SUBJECT_LINE,
                "sender": _SENDING_EMAIL,
                "recipients": [user.email],
                "html": ""
            }
            with app.app_context():
                message["html"] = render_template('email.html', posts=posts)

            send_email.delay(message)

@celery.task
def send_email(message):
    msg = Message(message['subject'], sender=message["sender"], recipients=message["recipients"])
    msg.html = message["html"]
    with app.app_context():
        mail.send(msg)
    return message["recipients"][0]
