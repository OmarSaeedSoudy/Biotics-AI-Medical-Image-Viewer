from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
import os
import marshmallow
import json
from db import db
from models import PatientModel, UserModel, MedicalRecordModel
from schemas import MedicalRecordSchema 
from utilities import DicomFileHandler, AmazonWebServicesHandler

blp = Blueprint("MedicalRecords", "medical_records", description="MedicalRecords API Endpoints")

@blp.route("/medical_records/register")
class PatientRegister(MethodView):
    @jwt_required()
    @blp.arguments(MedicalRecordSchema)
    def post(self, medical_record_data):
        doctor_identity = get_jwt_identity()
        errors = []
        
        patient_id = request.form.get('patient_id')
        description = request.form.get('description')
        dicom_file = request.files.get('dicom_file')

        # Validate required fields (using schema validation is recommended)
        if not patient_id:
            errors.append("patient_id is required")
        if not description:
            errors.append("description is required")
        if not dicom_file:
            errors.append("dicom_file is required")
        if errors:
            return {
                "errors": errors
            }, 400
        
        dicom_file_path = f"temp/{dicom_file.filename}"
        with open(dicom_file_path, 'wb') as f:
            f.write(dicom_file.read())
        
        dcm_class = DicomFileHandler()
        data, bucket, key = dcm_class.handle_dicom_file(dicom_file_path=dicom_file_path)
        
        medical_record = MedicalRecordModel(
            doctor_id = doctor_identity,
            patient_id = patient_id,
            description = description,
            dicom_bucket = bucket,
            dicom_key = key,
            _dicom_details = json.dumps(data)
        )        
        
        db.session.add(medical_record)
        db.session.commit()
        
        return {
                "message": "Medical Record Created Successfully."
            },  201
        

@blp.route("/medical_records/get/<int:patient_id>")
class PatientsGetAll(MethodView):
    @jwt_required()
    def get(self, patient_id):
        aws_class = AmazonWebServicesHandler()
        doctor_identity = get_jwt_identity()
        results = db.session.query(
            MedicalRecordModel,
            PatientModel.name  # Add patient name to the query
        ).join(
            PatientModel,  # Join PatientModel
            MedicalRecordModel.patient_id == PatientModel.id  # Join condition
        ).filter(
            MedicalRecordModel.doctor_id == doctor_identity,
            MedicalRecordModel.patient_id == patient_id
        ).all()
        
        response = {
                "patient_medical_records": []
            }
        if results:
            for res in results:
                presigned_url = aws_class.generate_presigned_url(res[0].dicom_bucket, res[0].dicom_key)
                medical_record = {
                    "patient_name": res[1],
                    "description": res[0].description,
                    "dicom_url": presigned_url,
                    "dicom_details": json.loads(res[0]._dicom_details)
                }
                response["patient_medical_records"].append(medical_record)
        return response, 200


