from datetime import datetime
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Fio(db.Model):
    __tablename__ = 'fios'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    marca = db.Column(db.String, nullable=True)
    cor = db.Column(db.String, nullable=True)
    espessura = db.Column(db.String, nullable=True)
    gramas = db.Column(db.Integer, default=0)
    foto = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship(User, backref='fios')
