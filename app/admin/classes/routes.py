from app.admin.classes import bp as admin_classes_bp
from flask import render_template, url_for, redirect, flash, current_app
from app import db
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from app.admin.classes.models import Classes
from app.admin.classes.forms import ClassAddForm, ClassUpdateForm

@admin_classes_bp.route('/admin/classes')
@login_required
def admin_classes():
    if not current_user.is_anonymous:

        if current_user.is_admin == True:
            try:
                classes = Classes.query.all()
                return render_template('admin/classes/admin_classes.html', title='Class Administration', classes=classes), 200
            
            except SQLAlchemyError as error:
                return render_template('errors/500.html', title='Internal Error'), 500

        else:
            return render_template('errors/401.html', title='Unauthorized'), 401

    else:
        flash('You must login to administer classes')
        return redirect(url_for('users.login'))
    
@admin_classes_bp.route('/admin/classes/add', methods=['GET', 'POST'])
@login_required
def add_class():
    if not current_user.is_anonymous:

        if current_user.is_admin == True:
            add_class_form = ClassAddForm()

            if add_class_form.validate_on_submit():
                class_name = add_class_form.name.data
                class_description = add_class_form.description.data

                try:
                    classroom = Classes(name=class_name, description=class_description)
                    db.session.add(classroom)
                    db.session.commit()
                    flash(f'Successfully created classroom {class_name}')
                    return redirect(url_for('admin_classes.admin_classes'))

                except SQLAlchemyError as error:
                    db.session.rollback()
                    return render_template('errors/500.html', title='Internal Error'), 500
                
            return render_template('admin/classes/add_class.html', title='Add Class', form=add_class_form, legend='Add Class')
    
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401

    else:
        flash('You must be logged in to add classes')
        return redirect(url_for('users.login'))
    
@admin_classes_bp.route('/admin/classes/<id>/update', methods=['GET', 'POST'])
@login_required
def update_class(id):
    if not current_user.is_anonymous:

        if current_user.is_admin:

            try:
                classroom = Classes.query.get_or_404(id)

            except SQLAlchemyError as error:
                return render_template('errors/500.html', title='Internal Error'), 500
            
            update_class_form = ClassUpdateForm(classroom.name)

            if update_class_form.validate_on_submit():
                classroom.name = update_class_form.name.data
                classroom.description = update_class_form.description.data
                db.session.commit()
                flash(f"Successfully updated classroom {classroom.name}")
                return redirect(url_for('admin_classes.admin_classes'))
            
            update_class_form.name.data = classroom.name
            update_class_form.description.data = classroom.description
            
            return render_template('admin/classes/add_class.html', title='Update Class', form=update_class_form,
                                   legend='Update Class', classroom=classroom)
    else:
        flash('You must be logged in to update classes')
        return redirect(url_for('users.login'))

@admin_classes_bp.route('/admin/classes/<id>/delete')
@login_required
def delete_class(id):
    if not current_user.is_anonymous:

        if current_user.is_admin:
            try:
                classroom = Classes.query.get_or_404(id)
                db.session.delete(classroom)
                db.session.commit()
                flash(f"Successfully deleted class {classroom.name}")
                return redirect(url_for('admin_classes.admin_classes'))

            except SQLAlchemyError as error:
                db.session.rollback()
                return render_template('errors/500.html', title='Internal Error'), 500

        else:
            return render_template('errors/401.html', title='Unauthorized'), 401

    else:
        flash('You must be logged in to delete classes')
        return redirect(url_for('users.login'))