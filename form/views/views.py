from datetime import datetime

from flask import render_template, redirect, request, make_response, jsonify, session
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restx import Namespace

from form.models.models import UserEducation, ApplicantDetails
from form import form_bp, db
from form.utils.utils import validate_request, showError
data_ns = Namespace('Data', description='Get Data')

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



@form_bp.route('home', methods=['GET', 'POST'])
def home():
    checkJWT_ = checkJWT()
    if checkJWT_[1] == 400:
        return checkJWT_[0]
    user_id = checkJWT_[0]['user_id']
    getData = getUserData(user_id)
    if getData[1] == 305:
        return getData[0]
    if request.method == 'POST':
        session['form_data'] = request.form.to_dict()

        expected_move_date = request.form.get('expected_move_date')
        try:
            expected_move_date = datetime.strptime(expected_move_date, '%Y-%m-%d')
        except ValueError:
            return showError('Invalid expected move date format. Use YYYY/MM/DD')
        fields = validate_request(request)
        if fields[1] == 400:
            for error in fields[0]:
                return showError(error)
        data = fields[0]

        education_obj = UserEducation(
            highest_level=data['highest_level'],
            user_id=user_id,
            interested_field=data['interested_field'],
            english_certificate=data['english_certificate'],
            english_score=data['english_score'],
            year_highest_level=data['year_highest_level']
        )
        db.session.add(education_obj)

        applicant_obj = ApplicantDetails(
            current_job=data['current_job'],
            user_id=user_id,
            tuition_fees=data['tuition_fees'],
            relevant_experience_years=data['relevant_experience'],
            urban_flag=True if data['urban_flag'] == 'Yes' else False,
            expected_move_date=expected_move_date
        )
        db.session.add(applicant_obj)

        db.session.commit()
        return redirect('http://127.0.0.1:5000/dashboard')

    form_data = session.pop('form_data', {})
    csrf_token = request.cookies.get('csrf_access_token')
    context = {
        'form_data': form_data,
        'csrf_token': csrf_token,
    }
    return render_template('home.html', **context)

