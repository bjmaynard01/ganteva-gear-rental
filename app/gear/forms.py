from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import InputRequired, ValidationError
from app.gear.utils import get_category_names

class GearCategoryForm(FlaskForm):
    category_name = StringField('Category Name:', validators=[InputRequired()])
    category_desc = StringField('Category Description:')
    submit = SubmitField('Submit')


class GearItemForm(FlaskForm):
    item_name = StringField('Item Name:', validators=[InputRequired()])
    item_image = FileField('Item Image:') # add validators later, multiple regex to limit extensions
    item_care = TextAreaField('Care Instructions:')
    qty = StringField('Quantity:')
    categories = QuerySelectMultipleField('Categories:', query_factory=get_category_names, allow_blank=True, get_label="name")                      
