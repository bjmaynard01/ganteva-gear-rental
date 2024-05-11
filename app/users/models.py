from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login
from sqlalchemy_utils import PhoneNumberType
from flask_marshmallow import Marshmallow
import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous import BadSignature, SignatureExpired
from flask import current_app

ma = Marshmallow()

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    create_date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)
    last_login: so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)
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
    
    def generate_password_reset_token(self):
        serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
        return serializer.dumps(self.email, salt=self.password_hash)
    
    @staticmethod
    def validate_password_reset_token(token: str, user_id: str):
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            return None
        
        serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
        try:
            token_user_email = serializer.loads(
                token,
                max_age=current_app.config.get('RESET_PASS_TOKEN_MAX_AGE'),
                salt = user.password_hash
            )

        except (BadSignature, SignatureExpired):
            return None
        
        return user
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fname', 'lname', 'email', 'phone', 'confirmed', 'is_admin')

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))