from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class GearCategories(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(80), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))

class GearCategoriesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class GearItem(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[int] = so.mapped_column(sa.String(64), index=True)

