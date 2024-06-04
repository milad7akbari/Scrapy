from datetime import datetime

from form import db


class UserEducation(db.Model):
    __tablename__ = 'user_education'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    highest_level = db.Column(db.String(128), nullable=False)
    interested_field = db.Column(db.String(255), nullable=False)
    english_certificate = db.Column(db.String(128), nullable=True)
    english_score = db.Column(db.SmallInteger, nullable=True)
    year_highest_level = db.Column(db.SmallInteger, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserEducation {self.user_id}>'


class ApplicantDetails(db.Model):
    __tablename__ = 'applicant_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), db.ForeignKey('user_education.user_id'), nullable=True)
    current_job = db.Column(db.String(255), unique=True, nullable=False)
    tuition_fees = db.Column(db.Integer, nullable=True)
    relevant_experience_years = db.Column(db.Integer, nullable=True)
    urban_flag = db.Column(db.Boolean, default=False)
    expected_move_date = db.Column(db.Date, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    user = db.relationship('UserEducation', backref=db.backref('applicant_details', lazy=True))

    def __repr__(self):
        return f'<ApplicantDetails {self.user_id}>'
