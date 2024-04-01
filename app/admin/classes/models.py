from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class Classes(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(180))

    def __repr__(self):
        return f"Classroom('{self.id}', '{self.name}', '{self.description}')"
    
class ClassesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')