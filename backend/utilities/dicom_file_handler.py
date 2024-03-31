import pydicom
from .aws_handler import AmazonWebServicesHandler
from models import MedicalRecordModel
import json
from db import db
import os

class DicomFileHandler:
    def __init__(self):
        self.aws_class = AmazonWebServicesHandler()
        self.s3_bucket = "biotics-ai.com"
        self.s3_prefix = "dicom"
    
    def read_dicom_file(self, dicom_file_path):
        try:
            dicom_data = pydicom.dcmread(dicom_file_path)
            
            meta_data = {}
            for element in dicom_data:
                if element.name != "Pixel Data":  # Skip Image Pixel Data
                    if isinstance(element.value, pydicom.multival.MultiValue):
                        meta_data[element.name] = [str(value) for value in element.value]
                    else:
                        meta_data[element.name] = str(element.value)

            return meta_data
        
        except Exception as e:
            print(f"Error reading DICOM file: {e}")
    
    def handle_dicom_file(self, dicom_file_path):
        data = self.read_dicom_file(dicom_file_path)
        file_name = os.path.basename(dicom_file_path)
        s3_key = f"{self.s3_prefix}/{file_name}"
        print(s3_key)
        self.aws_class.upload_file(dicom_file_path, self.s3_bucket, s3_key)
        
        if os.path.exists(dicom_file_path):
            os.remove(dicom_file_path)
            
        return data, self.s3_bucket, s3_key
            