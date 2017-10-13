from app.models import User
from flask_json import json_response
from app import db
from flask_restplus import Resource, reqparse, fields, inputs
from app import api, json
from sqlalchemy.exc import IntegrityError
from flask import render_template
from app.security import generate_confirmation_token, confirm_token
from app.email import send_email
from twilio.rest import Client
from flask import current_app
from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)


@json.invalid_json_error
def invalid_json():
    return json_response(status_=400, description='Not a Json')

@json.error_handler
def error_handler(e):
    return json_response(status_=401, description='An error occured')

def send_sms(to_number, body):
    """This function is to send_sms using twillio"""
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    twilio_number = current_app.config['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)
    client.api.messages.create(to_number, from_=twilio_number, body=body)


parser = reqparse.RequestParser()  # parsing arguments
parser.add_argument('full_name', type=str, help='Name should not be left blank', location='json', required=True)
parser.add_argument('username', type=str, help='username should not be left blank', location='json', required=True)
parser.add_argument('email', type=inputs.email(check=True), help='email should not be left blank', location='json', required=True)

model = api.model('User', {
    'full_name': fields.String(description='The user full name'),
    'username': fields.String(description='the username of the user'),
    'email': fields.String(description='the user email')
})

@api.route('/')
class Hello(Resource):
   def get(self):
       return json_response('hello')


@api.route('/register')
class RegisterUserApi(Resource):
    @api.expect(model, validate=True)
    @api.doc(responses={
        201: 'success',
        401: 'validation error',
        'msg': 'post fields to db to create a new user'
    })
    def post(self):
        user = parser.parse_args()
        user_mail = User.query.filter_by(email=user.get('email')).first()
        if not user_mail:
            try:
                user = User(full_name=user.get('full_name'), username=user.get('username'), email=user.get('email'))
                db.session.add(user)
                db.session.commit()

                token = generate_confirmation_token(user.email)
                confirm_url = api.url_for(ConfirmEmailApi, token=token, _external=True)
                subject = 'Please confirm your email'
                html = render_template('activate.html', confirm_url=confirm_url)

                send_email(user.email, subject, html)
                return json_response(status=201, text='Success')

            except IntegrityError:
                db.session.rollback()
                return json_response(status_=501, text='internal error')

            except Exception as e:
                return json_response(status_=401, text=str(e))

        else:
            return json_response(status_=202, text='User already exists. Please login.')


@api.route('/confirm-email/<token>')
class ConfirmEmailApi(Resource):
    def get(self, token):
        try:
            email = confirm_token(token)
        except Exception as e:
            return json_response(status=401, text='This link is broken or might has expired')

        user = User.query.filter_by(email=email).first()

        if user.email_confirmed:
            return json_response(status_=201, text='email has been confirmed please login')
        else:
            user.email_confirmed = True
            try:
                db.session.add(user)
                db.session.commit()
                return json_response(status_=201, text='Your email has been confirmed succefully')
            except IntegrityError:
                return json_response(status_=501, text='Internal server error')

parse = reqparse.RequestParser()
parse.add_argument('email', type=inputs.email(check=True), location='json')

user_login_email = api.model('User', {
    'email': fields.String(description='the user email')
})


@api.route('/login-with-email')
@api.doc(param={
    'email': 'An email'
})
class LoginWithEmailApi(Resource):
    def get(self):
        pass

    @api.doc(responses={'401': 'validation failed',
                        '201': 'success'})
    @api.marshal_with(user_login_email)
    @api.expect(parse)
    def post(self):
        args = parse.parse_args(strict=True)
        user = User.query.filter_by(email=args.get('email'))
        if user and user.email_confirmed:
            from . import gen_password
            otp = 'Paymiumm code {}'.format(gen_password)

            try:
                send_sms(user.phone_number, otp)

            except Exception as e:
                return json_response(status_=502, text='Failed')

            user.password = otp

            db.session.add(user)
            db.session.commit()

            return json_response(status_=201, text='A one time pass code has been sent to you')

        elif not user.email_confirmed:
            return json_response(status_=401, text='Please confirm your email before you would be able to login')

        else:
            return json_response(status_=401, text='This user doesnt exist')


parse_otp = reqparse.RequestParser()
parse_otp.add_argument('otp', type=str, required=True)

user_login_otp = api.model('User',
                           {
                               'email': fields.String(description='user email'),
                               'password': fields.String(description='The user password')
                           })


@api.route('/login-with otp')
@api.doc(params={
    'otp': 'one-time-pass',
    'email': 'user email'
})
class LoginWithOtpApi(Resource):
    def get(self):
        pass

    @api.marshal_with(user_login_otp)
    @api.doc(responses={
        'success': 201,
        'validation failed': 401
    })
    def post(self):
        try:
            request_details = parse_otp.parse_args(strict=True)

            user = User.query.filter_by(email=request_details.get('otp')).first()

            if user and user.verify_password(request_details.get('otp')):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    return json_response(status_=201, text='Successfully logged in', auth=auth_token.decode())
                db.session.delete(user.password)
                db.session.commit()

            else:
                return json_response(status_=401, text='invalid otp')

        except Exception as e:
            return json_response(status_=401, text='Failed', type=str(e))
