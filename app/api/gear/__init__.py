from flask import Blueprint

bp = Blueprint('gear_api', __name__)

from app.api.gear import routes