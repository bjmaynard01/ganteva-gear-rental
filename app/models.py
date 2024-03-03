from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    fname: so.Mapped[str] = so.mapped_column(sa.String[64], index=True)
    lname: so.Mapped[str] = so.mapped_column(sa.String[120], index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String[120], index=True, unique=True)
    username: so.Mapped[str] = so.mapped_column(sa.String[120], index=True, unique=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String[15], index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String[256])

    def __repr__(self):
        return '<User {}'