from flask_testing import TestCase
from flask import Flask
from app.models import db
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

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = self.client.post('/main/register',
            data=json.dumps(dict(
                full_name='joe@gmail.com',
                username='123456',
                email='something@example.com'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        db.session.remove()
        db.drop_all()




if __name__ == '__main__':
    unittest.main()