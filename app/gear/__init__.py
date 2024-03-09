from flask import Blueprint

bp = Blueprint('gear', __name__, static_folder='static', static_url_path='/gear/static')

from app.gear import routes