from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import PatientModel, UserModel
from schemas import PatientRegisterSchema

# Initialize Blueprint for Patients API Endpoints
blp = Blueprint("Patients", "patients", description="Patients API Endpoints")

# Patient Registration Endpoint
@blp.route("/patient/register")
class PatientRegister(MethodView):
    @blp.arguments(PatientRegisterSchema)
    @jwt_required()
    def post(self, patient_data):
        """
        Endpoint to register/update a patient.
        
        Parameters:
            patient_data (dict): Patient data including name and email
        
        Returns:
            dict: Success message
        """
        # Get doctor's identity from JWT token
        doctor_identity = get_jwt_identity()
        
        # Check if patient already exists
        patient = PatientModel.query.filter(PatientModel.name == patient_data["name"]).first()
        
        if patient:
            # Update patient's doctor ID and commit
            patient.doctor_id = doctor_identity 
            db.session.commit()
            return {
                "message": "Patient Updated Successfully."
            },  200
        else:
            # Create new patient and commit
            patient = PatientModel(
                doctor_id = doctor_identity,
                name = patient_data["name"],
                email = patient_data["email"]
            )
            db.session.add(patient)
            db.session.commit()
            
            return {
                "message": "Patient Created Successfully."
            },  201


# Get All Patients Endpoint
@blp.route("/patients/get_all")
class PatientsGetAll(MethodView):
    @jwt_required()
    def get(self):
        """
        Endpoint to get all patients associated with the current doctor.
        
        Returns:
            dict: Success message and list of patients
        """
        # Get doctor's identity from JWT token
        doctor_identity = get_jwt_identity()
        
        # Query patients and corresponding users
        results = db.session.query(PatientModel, UserModel).filter(
            PatientModel.doctor_id == UserModel.id,
            PatientModel.doctor_id == doctor_identity
        ).all()
        
        # Initialize response dictionary
        response = {
            "message": "Successfully fetched patients"
        }
        
        if results:
            # Convert results to a list of dictionaries
            formatted_results = [
                {
                    "patient_id": patient.id,
                    "patient_name": patient.name,
                    "patient_email": patient.email
                }
                for patient, user in results
            ]
            
            # Add formatted results to response
            response["patients"] = formatted_results
        else:
            # Add results to response
            response["patients"] = results
            
        return response
