from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app, db
from app.forms import LoginForm, RegistrationForm
from funcs import send_registration_mail, clear_user_table
from app.models import User
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa


@app.route('/')
@app.route('/index')
def index():

    if current_user.is_authenticated:
        return render_template('index.html', title='Home', user=current_user)
    else:
        return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data.lower()
        user = db.session.scalar(
            sa.select(User).where(User.email == username))
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        flash('Succesfully logged user in.')
        
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
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
        
        return redirect(url_for('index', user=f_name))
    
    return render_template('register.html', title='Sign Up', form=registration_form)

@app.route('/user/<id>')
@login_required
def user(id):
    user = db.first_or_404(sa.select(User).where(User.id == id))

    return render_template('user.html', user=user)


@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])