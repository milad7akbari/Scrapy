import os
import re
from functools import wraps

import jwt
from dotenv import load_dotenv

from form.models.models import UserEducation
from flask import redirect, request, make_response, url_for, flash
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
load_dotenv()

def checkJWT():
    try:
        verify_jwt_in_request(locations=['cookies'])
    except NoAuthorizationError:
        resp = make_response(redirect('http://127.0.0.1:5000/login-user'))
        resp.set_cookie('ACCESS_TOKEN', '', expires=0)
        resp.set_cookie('csrf_access_token', '', expires=0)
        return resp, 400
    token = request.cookies.get('ACCESS_TOKEN', None)
    csrf_token = request.cookies.get('csrf_access_token')
    if not token or not csrf_token:
        return redirect('http://127.0.0.1:5000/login-user'), 400
    return get_jwt_identity(), 200


def getUserData(user_id):
    count = UserEducation.query.filter_by(user_id=user_id).count()
    if count > 0:
        return redirect('http://127.0.0.1:5000/dashboard'), 305
    return count, 200


def showError(msg):
    flash(msg, 'error')
    return redirect(url_for('form.home'))
def validate_input(data, field, expected_type, choices=None):
    value = data.get(field)
    if value is None:
        return False, f"{field} is required."

    if expected_type == 'number':
        try:
            value = float(value)
        except ValueError:
            return False, f"{field} must be a valid number."

    if expected_type == 'text':
        if choices and value not in choices:
            return False, f"{field} must be one of {choices}."

    if expected_type == 'year':
        if not re.match(r'^\d{4}$', value):
            return False, f"{field} must be a valid year."

    return True, value


def validate_request(request):
    fields = [
        ('tuition_fees', 'number', None),
        ('urban_flag', 'text', ['Yes', 'No']),
        ('highest_level', 'text', ["Master's", "Bachelor's"]),
        ('interested_field', 'text', None),
        ('english_certificate', 'text', ['IELTS', 'TOEFL']),
        ('english_score', 'number', None),
        ('year_highest_level', 'year', None),
        ('current_job', 'text', None),
        ('relevant_experience', 'number', None)
    ]

    errors = []
    validated_data = {}

    for field, expected_type, choices in fields:
        is_valid, result = validate_input(request.form, field, expected_type, choices)
        if not is_valid:
            errors.append(result)
        else:
            validated_data[field] = result

    if errors:
        return errors, 400

    return validated_data, 200
