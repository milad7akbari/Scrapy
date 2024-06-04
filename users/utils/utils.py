from functools import wraps

from flask import request, redirect, url_for, make_response, flash
from flask_jwt_extended import decode_token

from users.models.models import User


def showError(msg, red='users.register'):
    flash(msg, 'error')
    return redirect(url_for(red))
def get_token_or_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('ACCESS_TOKEN')
        try:
            decoded_token = decode_token(token)
            return redirect('127.0.0.5002/home')
        except:
            return f(*args, **kwargs)
    return decorated_function
def get_user_or_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('ACCESS_TOKEN', None)
        csrf_token = request.cookies.get('csrf_access_token')
        if not token or not csrf_token:
            return redirect(url_for('users.login'))
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']['user_id']
        check = User.query.filter_by(id=user_id, active=1).count()
        if check > 0:
            return f(user_id, *args, **kwargs)
        resp = make_response(redirect(url_for('users.login')))
        resp.set_cookie('ACCESS_TOKEN', '', expires=0)
        resp.set_cookie('csrf_access_token', '', expires=0)
        return resp
    return decorated_function
