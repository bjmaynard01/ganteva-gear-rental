from app.admin.users import bp as admin_users_bp
from flask import render_template, url_for, redirect, flash, current_app
from app import db
from app.admin.users import bp as admin_users_bp
from flask_login import current_user, login_required
from app.users.models import User
from sqlalchemy.exc import SQLAlchemyError
from app.admin.users.admin_forms import UserAdminForm

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

@admin_users_bp.route('/admin/users/<id>/update', methods=['GET', 'POST'])
@login_required
def update_user(id):
    if not current_user.is_anonymous:
        
        if current_user.is_admin == True:
            try:
                user = User.query.get_or_404(id)

            except SQLAlchemyError as error:
                return render_template('errors/500.html', title='Internal Error'), 500
            
            if user is not None:
                update_user_form = UserAdminForm(user.email)

                if update_user_form.validate_on_submit():
                    user.fname = update_user_form.f_name.data.capitalize()
                    user.lname = update_user_form.l_name.data.capitalize()
                    user.email = update_user_form.email.data.lower()
                    user.phone = update_user_form.phone.data
                    if update_user_form.password.data is not None:
                        user.set_password(update_user_form.password.data)
                    user.confirmed = update_user_form.confirmed.data
                    user.is_admin = update_user_form.admin.data

                    try:
                        db.session.add(user)
                        db.session.commit()
                        flash('Successfully updated user {}'.format(user.email))
                        return redirect(url_for('admin_users.admin_users'))
                
                    except SQLAlchemyError as error:
                        return render_template('errors/500.html', title='Internal Error'), 500

                update_user_form.admin.data = user.is_admin
                update_user_form.confirmed.data = user.confirmed
                update_user_form.email.data = user.email
                update_user_form.phone.data = user.phone
                update_user_form.f_name.data = user.fname
                update_user_form.l_name.data = user.lname

                return render_template('admin/users/update_user.html', title='Update User', form=update_user_form,
                                       user=user), 200

        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
        
    else:
        flash('You must be logged in as admin to update user accounts.')
        return redirect(url_for('users.login'))
    
@admin_users_bp.route('/admin/users/<id>/delete')
@login_required
def delete_user(id):

    if not current_user.is_anonymous:
        if current_user.is_admin == True:
            
            try:
                user = User.query.get_or_404(id)
                db.session.delete(user)
                db.session.commit()
                flash('Successfully deleted user {}'.format(user.email))
                return redirect(url_for('admin_users.admin_users'))

            except SQLAlchemyError as error:
                return render_template('errors/500.html', title='Internal Error'), 500
        
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401

    else:
        flash('You must be logged in as admin to delete users.')
        return redirect(url_for('users.login'))