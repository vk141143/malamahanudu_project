from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from app.models import Member, MemberStatus
from app.schemas import MembersSummary, MembersList, MemberResponse, MemberFilters
from typing import List, Optional
import csv
import io
from fastapi.responses import StreamingResponse

def get_members_summary(db: Session) -> MembersSummary:
    """Get members summary for dashboard cards"""
    total_members = db.query(Member).count()
    approved_members = db.query(Member).filter(Member.status == "approved").count()
    pending_members = db.query(Member).filter(Member.status == "pending").count()
    
    return MembersSummary(
        total_members=total_members,
        approved_members=approved_members,
        pending_members=pending_members
    )

def get_members_list(db: Session, filters: MemberFilters) -> MembersList:
    """Get paginated members list with filters"""
    query = db.query(Member)
    
    # Apply search filters
    if filters.search:
        search_term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Member.name.ilike(search_term),
                Member.membership_id.ilike(search_term),
                Member.phone.ilike(search_term),
                Member.email.ilike(search_term),
                Member.aadhaar.ilike(search_term)
            )
        )
    
    # Apply dropdown filters
    if filters.state:
        query = query.filter(Member.state == filters.state)
    
    if filters.district:
        query = query.filter(Member.district == filters.district)
    
    if filters.mandal:
        query = query.filter(Member.mandal == filters.mandal)
    
    if filters.status:
        query = query.filter(Member.status == filters.status)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    offset = (filters.page - 1) * filters.limit
    members = query.order_by(Member.created_at.desc()).offset(offset).limit(filters.limit).all()
    
    # Calculate total pages
    total_pages = (total + filters.limit - 1) // filters.limit
    
    return MembersList(
        members=[MemberResponse.from_orm(member) for member in members],
        total=total,
        page=filters.page,
        limit=filters.limit,
        total_pages=total_pages
    )

def approve_member(db: Session, member_id: int) -> Optional[Member]:
    """Approve a member"""
    member = db.query(Member).filter(Member.id == member_id).first()
    if member:
        member.status = "approved"
        db.commit()
        db.refresh(member)
    return member

def reject_member(db: Session, member_id: int) -> Optional[Member]:
    """Reject a member"""
    member = db.query(Member).filter(Member.id == member_id).first()
    if member:
        member.status = "rejected"
        db.commit()
        db.refresh(member)
    return member

def get_member_by_id(db: Session, member_id: int) -> Optional[Member]:
    """Get member details by ID"""
    return db.query(Member).filter(Member.id == member_id).first()

def export_members_csv(db: Session, filters: MemberFilters) -> StreamingResponse:
    """Export filtered members as CSV"""
    # Get all members matching filters (no pagination for export)
    query = db.query(Member)
    
    # Apply same filters as get_members_list
    if filters.search:
        search_term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Member.name.ilike(search_term),
                Member.membership_id.ilike(search_term),
                Member.phone.ilike(search_term),
                Member.email.ilike(search_term),
                Member.aadhaar.ilike(search_term)
            )
        )
    
    if filters.state:
        query = query.filter(Member.state == filters.state)
    
    if filters.district:
        query = query.filter(Member.district == filters.district)
    
    if filters.mandal:
        query = query.filter(Member.mandal == filters.mandal)
    
    if filters.status:
        query = query.filter(Member.status == filters.status)
    
    members = query.order_by(Member.created_at.desc()).all()
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Membership ID', 'Name', 'Phone', 'Email', 'Aadhaar',
        'State', 'District', 'Mandal', 'Status', 'Registration Date'
    ])
    
    # Write data
    for member in members:
        writer.writerow([
            member.membership_id,
            member.name,
            member.phone,
            member.email,
            member.aadhaar,
            member.state,
            member.district,
            member.mandal,
            member.status,
            member.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=members_export.csv'}
    )

def get_filter_options(db: Session):
    """Get unique values for dropdown filters"""
    states = db.query(Member.state).distinct().all()
    districts = db.query(Member.district).distinct().all()
    mandals = db.query(Member.mandal).distinct().all()
    
    return {
        'states': [state[0] for state in states],
        'districts': [district[0] for district in districts],
        'mandals': [mandal[0] for mandal in mandals]
    }