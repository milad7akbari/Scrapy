from flask import redirect, request, jsonify
from flask_restx import Namespace, Resource
login_ns = Namespace('Login', description='Do not use manual action: Try it Out')

@login_ns.route('login')
class Login(Resource):
    def get(self):
        if request.content_type is None:
            return redirect('/login-employee')
        else:
            return jsonify({"message": "Fetch url by your browser"})
