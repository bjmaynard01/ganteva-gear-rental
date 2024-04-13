from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, DateField, BooleanField
from wtforms.validators import InputRequired, ValidationError
from app.admin.students.models import Student
from wtforms import widgets

class AddStudentForm(FlaskForm):
    first_name = StringField('First Name:', validators=[InputRequired()])
    last_name = StringField('Last Name:', validators=[InputRequired()])
    birthday = DateField('Date of Birth:')
    submit = SubmitField('Create Student')

class UpdateStudentForm(FlaskForm):
    first_name = StringField('First Name:', validators=[InputRequired()])
    last_name = StringField('Last Name:', validators=[InputRequired()])
    birthday = DateField('Date of Birth:')
    submit = SubmitField('Update')