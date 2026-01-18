import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.resource(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
bucket = s3.Bucket(bucket_name)

count = 0
for obj in bucket.objects.all():
    copy_source = {'Bucket': bucket_name, 'Key': obj.key}
    bucket.copy(copy_source, obj.key, ExtraArgs={
        'MetadataDirective': 'REPLACE',
        'ContentType': 'image/jpeg' if obj.key.endswith('.jpg') else 'image/png',
        'CacheControl': 'no-cache'
    })
    count += 1
    print(f"Updated: {obj.key}")

print(f"\nTotal files updated: {count}")
print("Wait 5 minutes and try again")
