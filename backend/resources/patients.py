from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import PatientModel, UserModel
from schemas import PatientRegisterSchema

blp = Blueprint("Patients", "patients", description="Patients API Endpoints")

@blp.route("/patient/register")
class PatientRegister(MethodView):
    @blp.arguments(PatientRegisterSchema)
    @jwt_required()
    def post(self, patient_data):
        doctor_identity = get_jwt_identity()
        patient = PatientModel.query.filter(PatientModel.name == patient_data["name"]).first()
        if patient:
            patient.doctor_id = doctor_identity 
            db.session.commit()
            return {
                "message": "Patient Updated Successfully."
            },  200
        else:
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


@blp.route("/patients/get_all")
class PatientsGetAll(MethodView):
    @jwt_required()
    def get(self):
        doctor_identity = get_jwt_identity()
        results = db.session.query(PatientModel, UserModel).filter(
            PatientModel.doctor_id == UserModel.id,
            PatientModel.doctor_id == doctor_identity
        ).all()
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

        if results:
            response["patients"] = formatted_results
        else:
            response["patients"] = results
            
        return response


