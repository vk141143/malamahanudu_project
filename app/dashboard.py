from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta
from app.models import Member, Donation, Complaint, DonationStatus, ComplaintStatus
from app.schemas import DashboardSummary, MonthlyTrend, DistrictDistribution
from typing import List

def get_dashboard_summary(db: Session) -> DashboardSummary:
    # Current month start for growth calculation
    current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Total members
    total_members = db.query(Member).count()
    
    # Monthly growth (members joined this month)
    members_growth = db.query(Member).filter(
        Member.created_at >= current_month_start
    ).count()
    
    # Total verified donations (updated for new donation status)
    donation_stats = db.query(
        func.sum(Donation.amount).label('total'),
        func.count(Donation.id).label('count')
    ).filter(Donation.status == "verified").first()
    
    total_donations = float(donation_stats.total or 0)
    donation_count = donation_stats.count or 0
    
    # Complaint stats
    total_complaints = db.query(Complaint).count()
    pending_complaints = db.query(Complaint).filter(
        Complaint.status == "pending"
    ).count()
    
    # Active members (ID card generated)
    active_members = db.query(Member).filter(
        Member.id_card_generated == True
    ).count()
    
    return DashboardSummary(
        total_members=total_members,
        members_growth=members_growth,
        total_donations=total_donations,
        donation_count=donation_count,
        total_complaints=total_complaints,
        pending_complaints=pending_complaints,
        active_members=active_members
    )

def get_monthly_trends(db: Session, months: int = 6) -> List[MonthlyTrend]:
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    # Get monthly data for members
    member_trends = db.query(
        extract('year', Member.created_at).label('year'),
        extract('month', Member.created_at).label('month'),
        func.count(Member.id).label('members_joined')
    ).filter(
        Member.created_at >= start_date
    ).group_by(
        extract('year', Member.created_at),
        extract('month', Member.created_at)
    ).all()
    
    # Get monthly data for donations
    donation_trends = db.query(
        extract('year', Donation.created_at).label('year'),
        extract('month', Donation.created_at).label('month'),
        func.sum(Donation.amount).label('donations_received')
    ).filter(
        and_(
            Donation.created_at >= start_date,
            Donation.status == "verified"
        )
    ).group_by(
        extract('year', Donation.created_at),
        extract('month', Donation.created_at)
    ).all()
    
    # Get monthly data for complaints
    complaint_trends = db.query(
        extract('year', Complaint.created_at).label('year'),
        extract('month', Complaint.created_at).label('month'),
        func.count(Complaint.id).label('complaints_raised')
    ).filter(
        Complaint.created_at >= start_date
    ).group_by(
        extract('year', Complaint.created_at),
        extract('month', Complaint.created_at)
    ).all()
    
    # Combine data by month/year
    trends_dict = {}
    
    # Process member trends
    for trend in member_trends:
        key = (int(trend.year), int(trend.month))
        trends_dict[key] = trends_dict.get(key, {
            'year': int(trend.year),
            'month': int(trend.month),
            'members_joined': 0,
            'donations_received': 0.0,
            'complaints_raised': 0
        })
        trends_dict[key]['members_joined'] = trend.members_joined
    
    # Process donation trends
    for trend in donation_trends:
        key = (int(trend.year), int(trend.month))
        trends_dict[key] = trends_dict.get(key, {
            'year': int(trend.year),
            'month': int(trend.month),
            'members_joined': 0,
            'donations_received': 0.0,
            'complaints_raised': 0
        })
        trends_dict[key]['donations_received'] = float(trend.donations_received or 0)
    
    # Process complaint trends
    for trend in complaint_trends:
        key = (int(trend.year), int(trend.month))
        trends_dict[key] = trends_dict.get(key, {
            'year': int(trend.year),
            'month': int(trend.month),
            'members_joined': 0,
            'donations_received': 0.0,
            'complaints_raised': 0
        })
        trends_dict[key]['complaints_raised'] = trend.complaints_raised
    
    # Convert to list and add month names
    month_names = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    
    trends = []
    for (year, month), data in sorted(trends_dict.items()):
        trends.append(MonthlyTrend(
            month=month_names[month - 1],
            year=year,
            members_joined=data['members_joined'],
            donations_received=data['donations_received'],
            complaints_raised=data['complaints_raised']
        ))
    
    return trends

def get_district_distribution(db: Session) -> List[DistrictDistribution]:
    # Group members by district
    district_data = db.query(
        Member.district,
        func.count(Member.id).label('member_count')
    ).group_by(Member.district).order_by(
        func.count(Member.id).desc()
    ).all()
    
    return [
        DistrictDistribution(
            district=district,
            member_count=count
        )
        for district, count in district_data
    ]