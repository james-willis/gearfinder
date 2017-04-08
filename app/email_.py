from threading import Thread, Timer
from flask_mail import Message

from app import app, celery, db, mail
from .models import User
from .mp_scanner import *

_SENDING_EMAIL = app.config['SENDING_EMAIL']
_MSG_BODY = '<h1>Gearfinder</h1><h2>Here are new Mountain Project For Sale posts:</h2>'


@celery.task
def email_new_posts():

    tree = get_forum_page(1)  # new posts always on first page
    users = db.session.query(User).all()
    for user in users:
        
        posts = get_matching_posts(user.get_search_terms(), tree, "n")
        if posts and user.email_opt_in:
            message = {
                "subject": "New Mountain Project Items for Sale",
                "sender": _SENDING_EMAIL,
                "recipients": [user.email],
                "html": _MSG_BODY
            }
            
            for link in write_links(posts):
                message["html"] += "<br>{}".format(link)

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
