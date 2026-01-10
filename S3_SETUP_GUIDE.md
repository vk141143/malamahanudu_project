# AWS S3 Integration Setup Guide

## Overview
All uploaded files (membership photos, complaint documents, gallery images/videos) are now stored in AWS S3 instead of local storage.

## AWS S3 Setup Steps

### 1. Create AWS Account
- Go to https://aws.amazon.com/
- Sign up for an AWS account if you don't have one

### 2. Create S3 Bucket
1. Go to AWS Console → S3
2. Click "Create bucket"
3. Enter bucket name (e.g., `mala-project-uploads`)
4. Choose region (e.g., `us-east-1`)
5. **Uncheck "Block all public access"** (for public file access)
6. Click "Create bucket"

### 3. Configure Bucket Policy (for public read access)
1. Go to your bucket → Permissions → Bucket Policy
2. Add this policy (replace `YOUR-BUCKET-NAME`):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

### 4. Create IAM User with S3 Access
1. Go to AWS Console → IAM → Users
2. Click "Add users"
3. Enter username (e.g., `mala-project-s3-user`)
4. Select "Access key - Programmatic access"
5. Click "Next: Permissions"
6. Click "Attach existing policies directly"
7. Search and select `AmazonS3FullAccess`
8. Click through to create user
9. **IMPORTANT**: Save the Access Key ID and Secret Access Key

### 5. Update .env File
Add these values to your `.env` file:

```env
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-access-key-id-here
AWS_SECRET_ACCESS_KEY=your-secret-access-key-here
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-bucket-name-here
```

### 6. Install Dependencies
```bash
pip install boto3
```

Or use the updated requirements.txt:
```bash
pip install -r requirements.txt
```

## File Storage Structure in S3

Files are organized in folders:
- `membership/photos/` - Member application photos
- `complaints/documents/` - Complaint supporting documents
- `gallery/images/` - Gallery images
- `gallery/videos/` - Gallery videos

## Features

### Automatic Upload
- Files are automatically uploaded to S3 when submitted
- Unique filenames are generated using UUID
- File URLs are stored in the database

### Automatic Deletion
- When gallery items are deleted, files are removed from S3
- When gallery items are updated with new files, old files are deleted from S3

### Public Access
- All uploaded files are publicly accessible via S3 URLs
- URLs format: `https://your-bucket-name.s3.amazonaws.com/folder/filename.ext`

## Security Best Practices

1. **Never commit AWS credentials to Git**
   - Keep `.env` file in `.gitignore`
   - Use environment variables in production

2. **Use IAM User with Limited Permissions**
   - Create separate IAM user for this application
   - Only grant S3 access, not full AWS access

3. **Enable Bucket Versioning** (optional)
   - Helps recover accidentally deleted files
   - Go to bucket → Properties → Bucket Versioning

4. **Set up CORS** (if accessing from browser)
   - Go to bucket → Permissions → CORS
   - Add CORS configuration if needed

## Cost Considerations

- S3 pricing: https://aws.amazon.com/s3/pricing/
- Free tier: 5GB storage, 20,000 GET requests, 2,000 PUT requests per month
- Monitor usage in AWS Cost Explorer

## Testing

1. Update `.env` with your AWS credentials
2. Restart the server
3. Test file uploads:
   - Submit membership application with photo
   - Submit complaint with document
   - Upload gallery image/video
4. Verify files appear in S3 bucket
5. Verify URLs are accessible

## Troubleshooting

### Error: "Failed to upload file to S3"
- Check AWS credentials in `.env`
- Verify IAM user has S3 permissions
- Check bucket name is correct

### Error: "Access Denied"
- Verify bucket policy allows public read
- Check IAM user permissions
- Ensure bucket and region are correct

### Files not accessible
- Check bucket policy for public read access
- Verify CORS configuration if accessing from browser
- Check file URLs in database

## Migration from Local Storage

If you have existing files in local storage:
1. Use AWS CLI to sync local files to S3:
   ```bash
   aws s3 sync uploads/ s3://your-bucket-name/
   ```
2. Update database URLs to point to S3 URLs
3. Run a migration script to update all file paths

## Rollback to Local Storage

If you need to revert to local storage:
1. Restore original `app/public/routes.py` and `app/gallery.py`
2. Remove S3 imports
3. Files will be saved locally again
