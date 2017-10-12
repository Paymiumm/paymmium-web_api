from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON
from config import DevelopmentConfig
from flask_restplus import Api

db = SQLAlchemy()
mail = Mail()
json = FlaskJSON()
api = Api(version='1.0', validate=True, catch_all_404s=True)

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    mail.init_app(app)
    json.init_app(app)
    api.init_app(app)


    from app import views

    with app.app_context():
        db.create_all()

    return app