from dotenv import load_dotenv
from flask import request, url_for, redirect, flash, render_template, session, make_response
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_restx import Namespace, Resource
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from users.utils.utils import showError
from users import users_bp, db
from users.models.models import User, Countries, Children
from users.utils.utils import get_token_or_login, get_user_or_login

users_ns = Namespace('Login', description='Users Data')
load_dotenv()

@users_ns.route('/user')
class Users(Resource):
    def get(self):
        return redirect(url_for('users.login'))

@users_bp.route('/login-user', methods=['GET', 'POST'])
@get_token_or_login
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if (not email or not password) and '@' not in email:
            return showError('Email and password are required and must be correct', 'users.login')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity={'user_id': user.id}, fresh=True)
            response = make_response(redirect('http://127.0.0.1:5002/home'))
            set_access_cookies(response, access_token, max_age=3600)
            return response
        else:
            return showError('User not found', 'users.login')
    return render_template('login.html')


@users_bp.route('/dashboard', methods=['GET'])
@get_user_or_login
def dashboard(user_id):
    context = {}
    try:
        user = User.query.options(joinedload(User.group), joinedload(User.user_children), joinedload(User.country)).get(user_id)
        if user is None:
            raise ValueError("User not found")
    except Exception as e:
        raise ValueError("User not found")
    context['user'] = user
    context['details'] = None
    context['education'] = None
    cookies = {
        'ACCESS_TOKEN': request.cookies.get('ACCESS_TOKEN'),
        'csrf_access_token': request.cookies.get('csrf_access_token'),
    }

    response = requests.get("http://127.0.0.1:5001/user/info/", cookies=cookies)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['status'] == 'success':
            context['details'] = response_data['details']
            context['education'] = response_data['education']


    template_name = 'dashboard.html' if user.group.name == 'Users' else 'admin.html'
    return render_template(template_name, **context)


@users_bp.route('/register-user', methods=['GET', 'POST'])
@get_token_or_login
def register():
    if request.method == 'POST':
        session['form_data'] = request.form.to_dict()
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        country_id = request.form.get('country_id')
        marital_status = request.form.get('marital_status')
        children = request.form.get('children')
        country_check = Countries.query.filter_by(id=country_id).first()
        if country_check is None:
            return showError("Country does not exist.")
        if lastname is None:
            return showError('Last Name cannot be empty.')
        if len(password) <= 3:
            return showError('Password cannot be empty.')
        if marital_status is None or marital_status not in ['0', '1', '2', '3']:
            return showError('Marital status cannot be empty.')
        elif marital_status == '2' and children not in ['0', '1', '2', '3']: # Married
            return showError('Children must be defined.')

        if firstname is None:
            return showError('First Name cannot be empty.')
        if '@' not in email:
            return showError('Please enter a valid email address.')

        email_check = User.query.filter_by(email=email).first()
        if email_check is not None:
            return showError('Email address already exists.')
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, group_id=1, firstname=firstname, lastname=lastname, country_id=country_id, married=marital_status)
        db.session.add(new_user)
        db.session.commit()
        if marital_status == '2' and children in ['3', '1', '2']:
            children_obj = Children(user_id=new_user.id, count=children)
            db.session.add(children_obj)
            db.session.commit()
        flash('User Successfully Registered', 'info')
        return redirect(url_for('users.login'))
    countries = Countries.query.filter_by(active=1).order_by('name').all()
    form_data = session.pop('form_data', {})
    context = {
        'countries': countries,
        'form_data': form_data,
    }
    return render_template('register.html', **context)
