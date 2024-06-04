import os
import re
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import request, redirect, jsonify, url_for, flash

load_dotenv()

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         print(request.headers)
#         # if 'Authorization' in request.headers:
#         #     token = request.headers['Authorization'].split()[1]
#
#         if not token:
#             return redirect('http://127.0.0.1:5000/login')
#
#         try:
#             data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
#             current_user = data['user_id']
#         except:
#             return redirect('http://127.0.0.1:5000/login')
#
#         return f(current_user, *args, **kwargs)
#
#     return decorated


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
