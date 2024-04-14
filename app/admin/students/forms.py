from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, DateField, BooleanField
from wtforms.validators import InputRequired, ValidationError
from app.admin.students.models import Student
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms import widgets
from app.admin.classes.utils import get_classes

class AddStudentForm(FlaskForm):
    first_name = StringField('First Name:', validators=[InputRequired()])
    last_name = StringField('Last Name:', validators=[InputRequired()])
    birthday = DateField('Date of Birth:')
    classes = QuerySelectMultipleField('Classes:', validators=[InputRequired()], query_factory=get_classes, get_label='name')
    submit = SubmitField('Create Student')

class UpdateStudentForm(FlaskForm):
    first_name = StringField('First Name:', validators=[InputRequired()])
    last_name = StringField('Last Name:', validators=[InputRequired()])
    birthday = DateField('Date of Birth:')
    classes = QuerySelectMultipleField('Classes:', validators=[InputRequired()], query_factory=get_classes, get_label='name')
    submit = SubmitField('Update')