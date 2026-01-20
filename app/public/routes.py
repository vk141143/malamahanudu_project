from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
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