from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_restx import Api
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

form_bp = Blueprint(
    'form',
    __name__,
    template_folder='templates',
    static_folder='static/',
    static_url_path='/static/form'
)

api = Api(
    form_bp,
    title='Users',
    version='1.0',
    doc='/doc',
    description='Desc'
)

from form.views.views import data_ns

api.add_namespace(data_ns, path='data/get')
