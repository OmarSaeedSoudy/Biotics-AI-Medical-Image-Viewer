from marshmallow import Schema, fields


"""User Schema"""
class PatientRegisterSchema(Schema):
    patient_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    doctor_id = fields.Int(dump_only=True)
    