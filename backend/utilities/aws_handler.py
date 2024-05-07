import boto3

class AmazonWebServicesHandler:
    def __init__(self) -> None:
        """
        Initializes the Amazon Web Services Handler with S3 client.
        
        Note:
            It's not recommended to hard-code AWS credentials in the code.
            Consider using environment variables or AWS credentials file for security.
        """
        self.s3_client = boto3.client(
            "s3"
        )
        
    def upload_file(self, file_local_path, s3_bucket, s3_key):
        """
        Uploads a file to S3 bucket.
        
        Args:
            file_local_path (str): Local path of the file to upload.
            s3_bucket (str): Name of the S3 bucket.
            s3_key (str): Key under which to store the file in the S3 bucket.
        """
        self.s3_client.upload_file(file_local_path, s3_bucket, s3_key)
    
    def download_file(self, file_local_path, s3_bucket, s3_key):
        """
        Downloads a file from S3 bucket (Currently not implemented).
        
        Args:
            file_local_path (str): Local path to save the downloaded file.
            s3_bucket (str): Name of the S3 bucket.
            s3_key (str): Key of the file in the S3 bucket.
        """
        pass
    
    def generate_presigned_url(self, s3_bucket, s3_key):
        """
        Generates a presigned URL for accessing a file from S3 bucket.
        
        Args:
            s3_bucket (str): Name of the S3 bucket.
            s3_key (str): Key of the file in the S3 bucket.
            
        Returns:
            str: Presigned URL for accessing the file.
        """
        presigned_url = self.s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': s3_bucket,
                'Key': s3_key
            }
        )
        return presigned_url
