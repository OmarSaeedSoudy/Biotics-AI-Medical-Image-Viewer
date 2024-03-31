import boto3

class AmazonWebServicesHandler:
    def __init__(self) -> None:
        self.s3_client = boto3.client("s3", aws_access_key_id="AKIAW3MEATE7UETOES5B", aws_secret_access_key="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")
        
    def upload_file(self, file_local_path, s3_bucket, s3_key):
        self.s3_client.upload_file(file_local_path, s3_bucket, s3_key)
    
    def download_file(self, file_local_path, s3_bucket, s3_key):
        pass
    
    def generate_presigned_url(self, s3_bucket, s3_key):
        presigned_url = self.s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': s3_bucket,
                'Key': s3_key
            }
        )
        return presigned_url