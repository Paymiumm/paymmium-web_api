from flask_testing import TestCase
from flask import Flask
from app.models import db, User
import unittest
import json
from config import Testing


class MyTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(Testing)
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def test_encode_token(self):
        user = User(full_name='something', username='emma', email='s@gmail.com',  password='ksks')
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

    def test_decode_token(self):
        user_details = User(full_name='mr jones', username='hit me', email='emmanuel@gmail',  password='something ')
        db.session.add(user_details)
        db.session.commit()
        auth_token = user_details.encode_auth_token(user_details.id)
        self.assertTrue(isinstance(auth_token, str))
        self.assertTrue(User.decode_token(auth_token == 1))


    def test_token(self):
        pass


    def tearDown(self):
        db.session.remove()
        db.drop_all()



if __name__ == '__main__':
    unittest.main()
