from app.admin.students import bp as admin_students_bp
from flask import render_template, url_for, redirect, flash, current_app, request
from app import db
from flask_login import current_user, login_required
from app.admin.students.models import Student
from sqlalchemy.exc import SQLAlchemyError
from app.admin.students.forms import AddStudentForm, UpdateStudentForm
from datetime import date
from app.admin.classes.models import Classes

@admin_students_bp.route('/admin/students')
@login_required
def admin_students():
    if not current_user.is_anonymous:

        if current_user.is_admin:
            try:
                page = request.args.get('page', 1, type=int)
                students = Student.query.order_by(Student.last_name).paginate(page=page, per_page=10)
                all_students = Student.query.all()
                total_students = len(all_students)
                return render_template('admin/students/admin_students.html', title='Student Administration',
                                       students=students, total_students=total_students, page=page)
            except SQLAlchemyError as error:
                return 500

        else:
            return 401

    else:
        flash('You must be logged in to administer students')
        return redirect(url_for('users.login'))
    
@admin_students_bp.route('/admin/students/add', methods=["GET", "POST"])
@login_required
def add_student():
    if not current_user.is_anonymous:

        if current_user.is_admin:

            add_student_form = AddStudentForm()

            if add_student_form.validate_on_submit():
                today = date.today()
                first_name = add_student_form.first_name.data.title()
                last_name = add_student_form.last_name.data.title()
                birthday = add_student_form.birthday.data
                classes = add_student_form.classes.data

                try:
                    student = Student(create_date=today, first_name=first_name, last_name=last_name, birthday=birthday, last_modified=today)
                    for classroom in classes:
                        classroom.students.append(student)
                    db.session.add(student)
                    db.session.commit()
                    flash(f'Successfully added student {first_name} {last_name}')
                    return redirect(url_for('admin_students.admin_students'))
                
                except SQLAlchemyError as error:
                    db.session.rollback()
                    return 500
                
            return render_template('/admin/students/add_student.html', title='Add Student', form=add_student_form,
                                   legend='Add Student')

        else:
            return 401

    else:
        flash('You must be logged in to add students')
        return redirect(url_for('users.login'))

@admin_students_bp.route('/admin/students/<id>/update', methods=["GET", "POST"])
@login_required
def update_student(id):
    if not current_user.is_anonymous:

        if current_user.is_admin:
            try:
                student = Student.query.get_or_404(id)

            except SQLAlchemyError as error:
                 db.session.rollback()
                 return 500
            
            update_student_form = UpdateStudentForm()

            if update_student_form.validate_on_submit():
                student.first_name = update_student_form.first_name.data.title()
                student.last_name = update_student_form.last_name.data.title()
                student.birthday = update_student_form.birthday.data
                student.classes = update_student_form.classes.data
                student.last_modified = date.today()

                try:
                    db.session.commit()
                    flash(f"Successfully updated student {student.first_name} {student.last_name}")
                    return redirect(url_for('admin_students.admin_students'))

                except:
                    db.session.rollback()
                    return 500
                
            update_student_form.first_name.data = student.first_name
            update_student_form.last_name.data = student.last_name
            update_student_form.birthday.data = student.birthday
            update_student_form.classes.data = student.classes

            return render_template('/admin/students/add_student.html', title='Update Student', form=update_student_form,
                                   legend='Update Student', student=student )

        else:
            return 401

    else:
        flash('You must be logged in to update a student.')
        return redirect(url_for('users.login'))

@admin_students_bp.route('/admin/students/<id>/delete')
@login_required
def delete_student(id):
    if not current_user.is_anonymous:

        if current_user.is_admin:
            try:
                student = Student.query.get_or_404(id)
                db.session.delete(student)
                db.session.commit()
                flash(f'Successfully deleted student {student.first_name} {student.last_name}')
                return redirect(url_for('admin_students.admin_students'))

            except SQLAlchemyError as error:
                db.session.rollback()
                return 500

        else:
            return 401

    else:
        flash(f"You must be logged in to delete students.")
        return redirect(url_for('users.login'))

