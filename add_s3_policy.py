"""
Add public read policy to S3 bucket
This allows uploaded files to be publicly accessible
"""
import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

# Bucket policy for public read access
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
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    
    # Convert policy to JSON string
    policy_string = json.dumps(bucket_policy)
    
    # Apply policy
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy_string)
    
    print(f"SUCCESS: Public read policy added to bucket '{bucket_name}'")
    print("\nFiles uploaded to this bucket will now be publicly accessible!")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    print("\nYou can also add this policy manually in AWS Console:")
    print("1. Go to S3 → Your Bucket → Permissions → Bucket Policy")
    print("2. Paste this policy:")
    print(json.dumps(bucket_policy, indent=2))
