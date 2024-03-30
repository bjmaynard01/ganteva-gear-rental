from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, BooleanField, PasswordField
from wtforms_alchemy import PhoneNumberField
from wtforms.validators import Email, InputRequired, Length, ValidationError, EqualTo
from app.users.models import User
from flask import flash
from flask_login import current_user

class UserAdminForm(FlaskForm):
    f_name = StringField('First Name:', validators=[InputRequired()])
    l_name = StringField('Last Name:', validators=[InputRequired()])
    email = EmailField('EMail:', validators=[InputRequired(), Email()])
    phone = PhoneNumberField('Phone:', validators=[InputRequired()], region="US", display_format='national')
    confirmed = BooleanField('Confirmed:')
    password = PasswordField('New Password:', validators=[EqualTo('confirm_pass', message="Password and Confirm Password fields must match.")])
    confirm_pass = PasswordField('Confirm Password:')
    admin = BooleanField('Admin:')
    submit = SubmitField('Update User')

    def __init__(self, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data.lower()).first()
            if user:
                raise ValidationError('That email is already in use')