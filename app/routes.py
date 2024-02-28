from flask import render_template, flash, redirect, url_for, request
from app import app, models
from app.forms import LoginForm, RegistrationForm
from funcs import send_mail

@app.route('/')
@app.route('/index')
def index():
    user = request.args.get('user')
    referrer = request.referrer
    #user = {'username': 'Bryan'}
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
        flash('Registration successful for {} {}, with an email of {}, a phone number of {}, and a password of {}.'.format(
            f_name, 
            l_name, 
            email, 
            registration_form.phone.data, 
            registration_form.password.data))
        try:
            send_mail(email, f_name, 'Thank You for Registering with GanTeva\'s Gear Rental Site')
        except Exception as error:
            return "Error encountered when trying to send email.", error
        return redirect(url_for('index', user=f_name))
    return render_template('register.html', title='Sign Up', form=registration_form)