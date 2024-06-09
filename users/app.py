import datetime
import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate

from . import users_bp, db, jwt

load_dotenv()

def create_app():
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'

    app = Flask(__name__)


    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    app.config['JWT_COOKIE_MAX_AGE'] = 3600 * 24
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_COOKIE_SECURE'] = True
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_CSRF_CHECK_FORM'] = True
    app.config['JWT_COOKIE_SAMESITE'] = 'Strict'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'ACCESS_TOKEN'

    jwt.init_app(app)
    db.init_app(app)
    app.register_blueprint(users_bp, url_prefix='/')
    Migrate(app, db, render_as_batch=True)
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000)
