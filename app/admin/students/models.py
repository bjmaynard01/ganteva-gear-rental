from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_marshmallow import Marshmallow
import datetime
from app.admin.classes.models import Classes
from app.users.models import User

ma = Marshmallow()

class Student(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    create_date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(80), index=True)
    birthday: so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True, nullable=True)

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'create_date', 'first_name', 'last_name', 'birthday')
