from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Gallery, MediaType
from app.schemas import GallerySummary, GalleryList, GalleryResponse, GalleryFilters, GalleryCreate, GalleryUpdate
from app.s3_storage import s3_storage
from fastapi import UploadFile, HTTPException, status
from typing import Optional
from pathlib import Path

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm"}

def get_gallery_summary(db: Session) -> GallerySummary:
    """Get gallery summary for overview"""
    total_items = db.query(Gallery).count()
    total_images = db.query(Gallery).filter(Gallery.media_type == "image").count()
    total_videos = db.query(Gallery).filter(Gallery.media_type == "video").count()
    
    return GallerySummary(
        total_items=total_items,
        total_images=total_images,
        total_videos=total_videos
    )

def get_gallery_list(db: Session, filters: GalleryFilters) -> GalleryList:
    """Get paginated gallery list with filters"""
    query = db.query(Gallery)
    
    # Apply media type filter
    if filters.media_type:
        query = query.filter(Gallery.media_type == filters.media_type)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    offset = (filters.page - 1) * filters.limit
    items = query.order_by(Gallery.created_at.desc()).offset(offset).limit(filters.limit).all()
    
    # Calculate total pages
    total_pages = (total + filters.limit - 1) // filters.limit
    
    return GalleryList(
        items=[GalleryResponse.from_orm(item) for item in items],
        total=total,
        page=filters.page,
        limit=filters.limit,
        total_pages=total_pages
    )

def save_uploaded_file(file: UploadFile) -> tuple[str, str]:
    """Save uploaded file to S3 and return URL and media type"""
    # Get file extension
    file_extension = Path(file.filename).suffix.lower()
    
    # Determine media type
    if file_extension in ALLOWED_IMAGE_EXTENSIONS:
        media_type = "image"
        folder = "gallery/images"
    elif file_extension in ALLOWED_VIDEO_EXTENSIONS:
        media_type = "video"
        folder = "gallery/videos"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file_extension}"
        )
    
    # Upload to S3
    media_url = s3_storage.upload_file(file, folder)
    
    return media_url, media_type

def create_gallery_item(db: Session, gallery_data: GalleryCreate, file: UploadFile) -> Gallery:
    """Create new gallery item with file upload"""
    # Save uploaded file
    media_url, media_type = save_uploaded_file(file)
    
    # Create gallery item
    gallery_item = Gallery(
        title=gallery_data.title,
        description=gallery_data.description,
        media_url=media_url,
        media_type=media_type
    )
    
    db.add(gallery_item)
    db.commit()
    db.refresh(gallery_item)
    
    return gallery_item

def get_gallery_item_by_id(db: Session, item_id: int) -> Optional[Gallery]:
    """Get gallery item by ID"""
    return db.query(Gallery).filter(Gallery.id == item_id).first()

def update_gallery_item(db: Session, item_id: int, gallery_data: GalleryUpdate, file: Optional[UploadFile] = None) -> Optional[Gallery]:
    """Update gallery item"""
    gallery_item = db.query(Gallery).filter(Gallery.id == item_id).first()
    if not gallery_item:
        return None
    
    # Update text fields
    if gallery_data.title is not None:
        gallery_item.title = gallery_data.title
    if gallery_data.description is not None:
        gallery_item.description = gallery_data.description
    
    # Update media file if provided
    if file:
        # Delete old file from S3
        s3_storage.delete_file(gallery_item.media_url)
        
        # Save new file to S3
        media_url, media_type = save_uploaded_file(file)
        gallery_item.media_url = media_url
        gallery_item.media_type = media_type
    
    db.commit()
    db.refresh(gallery_item)
    
    return gallery_item

def delete_gallery_item(db: Session, item_id: int) -> bool:
    """Delete gallery item and associated file from S3"""
    gallery_item = db.query(Gallery).filter(Gallery.id == item_id).first()
    if not gallery_item:
        return False
    
    # Delete file from S3
    s3_storage.delete_file(gallery_item.media_url)
    
    # Delete from database
    db.delete(gallery_item)
    db.commit()
    
    return True