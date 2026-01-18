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

print("=== Checking CORS Configuration ===")
try:
    cors = s3_client.get_bucket_cors(Bucket=bucket_name)
    print(json.dumps(cors['CORSRules'], indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n=== Checking Bucket Policy ===")
try:
    policy = s3_client.get_bucket_policy(Bucket=bucket_name)
    print(json.dumps(json.loads(policy['Policy']), indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n=== Checking Public Access Block ===")
try:
    block = s3_client.get_public_access_block(Bucket=bucket_name)
    print(json.dumps(block['PublicAccessBlockConfiguration'], indent=2))
except Exception as e:
    print(f"No public access block configured")
