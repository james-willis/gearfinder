from threading import Thread, Timer
from flask_mail import Message

from app import app, db, mail
from .models import User
from .mp_scanner import *

_SENDING_EMAIL = app.config['SENDING_EMAIL']


def email_new_posts():
    tree = get_forum_page(1)  # new posts always on first page
    users = db.session.query(User).all()

    for user in users:
        msg = Message('test subject', sender=_SENDING_EMAIL, recipients=[user.email])
        msg.html = '<h1>Gearfinder</h1><h2>Here are new Mountain Projet For Sale posts:</h2>'

        posts = get_matching_posts(user.get_search_terms(), tree, 'n')
        if len(posts) == 0 or not user.email_opt_in:
            continue

        for link in write_links(posts):
            msg.html += "<br>{}".format(link)

        with app.app_context():
            mail.send(msg)


def mail_thread():
    Timer(300, mail_thread).start()
    email_new_posts()


def start_mail_thread():
    email_thread = Thread(target=mail_thread)
    email_thread.daemon = True
    email_thread.start()
