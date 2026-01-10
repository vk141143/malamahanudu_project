from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MemberStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class DonationStatus(str, Enum):
    pending = "pending"
    verified = "verified"
    acknowledged = "acknowledged"
    failed = "failed"

class PaymentMethod(str, Enum):
    bank_transfer = "bank_transfer"
    upi = "upi"
    cash = "cash"
    cheque = "cheque"
    online_payment = "online_payment"

class ComplaintStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class ComplaintType(str, Enum):
    healthcare = "Healthcare"
    education = "Education"
    employment = "Employment"
    infrastructure = "Infrastructure"
    social_welfare = "Social Welfare"
    other = "Other"

class MediaType(str, Enum):
    image = "image"
    video = "video"

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class AdminResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardSummary(BaseModel):
    total_members: int
    members_growth: int
    total_donations: float
    donation_count: int
    total_complaints: int
    pending_complaints: int
    active_members: int

class MonthlyTrend(BaseModel):
    month: str
    year: int
    members_joined: int
    donations_received: float
    complaints_raised: int

class DistrictDistribution(BaseModel):
    district: str
    member_count: int

# Members Module Schemas
class MembersSummary(BaseModel):
    total_members: int
    approved_members: int
    pending_members: int

class MemberResponse(BaseModel):
    id: int
    membership_id: str
    name: str
    phone: str
    email: str
    aadhaar: str
    state: str
    district: str
    mandal: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MembersList(BaseModel):
    members: List[MemberResponse]
    total: int
    page: int
    limit: int
    total_pages: int

class MemberFilters(BaseModel):
    search: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    mandal: Optional[str] = None
    status: Optional[MemberStatus] = None
    page: int = 1
    limit: int = 10

# Donations Module Schemas
class DonationsSummary(BaseModel):
    total_donations: int
    pending_donations: int
    verified_donations: int
    acknowledged_donations: int
    total_raised_amount: float

class DonationResponse(BaseModel):
    id: int
    donor_name: str
    donor_email: str
    amount: float
    payment_method: str
    transaction_id: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DonationsList(BaseModel):
    donations: List[DonationResponse]
    total: int
    page: int
    limit: int
    total_pages: int

class DonationFilters(BaseModel):
    search: Optional[str] = None
    status: Optional[DonationStatus] = None
    page: int = 1
    limit: int = 10

# Complaints Module Schemas
class ComplaintsSummary(BaseModel):
    total_complaints: int
    pending_complaints: int
    in_progress_complaints: int
    resolved_complaints: int
    closed_complaints: int

class ComplaintResponse(BaseModel):
    id: int
    complainant_name: str
    email: str
    phone: str
    type: str
    subject: str
    description: str
    reference_id: str
    status: str
    admin_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ComplaintsList(BaseModel):
    complaints: List[ComplaintResponse]
    total: int
    page: int
    limit: int
    total_pages: int

class ComplaintFilters(BaseModel):
    search: Optional[str] = None
    status: Optional[ComplaintStatus] = None
    type: Optional[ComplaintType] = None
    page: int = 1
    limit: int = 10

class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus
    admin_notes: Optional[str] = None

# Gallery Module Schemas
class GallerySummary(BaseModel):
    total_items: int
    total_images: int
    total_videos: int

class GalleryResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    media_url: str
    media_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class GalleryList(BaseModel):
    items: List[GalleryResponse]
    total: int
    page: int
    limit: int
    total_pages: int

class GalleryFilters(BaseModel):
    media_type: Optional[MediaType] = None
    page: int = 1
    limit: int = 10

class GalleryCreate(BaseModel):
    title: str
    description: Optional[str] = None

class GalleryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None