from app import mail
from flask_mail import Message
from flask import current_app
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    thr = Thread(target=send_async_email, args=[current_app, msg])
    thr.start()
    return thr

