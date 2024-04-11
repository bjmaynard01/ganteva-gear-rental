from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, DateField, BooleanField
from wtforms.validators import InputRequired, ValidationError
from app.admin.classes.models import Classes
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from app.admin.classes.utils import get_days_of_week
from wtforms import widgets


class ClassAddForm(FlaskForm):
    name = StringField('Class Name:', validators=[InputRequired()])
    description = StringField('Description:')
    start_date = DateField('Start Date:', validators=[InputRequired()])
    end_date = DateField('End Date:', validators=[InputRequired()])
    morning = BooleanField('AM:')
    afternoon = BooleanField('PM:')
    days = QuerySelectMultipleField('Days of Week:', validators=[InputRequired()], query_factory=get_days_of_week, get_label="day")
    submit = SubmitField('Create Class')

    def validate_name(self, name):
        classroom = Classes.query.filter_by(name=name.data.title()).first()
        if classroom is not None:
            raise ValidationError('Class with that name already exists')
        
    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError('End date must not be before start date')
        
class ClassUpdateForm(FlaskForm):
    name = StringField('Class Name:', validators=[InputRequired()])
    description = StringField('Description:')
    start_date = DateField('Start Date:')
    end_date = DateField('End Date:')
    morning = BooleanField('AM:')
    afternoon = BooleanField('PM:')
    days = QuerySelectMultipleField('Days of Week:', validators=[InputRequired()], query_factory=get_days_of_week, get_label="day")
    submit = SubmitField('Update Class')

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name
    
    def validate_name(self, name):
        if name.data != self.original_name:
            classroom = Classes.query.filter_by(name=name.data.title()).first()
            if classroom:
                raise ValidationError('Class with that name already exists')
            
    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError('End date must not be before start date')