from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models import Complaint, ComplaintStatus
from app.schemas import ComplaintsSummary, ComplaintsList, ComplaintResponse, ComplaintFilters, ComplaintStatusUpdate
from typing import Optional
import csv
import io
from fastapi.responses import StreamingResponse

def get_complaints_summary(db: Session) -> ComplaintsSummary:
    """Get complaints summary for dashboard cards"""
    total_complaints = db.query(Complaint).count()
    pending_complaints = db.query(Complaint).filter(Complaint.status == "pending").count()
    in_progress_complaints = db.query(Complaint).filter(Complaint.status == "in_progress").count()
    resolved_complaints = db.query(Complaint).filter(Complaint.status == "resolved").count()
    closed_complaints = db.query(Complaint).filter(Complaint.status == "closed").count()
    
    return ComplaintsSummary(
        total_complaints=total_complaints,
        pending_complaints=pending_complaints,
        in_progress_complaints=in_progress_complaints,
        resolved_complaints=resolved_complaints,
        closed_complaints=closed_complaints
    )

def get_complaints_list(db: Session, filters: ComplaintFilters) -> ComplaintsList:
    """Get paginated complaints list with search and filters"""
    query = db.query(Complaint)
    
    # Apply search filter
    if filters.search:
        search_term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Complaint.complainant_name.ilike(search_term),
                Complaint.email.ilike(search_term),
                Complaint.reference_id.ilike(search_term),
                Complaint.subject.ilike(search_term)
            )
        )
    
    # Apply status filter
    if filters.status:
        query = query.filter(Complaint.status == filters.status)
    
    # Apply type filter
    if filters.type:
        query = query.filter(Complaint.type == filters.type)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    offset = (filters.page - 1) * filters.limit
    complaints = query.order_by(Complaint.created_at.desc()).offset(offset).limit(filters.limit).all()
    
    # Calculate total pages
    total_pages = (total + filters.limit - 1) // filters.limit
    
    return ComplaintsList(
        complaints=[ComplaintResponse.from_orm(complaint) for complaint in complaints],
        total=total,
        page=filters.page,
        limit=filters.limit,
        total_pages=total_pages
    )

def get_complaint_by_id(db: Session, complaint_id: int) -> Optional[Complaint]:
    """Get complaint details by ID"""
    return db.query(Complaint).filter(Complaint.id == complaint_id).first()

def update_complaint_status(db: Session, complaint_id: int, status_update: ComplaintStatusUpdate) -> Optional[Complaint]:
    """Update complaint status and admin notes"""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if complaint:
        complaint.status = status_update.status.value
        if status_update.admin_notes:
            complaint.admin_notes = status_update.admin_notes
        db.commit()
        db.refresh(complaint)
    return complaint

def export_complaints_csv(db: Session, filters: ComplaintFilters) -> StreamingResponse:
    """Export filtered complaints as CSV"""
    # Get all complaints matching filters (no pagination for export)
    query = db.query(Complaint)
    
    # Apply same filters as get_complaints_list
    if filters.search:
        search_term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Complaint.complainant_name.ilike(search_term),
                Complaint.email.ilike(search_term),
                Complaint.reference_id.ilike(search_term),
                Complaint.subject.ilike(search_term)
            )
        )
    
    if filters.status:
        query = query.filter(Complaint.status == filters.status)
    
    if filters.type:
        query = query.filter(Complaint.type == filters.type)
    
    complaints = query.order_by(Complaint.created_at.desc()).all()
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Reference ID', 'Complainant Name', 'Email', 'Phone', 'Type',
        'Subject', 'Status', 'Created Date', 'Admin Notes'
    ])
    
    # Write data
    for complaint in complaints:
        writer.writerow([
            complaint.reference_id,
            complaint.complainant_name,
            complaint.email,
            complaint.phone,
            complaint.type,
            complaint.subject,
            complaint.status,
            complaint.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            complaint.admin_notes or ''
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=complaints_export.csv'}
    )