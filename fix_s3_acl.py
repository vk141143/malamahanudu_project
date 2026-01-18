import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)
bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

# Update ACL for all files in membership/photos folder
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='membership/photos/')
    
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            s3_client.put_object_acl(Bucket=bucket_name, Key=key, ACL='public-read')
            print(f"Updated ACL for: {key}")
    
    # Update ACL for QR codes
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='members/qrcodes/')
    
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            s3_client.put_object_acl(Bucket=bucket_name, Key=key, ACL='public-read')
            print(f"Updated ACL for: {key}")
    
    print("Successfully updated ACL for all files")
except Exception as e:
    print(f"Error: {e}")
