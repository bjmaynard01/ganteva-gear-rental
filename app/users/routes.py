from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import db
from app.users import bp as users_bp
from app.users.forms import LoginForm, RegistrationForm
from app.models import User
from sqlalchemy.exc import SQLAlchemyError
from app.users.utils import send_registration_mail

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
            return redirect(url_for('users.login'))
        
        login_user(user, remember=form.remember_me.data)
        flash('Succesfully logged user in.')
        
        return redirect(url_for('main.index'))
    
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
        cc = 'bryan@maynardfolks.com'
        
        try:
            user = User(fname=f_name, lname=l_name, email=email, phone=phone)
            user.set_password(password)                        
            db.session.add(user)
            db.session.commit()

            try:
                send_registration_mail([email], f_name, email, [cc])
            
            except Exception as error:
                return "Error encountered when trying to send email." + str(error)

        except SQLAlchemyError as error:
            return 500
        
        flash('Registration successful. Please be on the lookout for a confirmation email')
        
        return redirect(url_for('main.index'))
    
    return render_template('users/register.html', title='Sign Up', form=registration_form)

@users_bp.route('/user/<id>')
@login_required
def user(id):
    user = db.first_or_404(sa.select(User).where(User.id == id))

    return render_template('users/user.html', user=user)