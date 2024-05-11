from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_marshmallow import Marshmallow
import datetime

ma = Marshmallow()

classes_days_ref = db.Table(
    'classes_days_ref',
    sa.Column('classes_id', sa.Integer, sa.ForeignKey('days_of_week.id')),
    sa.Column('days_id', sa.Integer, sa.ForeignKey('classes.id'))
)

classes_students_ref = db.Table(
    'classes_students_ref',
    sa.Column('classes_id', sa.Integer, sa.ForeignKey('student.id')),
    sa.Column('student_id', sa.Integer, sa.ForeignKey('classes.id'))
)

class Classes(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    create_date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(180))
    start_date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)
    end_date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)
    morning: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    afternoon: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    daysofweek = db.relationship('DaysOfWeek', secondary=classes_days_ref, backref=db.backref('classes', lazy='dynamic'), lazy='dynamic')
    students = db.relationship('Student', secondary=classes_students_ref, backref=db.backref('classes', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"Classroom('{self.create_date}', '{self.name}', '{self.description}', '{self.start_date}', '{self.end_date}')"
class ClassesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'create_date', 'name', 'description', 'start_date', 'end_date', 'morning', 'afternoon', 'daysofweek')


class DaysOfWeek(db.Model):
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    day: so.Mapped[str] = so.mapped_column(sa.String(3))

    def __repr__(self):
        return f"Days:('{self.id}', '{self.day}')"