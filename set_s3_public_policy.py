import boto3
import json
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

# Bucket policy to allow public read access
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }
    ]
}

try:
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
    print(f"Successfully set public read policy for bucket: {bucket_name}")
except Exception as e:
    print(f"Error: {e}")
