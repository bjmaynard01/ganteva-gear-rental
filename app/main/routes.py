from app.main import bp as main_bp
from flask_login import current_user
from flask import render_template, request, send_from_directory
from flask import current_app

@main_bp.route('/')
@main_bp.route('/index')
def index():

    if current_user.is_authenticated:
        return render_template('index.html', title='Home', user=current_user)
    else:
        return render_template('index.html', title='Home')


@main_bp.route('/credits')
def credits():
    return render_template('credits.html')

@main_bp.route('/robots.txt')
def robots():
    return send_from_directory(current_app.static_folder, request.path[1:])