from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON
from config import DevelopmentConfig
from flask_restplus import Api


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
json = FlaskJSON()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    mail.init_app(app)
    json.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.session_protection = 'strong'

    with app.app_context():
        db.create_all()

    from .web import web
    api.init_app(web)

    app.register_blueprint(web, url_prefix='/web')

    return app