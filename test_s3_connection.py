"""
Test script to verify AWS S3 connection and bucket access
"""
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()

def test_s3_connection():
    print("Testing AWS S3 Connection...")
    print("-" * 50)
    
    # Get credentials from .env
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_REGION')
    bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
    
    print(f"Access Key: {access_key[:10]}..." if access_key else "Access Key: NOT FOUND")
    print(f"Region: {region}")
    print(f"Bucket: {bucket_name}")
    print("-" * 50)
    
    try:
        # Create S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        
        # Test 1: Check if bucket exists
        print("\n1. Checking bucket access...")
        s3_client.head_bucket(Bucket=bucket_name)
        print("   SUCCESS: Bucket exists and is accessible!")
        
        # Test 2: List objects (first 5)
        print("\n2. Listing bucket contents...")
        response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
        if 'Contents' in response:
            print(f"   Found {len(response['Contents'])} objects:")
            for obj in response['Contents']:
                print(f"   - {obj['Key']}")
        else:
            print("   Bucket is empty (this is OK for new buckets)")
        
        # Test 3: Check bucket location
        print("\n3. Checking bucket location...")
        location = s3_client.get_bucket_location(Bucket=bucket_name)
        bucket_region = location['LocationConstraint'] or 'us-east-1'
        print(f"   Bucket region: {bucket_region}")
        if bucket_region != region:
            print(f"   WARNING: Bucket region ({bucket_region}) differs from configured region ({region})")
        
        # Test 4: Check bucket policy/permissions
        print("\n4. Checking bucket permissions...")
        try:
            s3_client.get_bucket_policy(Bucket=bucket_name)
            print("   Bucket has a policy configured")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                print("   WARNING: No bucket policy found - you may need to add public read policy")
            else:
                print(f"   Could not check policy: {e}")
        
        print("\n" + "=" * 50)
        print("SUCCESS: S3 connection is working!")
        print("=" * 50)
        print("\nYou can now:")
        print("1. Restart your FastAPI server")
        print("2. Upload files - they will go to S3")
        print("3. Check your S3 bucket in AWS Console")
        
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"\nERROR: {error_code}")
        print(f"Message: {e.response['Error']['Message']}")
        
        if error_code == '403' or error_code == 'AccessDenied':
            print("\nPossible issues:")
            print("- IAM user doesn't have S3 permissions")
            print("- Access keys are incorrect")
            print("- Bucket policy blocks access")
        elif error_code == '404' or error_code == 'NoSuchBucket':
            print("\nPossible issues:")
            print("- Bucket name is incorrect")
            print("- Bucket is in different region")
            print("- Bucket doesn't exist")
        
        return False
        
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_s3_connection()
