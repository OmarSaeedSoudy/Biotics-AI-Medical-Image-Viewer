from db import db
import json

class MedicalRecordModel(db.Model):
    __tablename__ = "medical_records"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text, nullable=True)
    dicom_bucket = db.Column(db.String(80), unique=False, nullable=True)
    dicom_key = db.Column(db.String(80), unique=False, nullable=True)
    _dicom_details = db.Column(db.Text, nullable=True)  # Store as JSON string

    patient = db.relationship('PatientModel', foreign_keys=[patient_id])
    doctor = db.relationship('UserModel', foreign_keys=[doctor_id])

    # @property
    # def dicom_details(self):
    #     """Property to get dicom_details as dictionary."""
    #     return json.loads(self._dicom_details) if self._dicom_details else {}

    # @dicom_details.setter
    # def dicom_details(self, value):
    #     """Property setter to set dicom_details as dictionary."""
    #     self._dicom_details = json.dumps(value) if value else None
