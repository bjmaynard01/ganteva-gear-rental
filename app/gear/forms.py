from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from flask_wtf.file import FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import InputRequired, ValidationError
from app.admin.gear.utils import get_category_names
from app.gear.models import GearCategories, GearItem
from flask import flash

class GearCategoryForm(FlaskForm):
    name = StringField('Category Name:', validators=[InputRequired()])
    desc = StringField('Category Description:')
    submit = SubmitField('Create Category')

    def validate_name(self, name):
        category = GearCategories.query.filter_by(name=name.data.title()).first()
        if category is not None:
            raise ValidationError('Category already exists')
            
class UpdateGearCategoryForm(FlaskForm):
    name = StringField('Category Name:', validators=[InputRequired()])
    desc = StringField('Category Description:')
    submit = SubmitField('Update Category')

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            category = GearCategories.query.filter_by(name=name.data.title()).first()
            if category:
                raise ValidationError('Category already exists')


class GearItemForm(FlaskForm):
    name = StringField('Item Name:', validators=[InputRequired()])
    image = FileField('Item Image:', validators=[FileAllowed(['jpg', 'png', 'jpeg'])]) # add validators later, multiple regex to limit extensions
    care_instructions = TextAreaField('Care Instructions:')
    qty = StringField('Quantity:')
    categories = QuerySelectMultipleField('Categories:', query_factory=get_category_names, get_label="name")                      
    submit = SubmitField('Submit')

    def validate_name(self, name):
        item = GearItem.query.filter_by(name=name.data.title()).first()
        if item is not None:
            raise ValidationError('Item already exists')
        
class UpdateGearItemForm(FlaskForm):
    name = StringField('Item Name:', validators=[InputRequired()])
    image = FileField('Item Image:', validators=[FileAllowed(['jpg', 'png', 'jpeg'])]) # add validators later, multiple regex to limit extensions
    care_instructions = TextAreaField('Care Instructions:')
    qty = StringField('Quantity:')
    categories = QuerySelectMultipleField('Categories:', query_factory=get_category_names, get_label="name")                      
    submit = SubmitField('Update')

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            item = GearItem.query.filter_by(name=name.data.title()).first()
            if item:
                raise ValidationError('Item already exists')
