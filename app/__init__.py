from flask import Flask
from config import Config
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_marshmallow import Marshmallow

mail = Mail()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
login = LoginManager()
login.login_view = 'users.login'
login.login_message = ('Please login to access this page.')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.users import bp as users_bp
    app.register_blueprint(users_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.gear import bp as gear_bp
    app.register_blueprint(gear_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@maynardfolks.com',
                toaddrs=app.config['MAIL_ADMIN'], subject='Ganteva Gear Rental App Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Ganteva Gear Rental App Startup')
        
    return app

from app import models