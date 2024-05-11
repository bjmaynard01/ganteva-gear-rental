from flask import Blueprint

bp = Blueprint('admin_classes', __name__)

from app.admin.classes import routes