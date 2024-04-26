from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import db
from app.users import bp as users_bp
from app.users.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm
from app.users.models import User
from sqlalchemy.exc import SQLAlchemyError
from app.users.utils import send_registration_mail, send_password_reset_email
import datetime

@users_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data.lower()
        user = db.session.scalar(
            sa.select(User).where(User.email == username))
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('users.login', title='Login'))
        
        try:
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.date.today()
            db.session.add(user)
            db.session.commit()

        except SQLAlchemyError as error:
            return 500
        
        return redirect(url_for('main.index', title='Home'))
    
    return render_template('users/login.html', title='Sign In', form=form)

@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    
    registration_form = RegistrationForm()
    
    if registration_form.validate_on_submit():
        
        f_name = registration_form.f_name.data.capitalize()
        l_name = registration_form.l_name.data.capitalize()
        email = registration_form.email.data.lower()
        phone = registration_form.phone.data
        password = registration_form.password.data
        create_date = datetime.date.today()
        cc = 'bryan@maynardfolks.com'
        
        try:
            user = User(fname=f_name, lname=l_name, email=email, phone=phone, create_date=create_date, last_login=create_date)
            user.set_password(password)                        
            db.session.add(user)
            db.session.commit()

            try:
                send_registration_mail([email], f_name, email, [cc])
            
            except Exception as error:
                return "Error encountered when trying to send email." + str(error)

        except SQLAlchemyError as error:
            db.session.rollback()
            return 500
        
        flash('Registration successful. Please be on the lookout for a confirmation email')
        
        return redirect(url_for('main.index', title='Home'))
    
    return render_template('users/register.html', title='Sign Up', form=registration_form)

@users_bp.route('/reset_password_request', methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index', title="Home"))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = db.session.query(User).filter_by(email=email).first()

        if user:
            token = user.generate_password_reset_token()
            reset_password_url = url_for('users.reset_password', token=token, user_id=user.id, _external=True)
            send_password_reset_email(user=user, reset_password_url=reset_password_url, user_email=user.email)

        flash(
            "Instructions to reset your password were sent to your email address,"
            " if a user account is found for your email address."
            
        )

        return redirect(url_for('users.login'))

    return render_template("users/reset_password_request.html", title="Request Password Reset", form=form)

@users_bp.route('/reset_password/<token>/<int:user_id>', methods=['GET', 'POST'])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.validate_password_reset_token(token, user_id)
    if not user:
        return render_template("errors/404.html", title="Page Not Found")
    
    form = PasswordResetForm()

    if form.validate_on_submit():
        try:
            user.set_password(form.password.data)
            db.session.commit()
            flash('Password successfully reset, please login with your new password.')
            return redirect(url_for('users.login'))

        except SQLAlchemyError as error:
            return 500
        
    return render_template("users/reset_password.html", title="Reset Password", form=form)

@users_bp.route('/user/<id>')
@login_required
def user(id):
    user = db.first_or_404(sa.select(User).where(User.id == current_user.id))
    return render_template('users/user.html', user=user)