from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import InputRequired, ValidationError
from app.gear.utils import get_category_names
from app.gear.models import GearCategories, GearItem

class GearCategoryForm(FlaskForm):
    name = StringField('Category Name:', validators=[InputRequired()])
    desc = StringField('Category Description:')
    submit = SubmitField('Create Category')

    def validate_name(self, category_name):
        category = GearCategories.query.filter_by(name=self.name.data.capitalize()).first()

        if category is not None:
            raise ValidationError('Category already exists')


class GearItemForm(FlaskForm):
    item_name = StringField('Item Name:', validators=[InputRequired()])
    item_image = FileField('Item Image:') # add validators later, multiple regex to limit extensions
    item_care = TextAreaField('Care Instructions:')
    qty = StringField('Quantity:')
    categories = QuerySelectMultipleField('Categories:', query_factory=get_category_names, get_label="name")                      
    submit = SubmitField('Submit')
