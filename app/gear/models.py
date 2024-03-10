from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.declarative import declarative_base

ma = Marshmallow()
Base= declarative_base()

gear_category = db.Table(
    "gear_category",
    db.Column('category_id', db.Integer, db.ForeignKey('gear_item.id'), primary_key=True),
    db.Column('gear_id', db.Integer, db.ForeignKey('gear_categories.id'), primary_key=True)
)
class GearCategories(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(80), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))
    gear_items = so.relationship('GearItem', secondary=gear_category, backref='categories')

class GearCategoriesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class GearItem(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[int] = so.mapped_column(sa.String(64), index=True)
    image: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    care_instructions: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    qty: so.Mapped[int] = so.mapped_column(default=0)
    categories = so.relationship('GearCategories', secondary=gear_category, backref='gear_items')



