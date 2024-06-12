from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_jwt_extended import JWTManager


sqlite_naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=sqlite_naming_convention)
db = SQLAlchemy(metadata=metadata)

jwt = JWTManager()

employee_bp = Blueprint(
    'employee',
    __name__,
    template_folder='templates',
    static_folder='static/',
    static_url_path='/static/users'
)

from employee.namespace import api
