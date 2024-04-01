from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError
from app.admin.classes.models import Classes

class ClassAddForm(FlaskForm):
    name = StringField('Class Name:', validators=[InputRequired()])
    description = StringField('Description:')
    submit = SubmitField('Create Class')

    def validate_name(self, name):
        classroom = Classes.query.filter_by(name=name.data.title()).first()
        if classroom is not None:
            raise ValidationError('Class with that name already exists')
        
class ClassUpdateForm(FlaskForm):
    name = StringField('Class Name:', validators=[InputRequired()])
    description = StringField('Description:')
    submit = SubmitField('Update Class')

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name
    
    def validate_name(self, name):
        if name.data != self.original_name:
            classroom = Classes.query.filter_by(name=name.data.title()).first()
            if classroom:
                raise ValidationError('Class with that name already exists')