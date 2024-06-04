from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from sqlalchemy import MetaData

sqlite_naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=sqlite_naming_convention)
jwt = JWTManager()
db = SQLAlchemy(metadata=metadata)

users_bp = Blueprint(
    'users',
    __name__,
    template_folder='templates',
    static_folder='static/',
    static_url_path='/static/users'
)
api = Api(
    users_bp,
    title='Users',
    version='1.0',
    doc='/doc',
    description='Desc'
)

from users.views.views import users_ns

api.add_namespace(users_ns, path='login')
