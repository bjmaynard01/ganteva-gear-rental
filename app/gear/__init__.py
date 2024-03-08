from flask import Blueprint

bp = Blueprint('gear', __name__)

from app.gear import routes