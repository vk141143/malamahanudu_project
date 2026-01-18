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

# List all objects
paginator = s3_client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket_name)

count = 0
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            key = obj['Key']
            s3_client.put_object_acl(Bucket=bucket_name, Key=key, ACL='public-read')
            count += 1
            print(f"Updated ACL for: {key}")

print(f"\nTotal files updated: {count}")
