from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Enum, Text, Date
from sqlalchemy.sql import func
from app.database import Base
import enum

class DonationStatus(enum.Enum):
    pending = "pending"
    verified = "verified"
    acknowledged = "acknowledged"
    failed = "failed"

class PaymentMethod(enum.Enum):
    bank_transfer = "bank_transfer"
    upi = "upi"
    cash = "cash"
    cheque = "cheque"
    online_payment = "online_payment"

class ComplaintStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class ComplaintType(enum.Enum):
    healthcare = "Healthcare"
    education = "Education"
    employment = "Employment"
    infrastructure = "Infrastructure"
    social_welfare = "Social Welfare"
    other = "Other"

class MemberStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class MediaType(enum.Enum):
    image = "image"
    video = "video"

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    membership_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    aadhaar = Column(String, nullable=False, index=True)
    state = Column(String, nullable=False, index=True)
    district = Column(String, nullable=False, index=True)
    mandal = Column(String, nullable=False, index=True)
    status = Column(String, default="pending", index=True)
    is_active = Column(Boolean, default=True)
    id_card_generated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MemberApplication(Base):
    __tablename__ = "member_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    father_husband_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    caste = Column(String, nullable=False)
    aadhaar_number = Column(String, nullable=False, index=True)
    phone_number = Column(String, nullable=False, index=True)
    email_address = Column(String)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    mandal = Column(String, nullable=False)
    village = Column(String, nullable=False)
    full_address = Column(Text, nullable=False)
    photo_path = Column(String)
    status = Column(String, default="pending", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    donor_name = Column(String, nullable=False, index=True)
    donor_email = Column(String, nullable=False, index=True)
    phone_number = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False, index=True)
    notes = Column(Text)
    status = Column(String, default="pending", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    complainant_name = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    phone = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    type = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    reference_id = Column(String, unique=True, index=True, nullable=False)
    supporting_document_path = Column(String)
    status = Column(String, default="pending", index=True)
    admin_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Gallery(Base):
    __tablename__ = "gallery"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    media_url = Column(String, nullable=False)
    media_type = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())