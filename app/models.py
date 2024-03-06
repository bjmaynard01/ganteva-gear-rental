from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login
from sqlalchemy_utils import PhoneNumberType
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class GearCategory(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80), index=True)
    #description = db.Column(db.String(200), nullable=True)

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(80), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))

class Classes(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80), index=True)
    #description = db.column(db.String(200), nullable=True)

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(80), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))

class User(UserMixin, db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    #fname = db.Column(db.String(64), index=True)
    fname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    #lname = db.Column(db.String(120), index=True)
    lname: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    #email = db.Column(db.String(200), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(200), index=True, unique=True)
    phone = db.Column(PhoneNumberType(region='US', max_length=20))
    #password_hash = db.Column(db.String(256))
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    #confirmed = db.Column(db.Boolean, default=False)
    confirmed: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    #is_admin = db.Column(db.Boolean, default=False)
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fname', 'lname', 'email', 'phone', 'confirmed', 'is_admin')

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))