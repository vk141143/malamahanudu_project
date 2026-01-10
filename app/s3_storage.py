import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException, status
import os
from dotenv import load_dotenv
import uuid
from pathlib import Path

load_dotenv()

class S3Storage:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
    
    def upload_file(self, file: UploadFile, folder: str = "uploads") -> str:
        """Upload file to S3 and return the URL"""
        try:
            # Generate unique filename
            file_extension = Path(file.filename).suffix.lower()
            unique_filename = f"{folder}/{uuid.uuid4()}{file_extension}"
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                unique_filename,
                ExtraArgs={'ContentType': file.content_type}
            )
            
            # Return S3 URL
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{unique_filename}"
            return s3_url
            
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload file to S3: {str(e)}"
            )
    
    def delete_file(self, file_url: str) -> bool:
        """Delete file from S3"""
        try:
            # Extract key from URL
            key = file_url.split(f"{self.bucket_name}.s3.amazonaws.com/")[1]
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return True
            
        except Exception as e:
            print(f"Failed to delete file from S3: {str(e)}")
            return False

# Singleton instance
s3_storage = S3Storage()
