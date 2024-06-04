import os

from flask import Flask

from dotenv import load_dotenv
from flask_migrate import Migrate

from . import form_bp, jwt, db

load_dotenv()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'ACCESS_TOKEN'
    app.config['JWT_CSRF_REQUEST_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_CSRF_CHECK_FORM'] = True
    jwt.init_app(app)
    db.init_app(app)
    app.register_blueprint(form_bp, url_prefix='/')

    Migrate(app, db)
    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5001, debug=True)