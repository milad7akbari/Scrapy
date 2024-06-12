from flask_restx import Api
from form import form_bp
from form.views.ns_view import data_ns

api = Api(
    form_bp,
    title='Users',
    version='1.0',
    doc='/doc',
    description='Desc'
)

api.add_namespace(data_ns, path='/user/info')
