from flask import Flask, request, jsonify, render_template
from config import Config
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_marshmallow import Marshmallow
from sqlalchemy import MetaData


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

mail = Mail()
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
migrate = Migrate()
login = LoginManager()
login.login_view = 'users.login'
login.login_message = ('Please login to access this page.')

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="./templates")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
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

    from app.admin.gear import bp as admin_gear_bp
    app.register_blueprint(admin_gear_bp)

    from app.admin.users import bp as admin_users_bp
    app.register_blueprint(admin_users_bp)

    from app.admin.classes import bp as admin_classes_bp
    app.register_blueprint(admin_classes_bp)

    from app.admin.students import bp as admin_students_bp
    app.register_blueprint(admin_students_bp)

    #from app.api import bp as api_bp
    #app.register_blueprint(api_bp)

    from app.api.errors import bp as errors_api
    app.register_blueprint(errors_api)

    from app.api.users import bp as users_api
    app.register_blueprint(users_api)

    from app.api.gear import bp as gear_api
    app.register_blueprint(gear_api)

    from app.api.main import bp as main_api
    app.register_blueprint(main_api)

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
        file_handler = RotatingFileHandler('logs/gear-rental.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Ganteva Gear Rental App Startup')
        
    return app

from app.users.models import User
from app.gear.models import GearCategories
from app.admin.classes.models import Classes