from flask import Blueprint

bp = Blueprint('admin_students', __name__)

from app.admin.students import routes