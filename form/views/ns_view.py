from flask import jsonify
from flask_restx import Namespace, Resource

from form.models.models import UserEducation, ApplicantDetails
from form.utils.utils import getUserData, checkJWT
from sqlalchemy.orm import joinedload

data_ns = Namespace('Data', description='Get Data')

@data_ns.route('/')
class Info(Resource):
    def get(self):
        checkJWT_ = checkJWT()
        if checkJWT_[1] == 400:
            return jsonify({'status': 'error', 'message': 'JWT Token is invalid.'})
        user_id = checkJWT_[0]['user_id']
        try:
            education_obj = UserEducation.query.filter_by(user_id=user_id).first()
            details_obj = ApplicantDetails.query.filter_by(user_id=user_id).first()
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'User does not exist.'})
        details = {
            'current_job': details_obj.current_job,
            'tuition_fees': details_obj.tuition_fees,
            'relevant_experience_years': details_obj.relevant_experience_years,
            'urban_flag': details_obj.urban_flag,
            'expected_move_date': details_obj.expected_move_date,
        }
        education = {
            'highest_level': education_obj.highest_level,
            'interested_field': education_obj.interested_field,
            'english_certificate': education_obj.english_certificate,
            'english_score': education_obj.english_score,
            'year_highest_level': education_obj.year_highest_level,
        }
        return jsonify(
            {
                'status': 'success',
                'education': education,
                'details': details
            }
        )