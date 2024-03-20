from flask import Blueprint

bp = Blueprint('admin_gear', __name__)

from app.admin.gear import routes