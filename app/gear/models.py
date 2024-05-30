from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

gear_categories_ref = db.Table('gear_categories_ref',
                           sa.Column('item_id', sa.Integer, sa.ForeignKey('gear_categories.id')),
                           sa.Column('category_id', sa.Integer, sa.ForeignKey('gear_item.id'))
                           )

class GearCategories(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(80), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))
    items = db.relationship('GearItem', secondary=gear_categories_ref, backref=db.backref('categories', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"Gear_Category('{self.id}', '{self.name}', '{self.description}')"

class GearCategoriesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class GearItem(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[int] = so.mapped_column(sa.String(64), index=True, unique=True)
    image: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    img_thumb: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    care_instructions: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    qty: so.Mapped[str] = so.mapped_column(sa.Integer, default=0, nullable=True)
    qty_available: so.Mapped[int] = so.mapped_column(sa.Integer, default=0, nullable=True)
    qty_out: so.Mapped[int] = so.mapped_column(sa.Integer, default=0, nullable=True)

    def __repr__(self):
        return f"Gear_Item('{self.id}', '{self.name}', '{self.qty_available}')"
    

class GearItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'image', 'img_thumb', 'care_instructions', 'qty')
        



