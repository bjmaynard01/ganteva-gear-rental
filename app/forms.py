from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms_alchemy import PhoneNumberField
from wtforms.validators import Email, EqualTo, InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me:')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    f_name = StringField('First Name:', validators=[InputRequired()])
    l_name = StringField('Last Name:', validators=[InputRequired()])
    email = EmailField('Email:', validators=[InputRequired(), Email()])

    phone = PhoneNumberField('Phone:', validators=[InputRequired()], region="US",\
                             display_format='national')
    
    password = PasswordField('Password:', validators=[InputRequired(), EqualTo('confirm_pass',\
                             message="Passwords must match."), Length(min=8, \
                             message='Password must be at least 8 characters in length.')])
    
    confirm_pass = PasswordField('Confirm Password:', validators=[InputRequired()])
    submit = SubmitField('Sign Up')