from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app


def generate_confirmation_token(email):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.dumps(email, salt=current_app.config['SECURITY_EMAIL_SALT'])


def confirm_token(token, expiration=84600):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.loads(token, salt=current_app.config['SECURITY_EMAIL_SALT'], max_age=expiration)


def generate_recovery_token(email):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_recovery_token(token, expiration=3600):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)


def resend_confirmation_token(email):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.dumps(email, salt=current_app.config['RESEND_EMAIL_SALT'])


def confirm_resend_confirmation_token(token, expiration=84600):
    ts = Serializer(current_app.config['SECRET_KEY'])
    return ts.loads(token, salt=current_app.config['RESEND_EMAIL_SALT'], max_age=expiration)
