from flask import render_template, session, url_for, redirect, flash, request
from app.admin import bp as admin_bp
from flask_login import current_user, login_required

@admin_bp.route('/admin')
@login_required
def admin():
    
    if not current_user.is_anonymous:
    
        if current_user.is_admin == True:
            return render_template('admin/admin.html', title='Admin Panel'), 200
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    
    else:
        return redirect(url_for('users.login'))
    
    
