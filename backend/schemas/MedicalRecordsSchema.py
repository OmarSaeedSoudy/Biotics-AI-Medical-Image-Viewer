from marshmallow import Schema, fields

"""User Schema"""
class MedicalRecordSchema(Schema):
    # patient_id = fields.Int(required=True)
    patient_id = fields.Raw(type='int')
    description = fields.Raw(type='str')
    dicom_file = fields.Raw(type='file')
    