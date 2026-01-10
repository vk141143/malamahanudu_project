# S3 Integration - Quick Reference

## ✅ COMPLETE - All Files Use S3 Storage

### What Changed:
- ❌ Local file storage removed
- ✅ All uploads go to AWS S3
- ✅ Database stores S3 URLs (not local paths)
- ✅ Gallery displays images from S3 URLs

### Files That Upload to S3:
1. **Membership Photos** → `membership/photos/` folder in S3
2. **Complaint Documents** → `complaints/documents/` folder in S3  
3. **Gallery Images** → `gallery/images/` folder in S3
4. **Gallery Videos** → `gallery/videos/` folder in S3

### How Gallery Works Now:

#### Upload Flow:
```
Admin uploads image/video
    ↓
app/gallery.py → save_uploaded_file()
    ↓
app/s3_storage.py → upload_file()
    ↓
File uploaded to S3
    ↓
S3 URL returned (e.g., https://bucket.s3.amazonaws.com/gallery/images/uuid.jpg)
    ↓
URL saved to gallery.media_url in database
    ↓
Database commit
```

#### Display Flow:
```
GET /public/gallery
    ↓
Query gallery table
    ↓
Return items with media_url (S3 URLs)
    ↓
Frontend displays images using S3 URLs
    ↓
Images load directly from S3
```

### Database Fields with S3 URLs:
- `member_applications.photo_path` → S3 URL
- `complaints.supporting_document_path` → S3 URL
- `gallery.media_url` → S3 URL

### Example S3 URLs:
```
https://your-bucket.s3.amazonaws.com/membership/photos/abc-123-def.jpg
https://your-bucket.s3.amazonaws.com/complaints/documents/xyz-789-ghi.pdf
https://your-bucket.s3.amazonaws.com/gallery/images/mno-456-pqr.jpg
https://your-bucket.s3.amazonaws.com/gallery/videos/stu-012-vwx.mp4
```

### API Endpoints:

#### Public Gallery (GET):
```
GET /public/gallery
GET /public/gallery?media_type=image
GET /public/gallery?media_type=video

Response:
{
  "items": [
    {
      "id": 1,
      "title": "Event Photo",
      "description": "Description",
      "media_url": "https://bucket.s3.amazonaws.com/gallery/images/uuid.jpg",
      "media_type": "image",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1
}
```

#### Admin Gallery (POST):
```
POST /admin/gallery
Content-Type: multipart/form-data

Fields:
- title: string
- description: string (optional)
- file: image/video file

Response:
{
  "id": 1,
  "title": "Event Photo",
  "media_url": "https://bucket.s3.amazonaws.com/gallery/images/uuid.jpg",
  "media_type": "image"
}
```

### Setup Steps:

1. **Install boto3**:
   ```bash
   pip install boto3
   ```

2. **Update .env** with your AWS credentials:
   ```env
   AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
   AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   AWS_REGION=us-east-1
   AWS_S3_BUCKET_NAME=mala-project-uploads
   ```

3. **Restart server**:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

### Testing:

1. **Upload gallery image**:
   ```bash
   curl -X POST "http://localhost:8000/admin/gallery" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "title=Test Image" \
     -F "file=@image.jpg"
   ```

2. **View gallery**:
   ```bash
   curl "http://localhost:8000/public/gallery"
   ```

3. **Verify in S3**:
   - Go to AWS Console → S3
   - Open your bucket
   - Check `gallery/images/` folder
   - File should be there with UUID name

### Troubleshooting:

**Error: "Failed to upload file to S3"**
- Check AWS credentials in .env
- Verify IAM user has S3 permissions
- Confirm bucket name is correct

**Images not displaying**
- Check S3 bucket policy allows public read
- Verify URLs in database are complete S3 URLs
- Test URL directly in browser

**Error: "Access Denied"**
- Check IAM user permissions
- Verify bucket policy
- Ensure region matches

### Important Notes:

✅ All file operations now use S3
✅ No local file storage needed
✅ Gallery images load from S3 URLs
✅ Old files deleted from S3 when updated
✅ Files removed from S3 when deleted
✅ Unique UUID filenames prevent conflicts
✅ Public read access for viewing
✅ Private write access via API only

### File Structure in S3:
```
your-bucket-name/
├── membership/
│   └── photos/
│       ├── 123e4567-e89b-12d3-a456-426614174000.jpg
│       └── 234e5678-e89b-12d3-a456-426614174001.jpg
├── complaints/
│   └── documents/
│       ├── 345e6789-e89b-12d3-a456-426614174002.pdf
│       └── 456e7890-e89b-12d3-a456-426614174003.pdf
└── gallery/
    ├── images/
    │   ├── 567e8901-e89b-12d3-a456-426614174004.jpg
    │   └── 678e9012-e89b-12d3-a456-426614174005.png
    └── videos/
        ├── 789e0123-e89b-12d3-a456-426614174006.mp4
        └── 890e1234-e89b-12d3-a456-426614174007.mp4
```

## 🎉 Ready to Use!

Once you configure AWS credentials in .env, all file uploads will automatically go to S3 and gallery will display images from S3 URLs.
