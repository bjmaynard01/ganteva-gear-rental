from flask import Blueprint

bp = Blueprint('errors_api', __name__)

from app.api.errors import routes