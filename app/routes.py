from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app, db
from app.forms import LoginForm, RegistrationForm
from funcs import send_registration_mail
from werkzeug.security import generate_password_hash
from app.models import User
from sqlalchemy.exc import SQLAlchemyError

@app.route('/')
@app.route('/index')
def index():
    user = request.args.get('user')
    referrer = request.referrer
    if user and referrer.endswith('/register'):
        return render_template('index.html', title='Home', user=user)
    else:
        return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        flash('Login requested for user {}, remember_me={}'.format(
            username, form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    registration_form = RegistrationForm()
    
    if registration_form.validate_on_submit():
        
        f_name = registration_form.f_name.data.capitalize()
        l_name = registration_form.l_name.data.capitalize()
        email = registration_form.email.data.lower()
        phone = registration_form.phone.data
        cc_to = 'bryan@maynardfolks.com'
        password_hash = generate_password_hash(registration_form.password.data)
        
        flash('Registration successful. Please be on the lookout for a confirmation email')
        try:
            user = User(fname=f_name, lname=l_name, email=email, phone=phone, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()

            try:
                send_registration_mail([email], f_name, email, cc_to)
            
            except Exception as error:
                return "Error encountered when trying to send email." + str(error)

        except SQLAlchemyError as error:
            return "Unable to execute database operations due to: " + str(error)
        
        return redirect(url_for('index', user=f_name))
    
    return render_template('register.html', title='Sign Up', form=registration_form)



@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])