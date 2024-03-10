from flask import render_template, session
from app.admin import bp as admin_bp
from app.users import utils
from flask_login import current_user
from app.users.models import User
from sqlalchemy.exc import SQLAlchemyError

@admin_bp.route('/admin')
def admin():
    if not current_user.is_anonymous:
        try:
            user_obj = User.query.filter_by(email=current_user.email).first()
            if user_obj.is_admin == True:
                return render_template('admin/admin.html', title='Admin Panel'), 200
        except SQLAlchemyError as error:
            return render_template('errors/500.html', title='Internal Error'), 500
    else:
        return render_template('errors/401.html', title='Unauthorized'), 401
    
@admin_bp.route('/admin/gear')
def gear_admin():
    try:
        user_obj = User.query.filter_by(email=current_user.email).first()
    except SQLAlchemyError as error:
        return render_template('errors/500.html', title='Internal Error'), 500
    if user_obj.is_admin == True:
        return render_template('admin/gear.html', title='Gear Admin'), 200
    else:
        return render_template('errors/401.html', title='Unauthorized'), 401

@admin_bp.route('/admin/gear/categories')
def gear_categories():
    try:
        user_obj = User.query.filter_by(email=current_user.email).first()
    except SQLAlchemyError as error:
        return render_template('errors/500.html', title='Internal Error'), 500
    if user_obj.is_admin == True:
        return render_template('admin/categories.html', title='Gear Categories'), 200
    else:
        return render_template('errors/401.html', title='Unauthorized'), 401