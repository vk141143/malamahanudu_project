# Gallery API Documentation for UI Developer

## Upload Gallery Item

### Endpoint
```
POST /admin/gallery
```

### Authentication
Required: Bearer Token in Authorization header
```
Authorization: Bearer <access_token>
```

### Request Format
**Content-Type:** `multipart/form-data`

### Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Title of the gallery item |
| description | string | No | Description of the gallery item |
| file | file | Yes | Image or video file |

### Supported File Types

**Images:**
- .jpg, .jpeg, .png, .gif, .webp

**Videos:**
- .mp4, .avi, .mov, .wmv, .flv, .webm

**Max File Size:** 5MB

### Example Request (JavaScript/Fetch)

```javascript
const formData = new FormData();
formData.append('title', 'Event Photo');
formData.append('description', 'Annual meeting 2024');
formData.append('file', fileInput.files[0]);

const response = await fetch('https://api.malamahanadu.org/admin/gallery', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  },
  body: formData
});

const result = await response.json();
```

### Success Response (200)

```json
{
  "id": 123,
  "title": "Event Photo",
  "description": "Annual meeting 2024",
  "media_url": "https://malamahanadu.s3.amazonaws.com/gallery/images/abc123.jpg",
  "media_type": "image",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Error Responses

**400 Bad Request** - Invalid file type
```json
{
  "detail": "Unsupported file type: .txt"
}
```

**400 Bad Request** - File too large
```json
{
  "detail": "File size exceeds 5MB limit"
}
```

**401 Unauthorized** - Missing or invalid token
```json
{
  "detail": "Not authenticated"
}
```

**500 Internal Server Error** - Upload failed
```json
{
  "detail": "Failed to upload file to S3: <error message>"
}
```

## Get Gallery List

### Endpoint
```
GET /admin/gallery
```

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| media_type | string | No | null | Filter by "image" or "video" |
| page | integer | No | 1 | Page number (min: 1) |
| limit | integer | No | 10 | Items per page (min: 1, max: 100) |

### Example Request

```javascript
const response = await fetch(
  'https://api.malamahanadu.org/admin/gallery?media_type=image&page=1&limit=10',
  {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  }
);

const result = await response.json();
```

### Success Response (200)

```json
{
  "items": [
    {
      "id": 123,
      "title": "Event Photo",
      "description": "Annual meeting 2024",
      "media_url": "https://malamahanadu.s3.amazonaws.com/gallery/images/abc123.jpg",
      "media_type": "image",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 10,
  "total_pages": 5
}
```

## Update Gallery Item

### Endpoint
```
PUT /admin/gallery/{item_id}
```

### Request Format
**Content-Type:** `multipart/form-data`

### Form Fields (All Optional)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | No | New title |
| description | string | No | New description |
| file | file | No | New image/video file (replaces old one) |

### Example Request

```javascript
const formData = new FormData();
formData.append('title', 'Updated Title');
// Only include file if replacing the media
if (newFile) {
  formData.append('file', newFile);
}

const response = await fetch(`https://api.malamahanadu.org/admin/gallery/${itemId}`, {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  },
  body: formData
});
```

## Delete Gallery Item

### Endpoint
```
DELETE /admin/gallery/{item_id}
```

### Example Request

```javascript
const response = await fetch(`https://api.malamahanadu.org/admin/gallery/${itemId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### Success Response (200)

```json
{
  "message": "Gallery item deleted successfully"
}
```

## Important Notes

1. **File Upload Flow:**
   - File is uploaded to S3 bucket automatically
   - S3 URL is returned in `media_url` field
   - Use this URL to display images/videos in UI

2. **Media Type Detection:**
   - Automatically detected from file extension
   - No need to specify in request

3. **File Storage:**
   - Images: `gallery/images/` folder in S3
   - Videos: `gallery/videos/` folder in S3
   - Files are renamed with UUID for uniqueness

4. **CORS:**
   - API supports CORS for localhost and production domains
   - No additional configuration needed

5. **Image Display:**
   - Use `media_url` directly in `<img>` or `<video>` tags
   - S3 bucket is configured for public read access
