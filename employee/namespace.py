from flask_restx import Api
from employee import employee_bp
from employee.views.ns_view import login_ns

api = Api(
    employee_bp,
    title='Employee',
    version='1.0',
    doc='/doc',
    description='Desc'
)

api.add_namespace(login_ns, path='/')
