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

# Initialize Blueprint for MedicalRecords API Endpoints
blp = Blueprint("MedicalRecords", "medical_records", description="MedicalRecords API Endpoints")

# Medical Record Registration Endpoint
@blp.route("/medical_records/register")
class MedicalRecordRegister(MethodView):
    @jwt_required()
    @blp.arguments(MedicalRecordSchema)
    def post(self, medical_record_data):
        """
        Endpoint to register a medical record.
        
        Parameters:
            medical_record_data (dict): Medical record data including patient_id, description, and dicom_file
        
        Returns:
            dict: Success message or errors
        """
        # Get doctor's identity from JWT token
        doctor_identity = get_jwt_identity()
        errors = []
        
        # Extract data from request
        patient_id = request.form.get('patient_id')
        description = request.form.get('description')
        dicom_file = request.files.get('dicom_file')

        # Validate required fields
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
        
        # Save DICOM file temporarily
        dicom_file_path = f"temp/{dicom_file.filename}"
        with open(dicom_file_path, 'wb') as f:
            f.write(dicom_file.read())
        
        # Handle DICOM file and get data, bucket, and key
        dcm_class = DicomFileHandler()
        data, bucket, key = dcm_class.handle_dicom_file(dicom_file_path=dicom_file_path)
        
        # Create MedicalRecordModel instance
        medical_record = MedicalRecordModel(
            doctor_id = doctor_identity,
            patient_id = patient_id,
            description = description,
            dicom_bucket = bucket,
            dicom_key = key,
            _dicom_details = json.dumps(data)
        )        
        
        # Add and commit medical_record to database
        db.session.add(medical_record)
        db.session.commit()
        
        return {
            "message": "Medical Record Created Successfully."
        }, 201
        

# Get All Medical Records for a Patient Endpoint
@blp.route("/medical_records/get/<int:patient_id>")
class MedicalRecordsGetAll(MethodView):
    @jwt_required()
    def get(self, patient_id):
        """
        Endpoint to get all medical records associated with a patient.
        
        Parameters:
            patient_id (int): ID of the patient
        
        Returns:
            dict: Success message and list of medical records
        """
        # Initialize AWS handler
        aws_class = AmazonWebServicesHandler()
        
        # Get doctor's identity from JWT token
        doctor_identity = get_jwt_identity()
        
        # Query medical records and corresponding patient names
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
        
        # Initialize response dictionary
        response = {
            "patient_medical_records": []
        }
        
        if results:
            for res in results:
                # Generate presigned URL for DICOM file
                presigned_url = aws_class.generate_presigned_url(res[0].dicom_bucket, res[0].dicom_key)
                
                # Create medical record dictionary
                medical_record = {
                    "patient_name": res[1],
                    "description": res[0].description,
                    "dicom_url": presigned_url,
                    "dicom_details": json.loads(res[0]._dicom_details)
                }
                
                # Add medical record to response
                response["patient_medical_records"].append(medical_record)
        
        return response, 200
