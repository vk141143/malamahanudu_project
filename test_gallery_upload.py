import boto3
from dotenv import load_dotenv
import os

load_dotenv()

# Test S3 connection
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

print(f"Testing S3 bucket: {bucket_name}")

try:
    # Test bucket access
    response = s3_client.head_bucket(Bucket=bucket_name)
    print("[OK] Bucket exists and is accessible")
    
    # Test upload with public-read ACL
    test_content = b"test"
    s3_client.put_object(
        Bucket=bucket_name,
        Key='test/test.txt',
        Body=test_content,
        ACL='public-read'
    )
    print("[OK] Upload with public-read ACL successful")
    
    # Clean up
    s3_client.delete_object(Bucket=bucket_name, Key='test/test.txt')
    print("[OK] Test file deleted")
    
except Exception as e:
    print(f"[ERROR] {str(e)}")
    print("\nIf ACL error, the bucket may have 'Block Public Access' enabled.")
    print("Try uploading without ACL...")
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key='test/test.txt',
            Body=test_content
        )
        print("[OK] Upload without ACL successful")
        s3_client.delete_object(Bucket=bucket_name, Key='test/test.txt')
        print("\nSolution: Remove ACL='public-read' from uploads")
    except Exception as e2:
        print(f"[ERROR] Upload failed: {str(e2)}")
