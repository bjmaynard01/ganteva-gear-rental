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

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    fname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    lname: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(200), index=True, unique=True)
    phone = db.Column(PhoneNumberType(region='US', max_length=20))
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    confirmed: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
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