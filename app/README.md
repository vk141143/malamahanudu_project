# FastAPI Admin Dashboard API

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create sample data:
```bash
python app/create_public_test_data.py
python app/create_gallery_data.py
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Database

**Default:** SQLite (admin_dashboard.db)
**Switch to PostgreSQL:** Set `DATABASE_URL` environment variable

## Admin Management

**Sample Admin:** admin@example.com / admin123

## Public APIs (No Authentication Required)

### Public Donations API
- `POST /public/donations` - Submit donation with payment details

**Fields:**
- full_name (required)
- email_address (optional)
- phone_number (10 digits, required)
- payment_method (bank_transfer/upi/cash/cheque/online_payment)
- preset_amount OR custom_amount (required)
- transaction_id (required)
- notes (optional)

### Public Membership Application API
- `POST /public/membership/apply` - Apply for membership with photo upload

**Fields:**
- Personal: full_name, father_husband_name, gender, date_of_birth (dd-mm-yyyy), caste, aadhaar_number (12 digits)
- Contact: phone_number (10 digits), email_address (optional)
- Address: state, district, mandal, village, full_address
- Photo: multipart file upload (max 5MB, JPG/PNG)

### Public Complaints API
- `POST /public/complaints` - Submit complaint with optional document

**Fields:**
- full_name, email_address (optional), phone_number (10 digits), address
- complaint_type, subject, detailed_description
- supporting_document (optional, max 5MB, JPG/PNG/GIF/PDF/TXT)
- Auto-generates reference_id (MMN-CMP-YYYYMMDD-XXXX)

### Public Gallery API (Read-Only)
- `GET /public/gallery` - View gallery items
- `GET /public/gallery?media_type=image` - Filter by media type

## Gallery Module APIs

### Gallery Overview
- `GET /admin/gallery/summary` - Total items, images, videos count

### Gallery Management
- `GET /admin/gallery` - Paginated gallery list with media type filter
- `POST /admin/gallery` - Upload new gallery item (multipart/form-data)
- `GET /admin/gallery/{id}` - Gallery item details
- `PUT /admin/gallery/{id}` - Update gallery item (multipart/form-data)
- `DELETE /admin/gallery/{id}` - Delete gallery item and file

## Complaints Module APIs

### Dashboard Summary Cards
- `GET /admin/complaints/summary` - Total, pending, in_progress, resolved, closed complaints

### Complaints Management
- `GET /admin/complaints` - Paginated complaints list with search & filters
- `GET /admin/complaints/{id}` - Complaint details
- `PATCH /admin/complaints/{id}/status` - Update complaint status and admin notes
- `GET /admin/complaints/export` - Export filtered complaints as CSV

## Donations Module APIs

### Dashboard Summary Cards
- `GET /admin/donations/summary` - Total, pending, verified, acknowledged donations + total raised amount

### Donations Management
- `GET /admin/donations` - Paginated donations list with search & filters
- `GET /admin/donations/{id}` - Donation details
- `POST /admin/donations/{id}/verify` - Verify donation
- `POST /admin/donations/{id}/acknowledge` - Acknowledge donation
- `GET /admin/donations/export` - Export filtered donations as CSV

## Members Module APIs

### Dashboard Cards
- `GET /admin/members/summary` - Total, approved, pending members count

### Members Management
- `GET /admin/members` - Paginated members list with search & filters
- `GET /admin/members/{id}` - Member details
- `POST /admin/members/{id}/approve` - Approve member
- `POST /admin/members/{id}/reject` - Reject member
- `GET /admin/members/export` - Export filtered members as CSV
- `GET /admin/members/filter-options` - Get dropdown filter options

## API Examples

### Public Donation Submission
```bash
curl -X POST "http://localhost:8000/public/donations" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email_address": "john@example.com",
    "phone_number": "9876543210",
    "payment_method": "upi",
    "preset_amount": 1000,
    "transaction_id": "TXN123456789",
    "notes": "Donation for community development"
  }'
```

### Public Membership Application
```bash
curl -X POST "http://localhost:8000/public/membership/apply" \
  -F "full_name=John Doe" \
  -F "father_husband_name=Robert Doe" \
  -F "gender=male" \
  -F "date_of_birth=15-01-1990" \
  -F "caste=General" \
  -F "aadhaar_number=123456789012" \
  -F "phone_number=9876543210" \
  -F "email_address=john@example.com" \
  -F "state=Telangana" \
  -F "district=Hyderabad" \
  -F "mandal=Secunderabad" \
  -F "village=Jubilee Hills" \
  -F "full_address=123 Main Street, Jubilee Hills" \
  -F "photo=@photo.jpg"
```

### Public Complaint Submission
```bash
curl -X POST "http://localhost:8000/public/complaints" \
  -F "full_name=John Doe" \
  -F "phone_number=9876543210" \
  -F "address=123 Main Street" \
  -F "complaint_type=Healthcare" \
  -F "subject=Hospital facility issues" \
  -F "detailed_description=Detailed complaint description" \
  -F "supporting_document=@document.pdf"
```

## File Storage

- **Public Uploads:** Files stored in `uploads/public/` directory
- **Photos:** `uploads/public/photos/` (membership applications)
- **Documents:** `uploads/public/documents/` (complaint supporting docs)
- **Static Serving:** Files accessible via `/uploads/public/`
- **File Limits:** 5MB max size, validated extensions

## Data Integration

**Public APIs store data in the same database tables as admin modules:**
- Public donations → `donations` table (visible in admin donations module)
- Public membership applications → `member_applications` table
- Public complaints → `complaints` table (visible in admin complaints module)
- Public gallery access → `gallery` table (managed by admin gallery module)

## Authentication

**Admin APIs:**
1. Login: `POST /admin/login` with email/password
2. Use returned JWT token in Authorization header: `Bearer <token>`

**Public APIs:**
- No authentication required
- Direct access to all public endpoints

## Features Implemented

✅ **Public Donations** - Full donation form with validation
✅ **Public Membership** - Complete application with photo upload
✅ **Public Complaints** - Complaint submission with document upload
✅ **Public Gallery** - Read-only gallery access with filtering
✅ **File Upload** - Photo and document handling with validation
✅ **Data Validation** - Phone, email, Aadhaar, date format validation
✅ **Reference IDs** - Auto-generated complaint tracking
✅ **File Management** - Secure file storage and serving
✅ **Database Integration** - Shared data with admin modules
✅ **Clean APIs** - Proper schemas and error handling