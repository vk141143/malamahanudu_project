from fastapi import FastAPI, Depends, HTTPException, status, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import Base, Admin, Member, Donation, Complaint, Gallery
from app.schemas import (
    AdminLogin, Token, AdminResponse, DashboardSummary, MonthlyTrend, DistrictDistribution,
    MembersSummary, MembersList, MemberResponse, MemberFilters, MemberStatus,
    DonationsSummary, DonationsList, DonationResponse, DonationFilters, DonationStatus,
    ComplaintsSummary, ComplaintsList, ComplaintResponse, ComplaintFilters, ComplaintStatus, ComplaintType, ComplaintStatusUpdate,
    GallerySummary, GalleryList, GalleryResponse, GalleryFilters, MediaType, GalleryCreate, GalleryUpdate
)
from app.auth import authenticate_admin, create_access_token, blacklist_token
from app.deps import get_current_admin, security
from app.dashboard import get_dashboard_summary, get_monthly_trends, get_district_distribution
from app.members import (
    get_members_summary, get_members_list, approve_member, reject_member,
    get_member_by_id, export_members_csv, get_filter_options
)
from app.donations import (
    get_donations_summary, get_donations_list, verify_donation, acknowledge_donation,
    get_donation_by_id, export_donations_csv
)
from app.complaints import (
    get_complaints_summary, get_complaints_list, get_complaint_by_id,
    update_complaint_status, export_complaints_csv
)
from app.gallery import (
    get_gallery_summary, get_gallery_list, create_gallery_item, get_gallery_item_by_id,
    update_gallery_item, delete_gallery_item
)
from typing import List, Optional
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Admin Dashboard API")

# Add CORS middleware - MUST be added immediately after FastAPI() creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://malamahanadu.org",
        "https://org.incirclejobs.com",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Import and include routers AFTER CORS middleware
from app.public.routes import router as public_router
app.include_router(public_router)

@app.post("/admin/login", response_model=Token)
async def admin_login(admin_data: AdminLogin, db: Session = Depends(get_db)):
    admin = authenticate_admin(db, admin_data.email, admin_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(data={"sub": admin.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/admin/logout")
async def admin_logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    blacklist_token(db, token)
    return {"message": "Successfully logged out"}

@app.get("/admin/dashboard", response_model=AdminResponse)
async def admin_dashboard(current_admin: Admin = Depends(get_current_admin)):
    return current_admin

# Dashboard APIs
@app.get("/admin/dashboard/summary", response_model=DashboardSummary)
async def dashboard_summary(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get dashboard summary metrics"""
    return get_dashboard_summary(db)

@app.get("/admin/dashboard/monthly-trends", response_model=List[MonthlyTrend])
async def monthly_trends(
    months: int = 6,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get monthly trends for last N months"""
    if months < 1 or months > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Months must be between 1 and 12"
        )
    return get_monthly_trends(db, months)

@app.get("/admin/dashboard/district-distribution", response_model=List[DistrictDistribution])
async def district_distribution(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get member distribution by district"""
    return get_district_distribution(db)

# Members Module APIs
@app.get("/admin/members/summary", response_model=MembersSummary)
async def members_summary(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get members summary for dashboard cards"""
    return get_members_summary(db)

@app.get("/admin/members", response_model=MembersList)
async def members_list(
    search: Optional[str] = Query(None, description="Search by name, membership ID, phone, email, or aadhaar"),
    state: Optional[str] = Query(None, description="Filter by state"),
    district: Optional[str] = Query(None, description="Filter by district"),
    mandal: Optional[str] = Query(None, description="Filter by mandal"),
    status: Optional[MemberStatus] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get paginated members list with search and filters"""
    filters = MemberFilters(
        search=search,
        state=state,
        district=district,
        mandal=mandal,
        status=status,
        page=page,
        limit=limit
    )
    return get_members_list(db, filters)

@app.get("/admin/members/export")
async def export_members(
    search: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    mandal: Optional[str] = Query(None),
    status: Optional[MemberStatus] = Query(None),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Export filtered members as CSV"""
    filters = MemberFilters(
        search=search,
        state=state,
        district=district,
        mandal=mandal,
        status=status,
        page=1,
        limit=999999
    )
    return export_members_csv(db, filters)

@app.get("/admin/members/filter-options")
async def members_filter_options(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get available filter options for dropdowns"""
    return get_filter_options(db)

@app.get("/admin/members/{member_id}", response_model=MemberResponse)
async def member_details(
    member_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get member details by ID"""
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    return member

@app.post("/admin/members/{member_id}/approve", response_model=MemberResponse)
async def approve_member_action(
    member_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Approve a member"""
    member = approve_member(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    return member

@app.post("/admin/members/{member_id}/reject", response_model=MemberResponse)
async def reject_member_action(
    member_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Reject a member"""
    member = reject_member(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    return member


# Member Applications APIs
@app.get("/admin/member-applications")
async def get_member_applications(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get member applications list"""
    from app.models import MemberApplication
    
    query = db.query(MemberApplication)
    
    if status:
        query = query.filter(MemberApplication.status == status)
    
    total = query.count()
    offset = (page - 1) * limit
    applications = query.order_by(MemberApplication.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "applications": applications,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }

@app.post("/admin/member-applications/{application_id}/approve")
async def approve_member_application(
    application_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Approve member application and create member"""
    from app.models import MemberApplication, Member
    import uuid
    
    application = db.query(MemberApplication).filter(MemberApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Create member from application
    member = Member(
        membership_id=f"MEM{str(uuid.uuid4())[:8].upper()}",
        name=application.full_name,
        phone=application.phone_number,
        email=application.email_address or "",
        aadhaar=application.aadhaar_number,
        state=application.state,
        district=application.district,
        mandal=application.mandal,
        photo_path=application.photo_path,
        status="approved"
    )
    
    db.add(member)
    application.status = "approved"
    db.commit()
    
    return {"message": "Member application approved", "member_id": member.id}

@app.post("/admin/member-applications/{application_id}/reject")
async def reject_member_application(
    application_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Reject member application"""
    from app.models import MemberApplication
    
    application = db.query(MemberApplication).filter(MemberApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.status = "rejected"
    db.commit()
    
    return {"message": "Member application rejected"}

# Donations Module APIs
@app.get("/admin/donations/summary", response_model=DonationsSummary)
async def donations_summary(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get donations summary for dashboard cards"""
    return get_donations_summary(db)

@app.get("/admin/donations", response_model=DonationsList)
async def donations_list(
    search: Optional[str] = Query(None, description="Search by donor name, email, or transaction ID"),
    status: Optional[DonationStatus] = Query(None, description="Filter by donation status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get paginated donations list with search and filters"""
    filters = DonationFilters(
        search=search,
        status=status,
        page=page,
        limit=limit
    )
    return get_donations_list(db, filters)

@app.get("/admin/donations/{donation_id}", response_model=DonationResponse)
async def donation_details(
    donation_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get donation details by ID"""
    donation = get_donation_by_id(db, donation_id)
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )
    return donation

@app.post("/admin/donations/{donation_id}/verify", response_model=DonationResponse)
async def verify_donation_action(
    donation_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Verify a donation"""
    donation = verify_donation(db, donation_id)
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )
    return donation

@app.post("/admin/donations/{donation_id}/acknowledge", response_model=DonationResponse)
async def acknowledge_donation_action(
    donation_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Acknowledge a donation"""
    donation = acknowledge_donation(db, donation_id)
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donation not found or must be verified before acknowledgement"
        )
    return donation

@app.get("/admin/donations/export")
async def export_donations(
    search: Optional[str] = Query(None),
    status: Optional[DonationStatus] = Query(None),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Export filtered donations as CSV"""
    filters = DonationFilters(
        search=search,
        status=status,
        page=1,
        limit=999999  # Export all matching records
    )
    return export_donations_csv(db, filters)

# Complaints Module APIs
@app.get("/admin/complaints/summary", response_model=ComplaintsSummary)
async def complaints_summary(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get complaints summary for dashboard cards"""
    return get_complaints_summary(db)

@app.get("/admin/complaints", response_model=ComplaintsList)
async def complaints_list(
    search: Optional[str] = Query(None, description="Search by name, email, reference ID, or subject"),
    status: Optional[ComplaintStatus] = Query(None, description="Filter by complaint status"),
    type: Optional[ComplaintType] = Query(None, description="Filter by complaint type"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get paginated complaints list with search and filters"""
    filters = ComplaintFilters(
        search=search,
        status=status,
        type=type,
        page=page,
        limit=limit
    )
    return get_complaints_list(db, filters)

@app.get("/admin/complaints/{complaint_id}", response_model=ComplaintResponse)
async def complaint_details(
    complaint_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get complaint details by ID"""
    complaint = get_complaint_by_id(db, complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    return complaint

@app.patch("/admin/complaints/{complaint_id}/status", response_model=ComplaintResponse)
async def update_complaint_status_action(
    complaint_id: int,
    status_update: ComplaintStatusUpdate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update complaint status and admin notes"""
    complaint = update_complaint_status(db, complaint_id, status_update)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    return complaint

@app.get("/admin/complaints/export")
async def export_complaints(
    search: Optional[str] = Query(None),
    status: Optional[ComplaintStatus] = Query(None),
    type: Optional[ComplaintType] = Query(None),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Export filtered complaints as CSV"""
    filters = ComplaintFilters(
        search=search,
        status=status,
        type=type,
        page=1,
        limit=999999  # Export all matching records
    )
    return export_complaints_csv(db, filters)

# Gallery Module APIs
@app.get("/admin/gallery/summary", response_model=GallerySummary)
async def gallery_summary(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get gallery summary for overview"""
    return get_gallery_summary(db)

@app.get("/admin/gallery", response_model=GalleryList)
async def gallery_list(
    media_type: Optional[MediaType] = Query(None, description="Filter by media type"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get paginated gallery list with filters"""
    filters = GalleryFilters(
        media_type=media_type,
        page=page,
        limit=limit
    )
    return get_gallery_list(db, filters)

@app.post("/admin/gallery", response_model=GalleryResponse)
async def create_gallery(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create new gallery item with file upload"""
    gallery_data = GalleryCreate(title=title, description=description)
    return create_gallery_item(db, gallery_data, file)

@app.get("/admin/gallery/{item_id}", response_model=GalleryResponse)
async def gallery_item_details(
    item_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get gallery item details by ID"""
    item = get_gallery_item_by_id(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery item not found"
        )
    return item

@app.put("/admin/gallery/{item_id}", response_model=GalleryResponse)
async def update_gallery(
    item_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update gallery item"""
    gallery_data = GalleryUpdate(title=title, description=description)
    item = update_gallery_item(db, item_id, gallery_data, file)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery item not found"
        )
    return item

@app.delete("/admin/gallery/{item_id}")
async def delete_gallery(
    item_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete gallery item"""
    success = delete_gallery_item(db, item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery item not found"
        )
    return {"message": "Gallery item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)