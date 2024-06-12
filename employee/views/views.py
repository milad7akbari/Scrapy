
from datetime import datetime

import requests
from flask import request, render_template, redirect, url_for, make_response, flash
from sqlalchemy.orm import joinedload
from werkzeug.security import check_password_hash

from employee import employee_bp, db
from employee.models.models import Employee, Access
from employee.utils.utils import showError, check_logged_in, cookie_and_jwt_required, sendPostRequest, \
    get_or_create_user
from flask_jwt_extended import create_access_token, create_refresh_token, unset_jwt_cookies, set_access_cookies, get_jwt_identity, set_refresh_cookies, jwt_required



@employee_bp.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@employee_bp.route('/login-employee', methods=['GET', 'POST'])
@check_logged_in
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember_me')

        if not email or not password or '@' not in email:
            return showError('Email or password are required and must be correct')

        employee = Employee.query.filter_by(email=email).first()
        if employee and check_password_hash(employee.password, password):
            remember = True if remember == 'on' else False
            access_token = create_access_token(identity=employee.id)
            refresh_token = create_refresh_token(identity=employee.id) if remember else None

            response = make_response(redirect(url_for('employee.dashboard')))
            set_access_cookies(response, access_token, max_age=3600 * 24 * 7)

            if remember:
                set_refresh_cookies(response, refresh_token)
            return response
        else:
            return showError('Employee not found')
    return render_template('auth/login.html')


@employee_bp.route('/user-register', methods=['GET'])
def users():
    access = Access.query.filter(
        Access.service_name == 'User',
        Access.access_expires > datetime.now()
    ).first()
    cookie = {
        "ACCESS_TOKEN": access.access_token,
    }
    context = {}
    data, response = sendPostRequest('http://127.0.0.1:5001/get-users', cookie=cookie, post=False, dest='users')
    if response.status_code != 200:
        flash(data['msg'], 'error')
    else:
        context['users'] = data['users']
    return render_template('users/dashboard.html', **context)



@employee_bp.route('/get-token-user', methods=['POST', 'GET'])
def token():
    if request.method == 'POST':
        data = {
            "username": request.form.get('username'),
            "password": request.form.get('password')
        }
        data, response = sendPostRequest(url="http://127.0.0.1:5001/access-token", cookie=None, headers=None, json=data)
        if response.status_code == 200:
            get_or_create_user(
                service_name='User',
                access_token=data['access_token'],
                refresh_token=data['refresh_token'],
                access_expires=data['access_expires'],
                refresh_expires=data['refresh_expires']
            )
            return redirect(url_for('employee.dashboard'))
        else:
            return showError(data['msg'], 'employee.token')
    return render_template('service/user.html')


@employee_bp.route('/refresh-token-user', methods=['GET'])
def refresh():
    employee = Access.query.filter(
        Access.service_name == 'User',
        Access.refresh_expires > datetime.now()
    ).first()
    if employee:
        cookie = {"refresh_token_cookie": employee.refresh_token}
        headers = {"X-CSRFToken": request.cookies.get('csrf_access_token')}
        data, response = sendPostRequest(cookie, headers)
        if response.status_code == 200:
            get_or_create_user(service_name='User', access_token=data['access_token'], access_expires=data['access_expires'])
            return redirect(url_for('employee.dashboard'))
        else:
            return showError(data['msg'], 'employee.token')
    else:
        return showError('Refresh Token Expired', 'employee.token')

@employee_bp.route('/dashboard', methods=['GET'])
@cookie_and_jwt_required
def dashboard():
    context = {}
    user_id = get_jwt_identity()
    try:
        employee = Employee.query.options(joinedload(Employee.role)).get(user_id)
        if employee is None:
            raise ValueError("employee not found")
    except Exception as e:
        raise ValueError("employee not found")
    context['employee'] = employee

    return render_template('dashboard/dashboard.html', **context)


@employee_bp.route('/logout')
@cookie_and_jwt_required
def logout():
    response = make_response(redirect(url_for('employee.login')))
    unset_jwt_cookies(response)
    return response
