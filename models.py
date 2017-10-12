from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app


class User(db.Model):
    """UserMixin, This provides default implementations for the methods that Flask-Login
   expects user objects to have."""

    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(60))
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    email_confirmed = db.Column(db.Boolean, default=False)
    account_confirmed = db.Column(db.Boolean, default=False)
    user = db.relationship('PrivateDetails', backref='users', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not in readable format')

    @password.setter
    def password(self, plaintext):
        self.password_hash = generate_password_hash(plaintext)

    def verify_password(self, plaintext):
        if check_password_hash(self.password_hash, plaintext):
            return True
        return False

    def encode_auth_token(self, user_id):
        # set up a payload with an expiration time
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            return jwt.encode(payload,
                              not current_app.config['SECRET_KEY'],
                              algorithm='HS256'
                              )
        # return an error in string format if an exception occurs
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            #  try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"





    def __repr__(self):
        """This method is used for debugging"""
        return 'User {}'.format(self.username)