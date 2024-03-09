from flask import Blueprint

bp = Blueprint('users_api', __name__)

from app.api.users import routes