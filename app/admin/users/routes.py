from app.admin.users import bp as admin_users_bp
from flask import render_template, url_for, redirect, flash, current_app
from app import db
from app.admin.users import bp as admin_users_bp
from flask_login import current_user, login_required
from app.users.models import User
#from app.admin.users.admin_forms import UserAdminForms
from sqlalchemy.exc import SQLAlchemyError
#from app.users.utils import functions

@admin_users_bp.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_anonymous:
        if current_user.is_admin == True:

            users = User.query.all()
            return render_template('admin/users/admin_users.html', title='User Admin', users=users)
        
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    else:
        flash('You must login to administer users.')
        return redirect(url_for('users.login'))

@admin_users_bp.route('/admin/users/<id>/update')
@login_required
def update_user(id):
    if not current_user.is_anonymous:
        
        if current_user.is_admin == True:
            user = User.query.get_or_404(id)
            
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
        
    else:
        flash('You must be logged in as admin to update user accounts.')
        return redirect(url_for('users.login'))