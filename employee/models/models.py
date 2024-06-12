import uuid
from datetime import datetime
from flask_login import UserMixin
from employee import db

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Access(db.Model):
    __tablename__ = 'access'
    id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    service_name = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(2048), nullable=False)
    refresh_token = db.Column(db.String(2048), nullable=False)
    access_expires = db.Column(db.DateTime)
    refresh_expires = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class Employee(db.Model, UserMixin):
    __tablename__ = 'employee'
    id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.relationship('Role', backref=db.backref('employees', lazy=True))
