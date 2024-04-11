from app.admin.classes import bp as admin_classes_bp
from flask import render_template, url_for, redirect, flash, current_app
from app import db
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from app.admin.classes.models import Classes, DaysOfWeek
from app.admin.classes.forms import ClassAddForm, ClassUpdateForm
from datetime import date

@admin_classes_bp.route('/admin/classes')
@login_required
def admin_classes():
    if not current_user.is_anonymous:

        if current_user.is_admin == True:
            try:
                classes = Classes.query.all()      
                return render_template('admin/classes/admin_classes.html', title='Class Administration', 
                                       classes=classes), 200
            
            except SQLAlchemyError as error:
                return 500

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
                today = date.today()
                class_name = add_class_form.name.data.title()
                class_description = add_class_form.description.data.capitalize()
                start_date = add_class_form.start_date.data
                end_date = add_class_form.end_date.data
                morning = add_class_form.morning.data
                afternoon = add_class_form.afternoon.data
                days = add_class_form.days.data

                try:
                    classroom = Classes(create_date=today, name=class_name, description=class_description, start_date=start_date, 
                                        end_date=end_date, morning=morning, afternoon=afternoon)
                    
                    for day in days:
                        classroom.daysofweek.append(day)
                    
                    db.session.add(classroom)
                    db.session.commit()
                    flash(f'Successfully created classroom {class_name}')
                    return redirect(url_for('admin_classes.admin_classes'))

                except SQLAlchemyError as error:
                    db.session.rollback()
                    return render_template('errors/500.html', title='Internal Error', error=error), 500
                
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
            #update_class_form.days.query = DaysOfWeek.query.all()

            if update_class_form.validate_on_submit():
                classroom.name = update_class_form.name.data.title()
                classroom.description = update_class_form.description.data.capitalize()
                classroom.start_date = update_class_form.start_date.data
                classroom.end_date = update_class_form.end_date.data
                classroom.morning = update_class_form.morning.data
                classroom.afternoon = update_class_form.afternoon.data
                classroom.daysofweek = update_class_form.days.data

                db.session.commit()
                flash(f"Successfully updated classroom {classroom.name}")
                return redirect(url_for('admin_classes.admin_classes'))
            
            update_class_form.name.data = classroom.name
            update_class_form.description.data = classroom.description
            update_class_form.start_date.data = classroom.start_date
            update_class_form.end_date.data = classroom.end_date
            update_class_form.morning.data = classroom.morning
            update_class_form.afternoon.data = classroom.afternoon
            update_class_form.days.data = classroom.daysofweek
            
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