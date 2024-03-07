from flask import Blueprint, render_template, request, send_from_directory
from flask_login import current_user
from flask import app

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():

    if current_user.is_authenticated:
        return render_template('index.html', title='Home', user=current_user)
    else:
        return render_template('index.html', title='Home')

@main.route('/credits')
def credits():
    return render_template('credits.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])