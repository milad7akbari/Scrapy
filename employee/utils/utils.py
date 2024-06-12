import os
from datetime import datetime

import requests
from functools import wraps

from flask import request, redirect, url_for, flash, make_response
from flask_jwt_extended import decode_token, verify_jwt_in_request, get_jwt_identity, exceptions, unset_jwt_cookies
from dotenv import load_dotenv

from employee import db
from employee.models.models import Access
from sqlalchemy.orm.exc import NoResultFound

load_dotenv()

def cookie_and_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        cookie = request.cookies.get(os.getenv('JWT_COOKIE_NAME'))
        try:
            verify_jwt_in_request()
            jwt_identity = get_jwt_identity()
        except exceptions.NoAuthorizationError:
            return redirect(url_for('employee.login'))
        if not cookie or not jwt_identity:
            return redirect(url_for('employee.login'))
        return fn(*args, **kwargs)

    return wrapper


def get_or_create_user(service_name, access_token, access_expires, refresh_token=None, refresh_expires=None):
    access_expires = datetime.utcfromtimestamp(access_expires)
    if refresh_expires is not None:
        refresh_expires = datetime.utcfromtimestamp(refresh_expires)
    try:
        user = db.session.query(Access).filter_by(service_name=service_name).one()
        user.access_token = access_token
        user.access_expires = access_expires
        if refresh_token is not None:
            user.refresh_token = refresh_token
        if refresh_expires is not None:
            user.refresh_expires = refresh_expires
        db.session.commit()
    except NoResultFound:
        new_user = Access(
            service_name=service_name,
            access_token=access_token,
            refresh_token=refresh_token,
            access_expires=access_expires,
            refresh_expires=refresh_expires,
        )
        db.session.add(new_user)
        db.session.commit()

def sendPostRequest(url, post=True, cookie=None, headers=None, json=None, dest='token'):
    try:
        if post:
            response = requests.post(url, cookies=cookie, headers=headers, json=json)
        else:
            response = requests.get(url, cookies=cookie, headers=headers)
        data = response.json()
    except ConnectionError:
        return showError("Connection error", f'employee.{dest}')
    except requests.exceptions.HTTPError:
        return showError("HTTP error", f'employee.{dest}')
    except requests.exceptions.RequestException:
        return showError("Request error", f'employee.{dest}')
    except Exception:
        return showError("Unknown error", f'employee.{dest}')
    print('------------------------------------')
    print(data, response)
    print('------------------------------------')
    return data, response

def check_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get(os.getenv('JWT_COOKIE_NAME'))
        if token:
            try:
                decode_token(token)
                return redirect(url_for('employee.dashboard'))
            except Exception:
                response = make_response(redirect(url_for('employee.login')))
                unset_jwt_cookies(response)
                return response
        return f(*args, **kwargs)
    return decorated_function

def showError(msg, url_for_='employee.login'):
    flash(msg, 'error')
    return redirect(url_for(url_for_))


