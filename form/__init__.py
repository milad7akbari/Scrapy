from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import MetaData


metadata = MetaData(
  naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    }
)
db = SQLAlchemy(metadata=metadata)
jwt = JWTManager()
csrf = CSRFProtect()

form_bp: Blueprint = Blueprint(
    'form',
    __name__,
    template_folder='templates',
    static_folder='static/',
    static_url_path='/static/form'
)
from form.namespace import api




