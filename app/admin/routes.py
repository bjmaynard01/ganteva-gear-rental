from flask import render_template, session
from app.admin import bp as admin_bp
from app.users import utils
from flask_login import current_user
from app.users.models import User
from sqlalchemy.exc import SQLAlchemyError

@admin_bp.route('/admin/')
def admin():
    user_obj = User.query.filter_by(email=current_user.email).first()
    if user_obj.is_admin == True:
        return render_template('admin/admin.html', title='Admin Panel')
    else:
        return render_template('errors/401.html', title='Unauthorized'), 401
    
@admin_bp.route('/admin/gear')
def admin_gear():
    user_obj = User.query.filter_by(email=current_user.email).first()
    if user_obj.is_admin == True:
        return render_template('admin/gear.html', title='Gear Admin')
    else:
        return render_template('errors/401.html', title='Unauthorized'), 401

@admin_bp.route('/admin/gear/categories')
def gear_categories():
    user_obj = User.query.filter_by(email=current_user.email).first()
    if user_obj.is_admin == True:
        return render_template('admin/gearcategories.html', title='Gear Categories')
    else:
        return render_template('errors/401.html', title='Unauthorized'), 401