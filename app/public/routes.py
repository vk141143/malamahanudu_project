from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Donation, MemberApplication, Complaint, Gallery, PaymentMethod, Gender, ComplaintType, MediaType
from app.s3_storage import s3_storage
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime, date
import uuid
import re

router = APIRouter(prefix="/public", tags=["Public APIs"])

# File validation
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Schemas
class PublicDonationCreate(BaseModel):
    full_name: Optional[str] = None
    email_address: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    preset_amount: Optional[float] = None
    custom_amount: Optional[float] = None
    transaction_id: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if v and not re.match(r'^\d{10}$', v):
            raise ValueError('Phone number must be exactly 10 digits')
        return v

class PublicMembershipCreate(BaseModel):
    full_name: Optional[str] = None
    father_husband_name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    caste: Optional[str] = None
    aadhaar_number: Optional[str] = None
    phone_number: Optional[str] = None
    email_address: Optional[str] = None
    blood_group: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    mandal: Optional[str] = None
    village: Optional[str] = None
    full_address: Optional[str] = None

class PublicComplaintCreate(BaseModel):
    full_name: str
    email_address: Optional[EmailStr] = None
    phone_number: str
    address: str
    complaint_type: ComplaintType
    subject: Optional[str] = None
    detailed_description: Optional[str] = None
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if not re.match(r'^\d{10}$', v):
            raise ValueError('Phone number must be exactly 10 digits')
        return v

class PublicGalleryResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    media_url: str
    media_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PublicGalleryList(BaseModel):
    items: List[PublicGalleryResponse]
    total: int

# Helper functions
def save_uploaded_file_to_s3(file: UploadFile, folder: str) -> str:
    """Upload file to S3 and return URL"""
    # Validate file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 5MB limit"
        )
    
    # Upload to S3
    return s3_storage.upload_file(file, folder)

def generate_reference_id() -> str:
    today = datetime.now().strftime('%Y%m%d')
    random_part = str(uuid.uuid4())[:4].upper()
    return f"MMN-CMP-{today}-{random_part}"

# API Endpoints
@router.post("/donations")
async def create_donation(donation: PublicDonationCreate, db: Session = Depends(get_db)):
    # Determine final amount
    final_amount = donation.preset_amount if donation.preset_amount else donation.custom_amount
    
    if not final_amount or final_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0"
        )
    
    # Create donation record
    db_donation = Donation(
        donor_name=donation.full_name or "",
        donor_email=donation.email_address or "",
        phone_number=donation.phone_number or "",
        amount=final_amount,
        payment_method=donation.payment_method.value if donation.payment_method else "",
        transaction_id=donation.transaction_id or "",
        notes=donation.notes,
        status="pending"
    )
    
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    
    return {
        "message": "Donation submitted successfully",
        "donation_id": db_donation.id,
        "status": "pending"
    }

@router.post("/membership/apply")
async def apply_membership(
    full_name: Optional[str] = Form(None),
    father_husband_name: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    date_of_birth: Optional[str] = Form(None),
    caste: Optional[str] = Form(None),
    aadhaar_number: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    email_address: Optional[str] = Form(None),
    blood_group: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    district: Optional[str] = Form(None),
    mandal: Optional[str] = Form(None),
    village: Optional[str] = Form(None),
    full_address: Optional[str] = Form(None),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Save photo to S3
        if not photo or not photo.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Photo is required"
            )
        
        photo_path = save_uploaded_file_to_s3(photo, "membership/photos")
        
        # Convert date format
        dob = None
        if date_of_birth:
            try:
                dob = datetime.strptime(date_of_birth, '%d-%m-%Y').date()
            except ValueError:
                dob = None
        
        # Create membership application
        db_application = MemberApplication(
            full_name=full_name or "",
            father_husband_name=father_husband_name or "",
            gender=gender,
            date_of_birth=dob,
            caste=caste or "",
            aadhaar_number=aadhaar_number or "",
            phone_number=phone_number or "",
            email_address=email_address or "",
            blood_group=blood_group or "",
            state=state or "",
            district=district or "",
            mandal=mandal or "",
            village=village,
            full_address=full_address,
            photo_path=photo_path,
            status="pending"
        )
        
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        
        return {
            "message": "Membership application submitted successfully",
            "application_id": db_application.id,
            "status": "pending"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error in apply_membership: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit application: {str(e)}"
        )

@router.post("/complaints")
async def create_complaint(
    full_name: str = Form(...),
    phone_number: str = Form(...),
    address: str = Form(...),
    complaint_type: ComplaintType = Form(...),
    subject: Optional[str] = Form(None),
    detailed_description: Optional[str] = Form(None),
    email_address: Optional[str] = Form(None),
    supporting_document: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Validate form data
    try:
        complaint_data = PublicComplaintCreate(
            full_name=full_name,
            email_address=email_address,
            phone_number=phone_number,
            address=address,
            complaint_type=complaint_type,
            subject=subject,
            detailed_description=detailed_description
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Save supporting document to S3 if provided
    document_path = None
    if supporting_document and supporting_document.filename:
        document_path = save_uploaded_file_to_s3(supporting_document, "complaints/documents")
    
    # Generate reference ID
    reference_id = generate_reference_id()
    
    # Create complaint
    db_complaint = Complaint(
        complainant_name=full_name,
        email=email_address,
        phone=phone_number,
        address=address,
        type=complaint_type.value,
        subject=subject or "",
        description=detailed_description or "",
        reference_id=reference_id,
        supporting_document_path=document_path,
        status="pending"
    )
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    return {
        "message": "Complaint submitted successfully",
        "reference_id": reference_id,
        "complaint_id": db_complaint.id,
        "status": "pending"
    }

@router.get("/gallery", response_model=PublicGalleryList)
async def get_gallery(
    media_type: Optional[MediaType] = Query(None, description="Filter by media type"),
    db: Session = Depends(get_db)
):
    query = db.query(Gallery)
    
    # Apply media type filter
    if media_type:
        query = query.filter(Gallery.media_type == media_type)
    
    items = query.order_by(Gallery.created_at.desc()).all()
    
    return PublicGalleryList(
        items=[PublicGalleryResponse.from_orm(item) for item in items],
        total=len(items)
    )

@router.get("/member/{membership_id}")
async def get_member_profile(membership_id: str, db: Session = Depends(get_db)):
    """Get member profile by membership ID for QR code scanning"""
    from app.models import Member
    from fastapi.responses import HTMLResponse
    
    member = db.query(Member).filter(Member.membership_id == membership_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Return HTML for better user experience when scanning QR code
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Member Profile - {member.name}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 400px; margin: 0 auto; }}
            .header {{ text-align: center; color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px; }}
            .field {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #555; }}
            .value {{ color: #333; }}
            .status {{ padding: 4px 8px; border-radius: 4px; color: white; font-size: 12px; }}
            .approved {{ background-color: #28a745; }}
            .pending {{ background-color: #ffc107; color: #000; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>Malamahanadu Member</h2>
                <h3>{member.name}</h3>
            </div>
            <div class="field">
                <span class="label">Membership ID:</span>
                <span class="value">{member.membership_id}</span>
            </div>
            <div class="field">
                <span class="label">Phone:</span>
                <span class="value">{member.phone}</span>
            </div>
            <div class="field">
                <span class="label">Email:</span>
                <span class="value">{member.email}</span>
            </div>
            <div class="field">
                <span class="label">Blood Group:</span>
                <span class="value">{member.blood_group or 'Not specified'}</span>
            </div>
            <div class="field">
                <span class="label">Location:</span>
                <span class="value">{member.mandal}, {member.district}, {member.state}</span>
            </div>
            <div class="field">
                <span class="label">Status:</span>
                <span class="status {'approved' if member.status == 'approved' else 'pending'}">{member.status.upper()}</span>
            </div>
            <div class="field">
                <span class="label">Member Since:</span>
                <span class="value">{member.created_at.strftime('%B %d, %Y')}</span>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)