import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """This class contains
    configs of all flask extensions
    being used
    """
    # flask_wtf configs
    WTF_CSRF_ENABLED = True  # this protects forms against cross-site forgery
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # generate a standard secret key and als
    #  Used to securely sign the token

    # sqlalchemy config using sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_JSONEDITOR = True
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')


    # RecaptchaField config
    RECAPTCHA_PUBLIC_KEY = '6LfFNysUAAAAAH8XvHjiSSpCpxrJc95vI-uN5Swy'
    RECAPTCHA_PRIVATE_KEY = '6LfFNysUAAAAAHbiD_yVYEG9rZfrft48x9VPHzl6'  # this key should be kept secret

    # Mail Settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_USERNAME = 'emmanuelukwuegbu2016@gmail.com'
    MAIL_PASSWORD = '@1OBINNN'
    MAIL_DEFAULT_SENDER = 'myapp@app.com'

    SECURITY_PASSWORD_SALT = 'password-reset-salt'  # salt used for forgot password
    SECURITY_EMAIL_SALT = 'email-confirmation-salt'  # salt used for email confirmation

    RESEND_EMAIL_SALT = 'resend-email-confirmation'

    JSON_DECODE_ERROR_MESSAGE = 'invalid values'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': Testing
}




