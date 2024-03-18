from flask import Blueprint

bp = Blueprint('admin_users', __name__)

from app.admin.users import routes