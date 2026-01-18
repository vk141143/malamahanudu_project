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

cors_configuration = {
    'CORSRules': [{
        'AllowedHeaders': ['*'],
        'AllowedMethods': ['GET', 'HEAD', 'PUT', 'POST'],
        'AllowedOrigins': ['*'],
        'ExposeHeaders': ['ETag', 'x-amz-server-side-encryption', 'x-amz-request-id', 'x-amz-id-2'],
        'MaxAgeSeconds': 3600
    }]
}

s3_client.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)
print(f"CORS updated with wildcard origin for bucket: {bucket_name}")
