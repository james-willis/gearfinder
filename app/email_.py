from threading import Thread, Timer
from flask import render_template
from flask_mail import Message

from app import app, celery, db, mail
from .models import User
from .mp_scanner import get_forum_page, get_matching_posts

_SENDING_EMAIL = app.config['SENDING_EMAIL']
_MSG_BODY = '<h1>Gearfinder</h1><h2>Here are new Mountain Project For Sale posts:</h2>'


@celery.task(name="email_new_posts")
def email_new_posts():

    # new posts are always on first page
    tree = get_forum_page(1) 
    users = db.session.query(User).all()
    for user in users:
        posts = get_matching_posts(user.parse_terms(), tree, "n")
        if posts and user.email_opt_in:
            message = {
                "subject": "New Mountain Project Items for Sale",
                "sender": _SENDING_EMAIL,
                "recipients": [user.email],
                "html": _MSG_BODY
            }

            message["html"] += render_template('results.html', posts=posts)

            send_email.delay(message)

@celery.task
def send_email(message):
    msg = Message(message['subject'], sender=message["sender"], recipients=message["recipients"])
    msg.html = message["html"]
    with app.app_context():
        mail.send(msg)
    return message["recipients"][0]

def mail_thread():
    Timer(300, mail_thread).start()
    email_new_posts()


def start_mail_thread():
    email_thread = Thread(target=mail_thread)
    email_thread.daemon = True
    email_thread.start()
