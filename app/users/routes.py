
from flask import render_template, flash, redirect, url_for, Blueprint
from app.users.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app import db
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from app.models import User
from app.users.utils import send_registration_mail, clear_user_table

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
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
    
    return render_template('login.html', title='Sign In', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/register', methods=['GET', 'POST'])
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
        
        return redirect(url_for('main.index', user=f_name))
    
    return render_template('register.html', title='Sign Up', form=registration_form)

@users.route('/user/<id>')
@login_required
def user(id):
    user = db.first_or_404(sa.select(User).where(User.id == id))

    return render_template('user.html', user=user)

@users.route('/clear-user-table')
@login_required
def clear_users():
    clear_user_table()
    flash('User table cleared successfully.')
    return redirect(url_for('main.index'))