import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'unguessable-secret-code'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 1025
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_ADMIN = os.environ.get('MAIL_ADMIN')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SERVER_NAME = os.environ.get('SERVER_NAME') or '127.0.0.1:8090'
    API_ADMIN_KEY = os.environ.get('API_ADMIN_KEY')
    API_READ_KEY = os.environ.get('API_READ_KEY')
    #RESET_PASS_TOKEN_MAX_AGE = os.environ.get('RESET_PASS_TOKEN_MAX_AGE') or 1800
    RESET_PASS_TOKEN_MAX_AGE = 1800
    CONFIRMATION_TOKEN_MAX_AGE = 3600
    REGISTRATION_SUBJECT = os.environ.get('REGISTRATION_SUBJECT') or 'Test Subject'
    PASSWORD_RESET_SUBJECT = os.environ.get('PASSWORD_RESET_SUBJECT') or 'Test Password Reset Subject'
