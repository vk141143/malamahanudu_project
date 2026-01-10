from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models import Donation, DonationStatus
from app.schemas import DonationsSummary, DonationsList, DonationResponse, DonationFilters
from typing import Optional
import csv
import io
from fastapi.responses import StreamingResponse

def get_donations_summary(db: Session) -> DonationsSummary:
    """Get donations summary for dashboard cards"""
    total_donations = db.query(Donation).count()
    pending_donations = db.query(Donation).filter(Donation.status == "pending").count()
    verified_donations = db.query(Donation).filter(Donation.status == "verified").count()
    acknowledged_donations = db.query(Donation).filter(Donation.status == "acknowledged").count()
    
    # Total raised amount from verified AND acknowledged donations
    total_raised = db.query(func.sum(Donation.amount)).filter(
        or_(Donation.status == "verified", Donation.status == "acknowledged")
    ).scalar() or 0.0
    
    return DonationsSummary(
        total_donations=total_donations,
        pending_donations=pending_donations,
        verified_donations=verified_donations,
        acknowledged_donations=acknowledged_donations,
        total_raised_amount=float(total_raised)
    )

def get_donations_list(db: Session, filters: DonationFilters) -> DonationsList:
    """Get paginated donations list with search and filters"""
    query = db.query(Donation)
    
    # Apply search filter
    if filters.search:
        search_term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Donation.donor_name.ilike(search_term),
                Donation.donor_email.ilike(search_term),
                Donation.transaction_id.ilike(search_term)
            )
        )
    
    # Apply status filter
    if filters.status:
        query = query.filter(Donation.status == filters.status)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    offset = (filters.page - 1) * filters.limit
    donations = query.order_by(Donation.created_at.desc()).offset(offset).limit(filters.limit).all()
    
    # Calculate total pages
    total_pages = (total + filters.limit - 1) // filters.limit
    
    return DonationsList(
        donations=[DonationResponse.from_orm(donation) for donation in donations],
        total=total,
        page=filters.page,
        limit=filters.limit,
        total_pages=total_pages
    )

def verify_donation(db: Session, donation_id: int) -> Optional[Donation]:
    """Verify a donation"""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if donation:
        donation.status = "verified"
        db.commit()
        db.refresh(donation)
    return donation

def acknowledge_donation(db: Session, donation_id: int) -> Optional[Donation]:
    """Acknowledge a donation"""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if donation:
        if donation.status != "verified":
            return None  # Only verified donations can be acknowledged
        donation.status = "acknowledged"
        db.commit()
        db.refresh(donation)
    return donation

def get_donation_by_id(db: Session, donation_id: int) -> Optional[Donation]:
    """Get donation details by ID"""
    return db.query(Donation).filter(Donation.id == donation_id).first()

def export_donations_csv(db: Session, filters: DonationFilters) -> StreamingResponse:
    """Export filtered donations as CSV"""
    # Get all donations matching filters (no pagination for export)
    query = db.query(Donation)
    
    # Apply same filters as get_donations_list
    if filters.search:
        search_term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Donation.donor_name.ilike(search_term),
                Donation.donor_email.ilike(search_term),
                Donation.transaction_id.ilike(search_term)
            )
        )
    
    if filters.status:
        query = query.filter(Donation.status == filters.status)
    
    donations = query.order_by(Donation.created_at.desc()).all()
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Donor Name', 'Donor Email', 'Amount', 'Payment Method',
        'Transaction ID', 'Status', 'Date'
    ])
    
    # Write data
    for donation in donations:
        writer.writerow([
            donation.donor_name,
            donation.donor_email,
            donation.amount,
            donation.payment_method,
            donation.transaction_id,
            donation.status,
            donation.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=donations_export.csv'}
    )