"""
Highland Tower Development - Progress Photos Management Backend
Enterprise-grade photo documentation with approval workflows and organization.
"""

import json
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class PhotoStatus(Enum):
    UPLOADED = "Uploaded"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    ARCHIVED = "Archived"

class PhotoCategory(Enum):
    PROGRESS = "Progress Documentation"
    QUALITY = "Quality Control"
    SAFETY = "Safety Compliance"
    MILESTONE = "Milestone Achievement"
    DEFECT = "Defect Documentation"
    BEFORE_AFTER = "Before/After Comparison"
    INSPECTION = "Inspection Documentation"

class ViewAngle(Enum):
    OVERVIEW = "Overview"
    DETAIL = "Detail View"
    CLOSEUP = "Close-up"
    AERIAL = "Aerial View"
    INTERIOR = "Interior View"
    EXTERIOR = "Exterior View"

@dataclass
class PhotoMetadata:
    """Photo metadata and technical information"""
    file_size: int
    resolution: str
    format: str
    camera_model: Optional[str]
    gps_coordinates: Optional[str]
    weather_conditions: Optional[str]

@dataclass
class PhotoReview:
    """Photo review and approval record"""
    review_id: str
    reviewer_name: str
    reviewer_role: str
    review_date: str
    action: str  # "Approved", "Rejected", "Needs Revision"
    comments: str
    rating: Optional[int]  # 1-5 star rating

@dataclass
class ProgressPhoto:
    """Complete progress photo record"""
    photo_id: str
    photo_number: str
    title: str
    description: str
    category: PhotoCategory
    status: PhotoStatus
    
    # Project details
    project_name: str
    location: str
    work_package: str
    floor_level: Optional[str]
    view_angle: ViewAngle
    
    # Capture details
    captured_date: str
    captured_time: str
    captured_by: str
    camera_operator: str
    
    # Technical data
    filename: str
    metadata: PhotoMetadata
    
    # Organization
    tags: List[str]
    album_id: Optional[str]
    sequence_number: int
    
    # Reviews and approvals
    reviews: List[PhotoReview]
    approval_required: bool
    approved_by: Optional[str]
    approved_date: Optional[str]
    
    # References
    related_rfi: Optional[str]
    related_submittal: Optional[str]
    related_inspection: Optional[str]
    drawing_references: List[str]
    
    # Notes
    photographer_notes: str
    reviewer_notes: str
    
    created_at: str
    updated_at: str

@dataclass
class PhotoAlbum:
    """Photo album for organizing related photos"""
    album_id: str
    name: str
    description: str
    project_name: str
    category: PhotoCategory
    created_by: str
    created_date: str
    photo_count: int
    cover_photo_id: Optional[str]
    
    # Organization
    tags: List[str]
    work_package: str
    date_range_start: str
    date_range_end: str
    
    # Access control
    visibility: str  # "Public", "Project Team", "Management Only"
    access_permissions: List[str]

class ProgressPhotosManager:
    """Enterprise progress photos management system"""
    
    def __init__(self):
        self.photos: Dict[str, ProgressPhoto] = {}
        self.albums: Dict[str, PhotoAlbum] = {}
        self.next_photo_number = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample photo data"""
        
        # Sample photo album
        sample_album = PhotoAlbum(
            album_id="album-001",
            name="Level 15 Structural Progress",
            description="Structural concrete and steel installation progress for Level 15",
            project_name="Highland Tower Development",
            category=PhotoCategory.PROGRESS,
            created_by="Mike Johnson",
            created_date="2025-05-20",
            photo_count=3,
            cover_photo_id="photo-001",
            tags=["Level 15", "Structural", "Concrete", "Steel"],
            work_package="Structure",
            date_range_start="2025-05-20",
            date_range_end="2025-05-27",
            visibility="Project Team",
            access_permissions=["Project Manager", "Site Supervisor", "Structural Engineer"]
        )
        
        # Sample photo 1 - Approved progress photo
        sample_photo_1 = ProgressPhoto(
            photo_id="photo-001",
            photo_number="HTD-P-2025-001",
            title="Level 15 Concrete Pour - North Wing",
            description="Concrete placement in progress for Level 15 north wing slab",
            category=PhotoCategory.PROGRESS,
            status=PhotoStatus.APPROVED,
            project_name="Highland Tower Development",
            location="Level 15 - North Wing",
            work_package="Structure",
            floor_level="Level 15",
            view_angle=ViewAngle.OVERVIEW,
            captured_date="2025-05-25",
            captured_time="10:30",
            captured_by="Mike Johnson",
            camera_operator="Site Photography Team",
            filename="HTD_L15_Concrete_Pour_20250525_1030.jpg",
            metadata=PhotoMetadata(
                file_size=8421504,
                resolution="4032x3024",
                format="JPEG",
                camera_model="Canon EOS R5",
                gps_coordinates="40.7589, -73.9851",
                weather_conditions="Clear, 72°F"
            ),
            tags=["concrete", "pour", "level-15", "north-wing", "structural"],
            album_id="album-001",
            sequence_number=1,
            reviews=[
                PhotoReview(
                    review_id="rev-001",
                    reviewer_name="John Smith",
                    reviewer_role="Project Manager",
                    review_date="2025-05-25",
                    action="Approved",
                    comments="Good documentation of concrete placement. Quality appears excellent.",
                    rating=5
                )
            ],
            approval_required=True,
            approved_by="John Smith",
            approved_date="2025-05-25",
            related_rfi=None,
            related_submittal="sub-001",
            related_inspection="insp-001",
            drawing_references=["S-301", "S-302"],
            photographer_notes="Concrete pour proceeding smoothly, good weather conditions",
            reviewer_notes="Approved for project documentation and client presentation",
            created_at="2025-05-25 10:45:00",
            updated_at="2025-05-25 15:20:00"
        )
        
        # Sample photo 2 - Under review
        sample_photo_2 = ProgressPhoto(
            photo_id="photo-002",
            photo_number="HTD-P-2025-002",
            title="MEP Rough-in Installation",
            description="HVAC ductwork and electrical conduit installation in Level 12 ceiling",
            category=PhotoCategory.PROGRESS,
            status=PhotoStatus.UNDER_REVIEW,
            project_name="Highland Tower Development",
            location="Level 12 - Mechanical Room",
            work_package="MEP Systems",
            floor_level="Level 12",
            view_angle=ViewAngle.DETAIL,
            captured_date="2025-05-27",
            captured_time="14:15",
            captured_by="Tom Brown",
            camera_operator="MEP Team",
            filename="HTD_L12_MEP_Roughin_20250527_1415.jpg",
            metadata=PhotoMetadata(
                file_size=6291456,
                resolution="3840x2160",
                format="JPEG",
                camera_model="iPhone 14 Pro",
                gps_coordinates="40.7589, -73.9851",
                weather_conditions="Indoor"
            ),
            tags=["mep", "hvac", "electrical", "level-12", "rough-in"],
            album_id=None,
            sequence_number=1,
            reviews=[],
            approval_required=True,
            approved_by=None,
            approved_date=None,
            related_rfi="rfi-002",
            related_submittal="sub-002",
            related_inspection="insp-002",
            drawing_references=["M-401", "E-201"],
            photographer_notes="Ductwork installation 80% complete, coordinate with electrical",
            reviewer_notes="",
            created_at="2025-05-27 14:30:00",
            updated_at="2025-05-27 14:30:00"
        )
        
        # Sample photo 3 - Quality control
        sample_photo_3 = ProgressPhoto(
            photo_id="photo-003",
            photo_number="HTD-P-2025-003",
            title="Curtain Wall Installation Quality Check",
            description="Detail view of curtain wall glazing installation showing proper sealant application",
            category=PhotoCategory.QUALITY,
            status=PhotoStatus.APPROVED,
            project_name="Highland Tower Development",
            location="East Facade - Level 10",
            work_package="Facade",
            floor_level="Level 10",
            view_angle=ViewAngle.CLOSEUP,
            captured_date="2025-05-26",
            captured_time="16:00",
            captured_by="Lisa Chen",
            camera_operator="Quality Control Team",
            filename="HTD_Facade_QC_Detail_20250526_1600.jpg",
            metadata=PhotoMetadata(
                file_size=5242880,
                resolution="4000x3000",
                format="JPEG",
                camera_model="Nikon D850",
                gps_coordinates="40.7589, -73.9851",
                weather_conditions="Partly cloudy, 68°F"
            ),
            tags=["curtain-wall", "glazing", "quality-control", "sealant", "facade"],
            album_id="album-001",
            sequence_number=3,
            reviews=[
                PhotoReview(
                    review_id="rev-002",
                    reviewer_name="Sarah Wilson",
                    reviewer_role="Quality Manager",
                    review_date="2025-05-26",
                    action="Approved",
                    comments="Excellent documentation of proper sealant application technique.",
                    rating=5
                )
            ],
            approval_required=True,
            approved_by="Sarah Wilson",
            approved_date="2025-05-26",
            related_rfi=None,
            related_submittal="sub-003",
            related_inspection="insp-003",
            drawing_references=["A-301", "A-401"],
            photographer_notes="Sealant application meets specification requirements",
            reviewer_notes="Good quality documentation for training purposes",
            created_at="2025-05-26 16:15:00",
            updated_at="2025-05-26 17:00:00"
        )
        
        self.albums[sample_album.album_id] = sample_album
        self.photos[sample_photo_1.photo_id] = sample_photo_1
        self.photos[sample_photo_2.photo_id] = sample_photo_2
        self.photos[sample_photo_3.photo_id] = sample_photo_3
        self.next_photo_number = 4
    
    def create_photo(self, photo_data: Dict[str, Any]) -> str:
        """Create a new progress photo record"""
        photo_id = f"photo-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        photo_number = f"HTD-P-2025-{self.next_photo_number:03d}"
        
        photo_data.update({
            "photo_id": photo_id,
            "photo_number": photo_number,
            "status": PhotoStatus.UPLOADED,
            "reviews": [],
            "tags": photo_data.get("tags", []),
            "drawing_references": photo_data.get("drawing_references", []),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        photo_data["category"] = PhotoCategory(photo_data["category"])
        photo_data["status"] = PhotoStatus(photo_data["status"])
        photo_data["view_angle"] = ViewAngle(photo_data["view_angle"])
        
        # Handle metadata
        if "metadata" in photo_data:
            photo_data["metadata"] = PhotoMetadata(**photo_data["metadata"])
        
        photo = ProgressPhoto(**photo_data)
        self.photos[photo_id] = photo
        self.next_photo_number += 1
        
        return photo_id
    
    def create_album(self, album_data: Dict[str, Any]) -> str:
        """Create a new photo album"""
        album_id = f"album-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        album_data.update({
            "album_id": album_id,
            "photo_count": 0,
            "created_date": datetime.now().strftime('%Y-%m-%d'),
            "tags": album_data.get("tags", []),
            "access_permissions": album_data.get("access_permissions", [])
        })
        
        # Convert enum
        album_data["category"] = PhotoCategory(album_data["category"])
        
        album = PhotoAlbum(**album_data)
        self.albums[album_id] = album
        
        return album_id
    
    def get_photo(self, photo_id: str) -> Optional[ProgressPhoto]:
        """Get a specific photo"""
        return self.photos.get(photo_id)
    
    def get_all_photos(self) -> List[ProgressPhoto]:
        """Get all photos sorted by date (newest first)"""
        return sorted(self.photos.values(),
                     key=lambda p: p.captured_date,
                     reverse=True)
    
    def get_photos_by_status(self, status: PhotoStatus) -> List[ProgressPhoto]:
        """Get photos by status"""
        return [photo for photo in self.photos.values() if photo.status == status]
    
    def get_photos_by_category(self, category: PhotoCategory) -> List[ProgressPhoto]:
        """Get photos by category"""
        return [photo for photo in self.photos.values() if photo.category == category]
    
    def get_photos_by_album(self, album_id: str) -> List[ProgressPhoto]:
        """Get photos in a specific album"""
        return [photo for photo in self.photos.values() if photo.album_id == album_id]
    
    def add_photo_review(self, photo_id: str, review_data: Dict[str, Any]) -> bool:
        """Add a review to a photo"""
        photo = self.photos.get(photo_id)
        if not photo:
            return False
        
        review_id = f"rev-{len(photo.reviews) + 1:03d}"
        review_data.update({
            "review_id": review_id,
            "review_date": datetime.now().strftime('%Y-%m-%d')
        })
        
        review = PhotoReview(**review_data)
        photo.reviews.append(review)
        
        # Update photo status based on review
        if review.action == "Approved":
            photo.status = PhotoStatus.APPROVED
            photo.approved_by = review.reviewer_name
            photo.approved_date = review.review_date
        elif review.action == "Rejected":
            photo.status = PhotoStatus.REJECTED
        
        photo.updated_at = datetime.now().isoformat()
        return True
    
    def add_photo_to_album(self, photo_id: str, album_id: str) -> bool:
        """Add a photo to an album"""
        photo = self.photos.get(photo_id)
        album = self.albums.get(album_id)
        
        if not photo or not album:
            return False
        
        photo.album_id = album_id
        album.photo_count += 1
        
        # Set as cover photo if first photo
        if album.photo_count == 1:
            album.cover_photo_id = photo_id
        
        return True
    
    def generate_photo_metrics(self) -> Dict[str, Any]:
        """Generate photo documentation metrics"""
        photos = list(self.photos.values())
        albums = list(self.albums.values())
        
        if not photos:
            return {}
        
        total_photos = len(photos)
        
        # Status counts
        status_counts = {}
        for status in PhotoStatus:
            status_counts[status.value] = len([p for p in photos if p.status == status])
        
        # Category counts
        category_counts = {}
        for category in PhotoCategory:
            category_counts[category.value] = len([p for p in photos if p.category == category])
        
        # Review metrics
        photos_with_reviews = [p for p in photos if p.reviews]
        avg_rating = sum(r.rating for p in photos_with_reviews for r in p.reviews if r.rating) / max(sum(len(p.reviews) for p in photos_with_reviews), 1)
        
        # Approval metrics
        approved_photos = len([p for p in photos if p.status == PhotoStatus.APPROVED])
        approval_rate = (approved_photos / total_photos * 100) if total_photos > 0 else 0
        
        # Storage metrics
        total_file_size = sum(p.metadata.file_size for p in photos)
        avg_file_size = total_file_size / total_photos if total_photos > 0 else 0
        
        return {
            "total_photos": total_photos,
            "total_albums": len(albums),
            "status_breakdown": status_counts,
            "category_breakdown": category_counts,
            "approval_rate": round(approval_rate, 1),
            "average_rating": round(avg_rating, 1),
            "total_file_size_mb": round(total_file_size / (1024 * 1024), 1),
            "average_file_size_mb": round(avg_file_size / (1024 * 1024), 1),
            "pending_review": status_counts.get("Under Review", 0)
        }
    
    def validate_photo_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate photo data"""
        errors = []
        
        required_fields = ["title", "category", "location", "captured_date", 
                          "captured_by", "filename", "view_angle"]
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        return errors

# Global instance for use across the application
progress_photos_manager = ProgressPhotosManager()