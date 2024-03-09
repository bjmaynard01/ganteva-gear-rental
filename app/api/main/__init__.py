from flask import Blueprint

bp = Blueprint('main_api', __name__)

from app.api.main import routes