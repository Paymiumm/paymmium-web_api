from app.models import User
from flask_json import JsonError, json_response
from app import db, api
from flask_restplus import Resource, reqparse, fields, marshal_with
from app.web import web
from sqlalchemy.exc import IntegrityError
from flask import render_template, url_for
from .security import generate_confirmation_token
from .email import send_email


parser = reqparse.RequestParser()
parser.add_argument('email', type=str, help='fields should not be left blank', location='json', required=True)

model = api.model('User', {
    'full_name': fields.String,
    'username': fields.String,
    'email': fields.String
})


@web.route('/signup')
class SignupApi(Resource):
    def get(self):
        return 'something'
    @api.marshal_with(model)
    @api.expect(model, validate=True)
    @api.doc(responses={
        200: 'success',
        400: 'validation error',
        'msg': 'post fields to db to create a new user'
    })
    def post(self):
        user = parser.parse_args()
        user_mail = User.query.filter_by(email=user.get('email')).first()
        if not user_mail:
            try:
                user_ = User(full_name=user.get('full_name'), username=user.get('username'), email=user.get('email'))
                db.session.add(user_)
                db.session.commit()

                token = generate_confirmation_token(user_.email)
                confirm_url = url_for('auth.confirm_email', token=token, _external=True)
                subject = 'Please confirm your email'
                html = render_template('activate.html', confirm_url=confirm_url)

                try:
                    send_email(user.email, subject, html)
                    return json_response(status_=201, text='A confirmation email has been sent to you')

                except Exception as e:
                    return json_response(status_=502, text='bad gateway')

                auth_token = user_.encode_auth_token(user_.id)

                return json_response(status_=201, text='you have registered successfully', auth_token=auth_token.decode())
            except Exception as e:
                return json_response(status_=401, text=str(e))
            except IntegrityError:
                db.session.rollback()

        else:
            return json_response(status_=202, text='User already exists. Please login.')



@web.route('/login')
class LoginWithOtp(Resource):
    def post(self):
        pass
