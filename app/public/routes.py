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
    full_name: str
    email_address: Optional[EmailStr] = None
    phone_number: str
    payment_method: PaymentMethod
    preset_amount: Optional[float] = None
    custom_amount: Optional[float] = None
    transaction_id: str
    notes: Optional[str] = None
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if not re.match(r'^\d{10}$', v):
            raise ValueError('Phone number must be exactly 10 digits')
        return v

class PublicMembershipCreate(BaseModel):
    full_name: str
    father_husband_name: str
    gender: Gender
    date_of_birth: str  # dd-mm-yyyy format
    caste: str
    aadhaar_number: str
    phone_number: str
    email_address: Optional[EmailStr] = None
    state: str
    district: str
    mandal: str
    village: str
    full_address: str
    
    @validator('full_name', 'father_husband_name', 'caste')
    def validate_letters_only(cls, v):
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError('Field must contain only letters and spaces')
        return v
    
    @validator('aadhaar_number')
    def validate_aadhaar(cls, v):
        if not re.match(r'^\d{12}$', v):
            raise ValueError('Aadhaar number must be exactly 12 digits')
        return v
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if not re.match(r'^\d{10}$', v):
            raise ValueError('Phone number must be exactly 10 digits')
        return v
    
    @validator('date_of_birth')
    def validate_dob(cls, v):
        try:
            datetime.strptime(v, '%d-%m-%Y')
        except ValueError:
            raise ValueError('Date of birth must be in dd-mm-yyyy format')
        return v

class PublicComplaintCreate(BaseModel):
    full_name: str
    email_address: Optional[EmailStr] = None
    phone_number: str
    address: str
    complaint_type: ComplaintType
    subject: str
    detailed_description: str
    
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
        donor_name=donation.full_name,
        donor_email=donation.email_address or "",
        phone_number=donation.phone_number,
        amount=final_amount,
        payment_method=donation.payment_method.value,
        transaction_id=donation.transaction_id,
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
    full_name: str = Form(...),
    father_husband_name: str = Form(...),
    gender: Gender = Form(...),
    date_of_birth: str = Form(...),
    caste: str = Form(...),
    aadhaar_number: str = Form(...),
    phone_number: str = Form(...),
    email_address: Optional[str] = Form(None),
    state: str = Form(...),
    district: str = Form(...),
    mandal: str = Form(...),
    village: str = Form(...),
    full_address: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate form data using Pydantic
    try:
        membership_data = PublicMembershipCreate(
            full_name=full_name,
            father_husband_name=father_husband_name,
            gender=gender,
            date_of_birth=date_of_birth,
            caste=caste,
            aadhaar_number=aadhaar_number,
            phone_number=phone_number,
            email_address=email_address,
            state=state,
            district=district,
            mandal=mandal,
            village=village,
            full_address=full_address
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Save photo to S3
    photo_path = save_uploaded_file_to_s3(photo, "membership/photos")
    
    # Convert date format
    dob = datetime.strptime(date_of_birth, '%d-%m-%Y').date()
    
    # Create membership application
    db_application = MemberApplication(
        full_name=full_name,
        father_husband_name=father_husband_name,
        gender=gender.value,
        date_of_birth=dob,
        caste=caste,
        aadhaar_number=aadhaar_number,
        phone_number=phone_number,
        email_address=email_address,
        state=state,
        district=district,
        mandal=mandal,
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

@router.post("/complaints")
async def create_complaint(
    full_name: str = Form(...),
    phone_number: str = Form(...),
    address: str = Form(...),
    complaint_type: ComplaintType = Form(...),
    subject: str = Form(...),
    detailed_description: str = Form(...),
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
        subject=subject,
        description=detailed_description,
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