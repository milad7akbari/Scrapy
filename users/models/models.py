import uuid
from datetime import datetime

from users import db

class Countries(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    country_id = db.Column(db.SmallInteger, db.ForeignKey('countries.id'), nullable=True)
    group_id = db.Column(db.SmallInteger, db.ForeignKey('group.id'), default=1)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    active = db.Column(db.Boolean, default=True)
    married = db.Column(db.SmallInteger, default=False, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    country = db.relationship('Countries', backref=db.backref('users', lazy=True))
    group = db.relationship('Group', backref=db.backref('users', lazy=True), )


class Children(db.Model):
    __tablename__ = 'user_children'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    count = db.Column(db.SmallInteger, nullable=False)

    user = db.relationship('User', backref=db.backref('user_children', lazy=True))

    def __repr__(self):
        return f'<UserChildren {self.count}>'
