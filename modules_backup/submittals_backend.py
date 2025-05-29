"""
Highland Tower Development - Submittals Management Backend
Enterprise-grade submittal tracking with approval workflows and document management.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class SubmittalType(Enum):
    SHOP_DRAWINGS = "Shop Drawings"
    PRODUCT_DATA = "Product Data"
    SAMPLES = "Samples"
    CERTIFICATES = "Certificates"
    TEST_REPORTS = "Test Reports"
    CALCULATIONS = "Calculations"
    O_AND_M_MANUALS = "O&M Manuals"
    WARRANTIES = "Warranties"

class SubmittalStatus(Enum):
    NOT_SUBMITTED = "Not Submitted"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    APPROVED_WITH_COMMENTS = "Approved with Comments"
    REVISE_AND_RESUBMIT = "Revise and Resubmit"
    REJECTED = "Rejected"

class ReviewAction(Enum):
    NO_EXCEPTION_TAKEN = "No Exception Taken"
    MAKE_CORRECTIONS_NOTED = "Make Corrections Noted"
    REVISE_AND_RESUBMIT = "Revise and Resubmit"
    REJECTED = "Rejected"

@dataclass
class SubmittalReview:
    """Individual review of a submittal"""
    review_id: str
    reviewer_name: str
    reviewer_role: str
    review_date: str
    action: ReviewAction
    comments: str
    markup_file: Optional[str]
    signature: str

@dataclass
class SubmittalDocument:
    """Document attached to submittal"""
    doc_id: str
    filename: str
    file_type: str
    file_size: int
    upload_date: str
    uploaded_by: str
    description: str
    revision: str

@dataclass
class Submittal:
    """Complete submittal record"""
    submittal_id: str
    submittal_number: str
    title: str
    description: str
    submittal_type: SubmittalType
    status: SubmittalStatus
    
    # Project details
    project_name: str
    spec_section: str
    drawing_reference: str
    work_package: str
    location: str
    
    # Contractor info
    contractor: str
    subcontractor: str
    contact_person: str
    contact_email: str
    
    # Schedule
    required_date: str
    submitted_date: Optional[str]
    review_period_days: int
    due_date: str
    approved_date: Optional[str]
    
    # Reviews
    reviews: List[SubmittalReview]
    current_revision: str
    total_revisions: int
    
    # Documents
    documents: List[SubmittalDocument]
    
    # Notes
    contractor_notes: str
    design_team_notes: str
    
    # Tracking
    days_in_review: int
    is_overdue: bool
    created_at: str
    updated_at: str
    
    def calculate_days_in_review(self) -> int:
        """Calculate days submittal has been in review"""
        if self.submitted_date and self.status in [SubmittalStatus.SUBMITTED, SubmittalStatus.UNDER_REVIEW]:
            start_date = datetime.strptime(self.submitted_date, '%Y-%m-%d').date()
            return (date.today() - start_date).days
        return 0
    
    def check_overdue_status(self) -> bool:
        """Check if submittal is overdue"""
        if self.status in [SubmittalStatus.APPROVED, SubmittalStatus.REJECTED]:
            return False
        
        due_date = datetime.strptime(self.due_date, '%Y-%m-%d').date()
        return date.today() > due_date

class SubmittalsManager:
    """Enterprise submittals management system"""
    
    def __init__(self):
        self.submittals: Dict[str, Submittal] = {}
        self.next_submittal_number = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample submittal data"""
        
        # Sample submittal 1 - Approved
        sample_submittal_1 = Submittal(
            submittal_id="sub-001",
            submittal_number="SUB-2025-001",
            title="Structural Steel Shop Drawings - Level 15",
            description="Detailed shop drawings for structural steel connections and members for Level 15",
            submittal_type=SubmittalType.SHOP_DRAWINGS,
            status=SubmittalStatus.APPROVED,
            project_name="Highland Tower Development",
            spec_section="05 12 00 - Structural Steel Framing",
            drawing_reference="S-301, S-302",
            work_package="Structure",
            location="Level 15",
            contractor="Highland Construction Co.",
            subcontractor="Steel Fabricators Inc.",
            contact_person="Mike Johnson",
            contact_email="mjohnson@steelfab.com",
            required_date="2025-05-15",
            submitted_date="2025-05-10",
            review_period_days=10,
            due_date="2025-05-20",
            approved_date="2025-05-18",
            reviews=[
                SubmittalReview(
                    review_id="rev-001",
                    reviewer_name="Sarah Wilson",
                    reviewer_role="Structural Engineer",
                    review_date="2025-05-18",
                    action=ReviewAction.NO_EXCEPTION_TAKEN,
                    comments="Shop drawings are complete and conform to design intent. No exceptions taken.",
                    markup_file="markup_sub001_rev1.pdf",
                    signature="S. Wilson, PE"
                )
            ],
            current_revision="1",
            total_revisions=1,
            documents=[
                SubmittalDocument(
                    doc_id="doc-001",
                    filename="steel_shop_drawings_L15.pdf",
                    file_type="PDF",
                    file_size=15728640,
                    upload_date="2025-05-10",
                    uploaded_by="Mike Johnson",
                    description="Level 15 structural steel shop drawings",
                    revision="1"
                )
            ],
            contractor_notes="All steel members fabricated per AISC standards",
            design_team_notes="Approved for construction. Proceed with fabrication.",
            days_in_review=8,
            is_overdue=False,
            created_at="2025-05-10 09:00:00",
            updated_at="2025-05-18 16:30:00"
        )
        
        # Sample submittal 2 - Under Review
        sample_submittal_2 = Submittal(
            submittal_id="sub-002",
            submittal_number="SUB-2025-002",
            title="HVAC Equipment Data - Rooftop Units",
            description="Product data sheets for rooftop HVAC units",
            submittal_type=SubmittalType.PRODUCT_DATA,
            status=SubmittalStatus.UNDER_REVIEW,
            project_name="Highland Tower Development",
            spec_section="23 31 00 - HVAC Ducts and Casings",
            drawing_reference="M-401, M-402",
            work_package="MEP Systems",
            location="Rooftop",
            contractor="Highland MEP Contractors",
            subcontractor="Climate Control Systems",
            contact_person="Tom Brown",
            contact_email="tbrown@climatecontrol.com",
            required_date="2025-06-01",
            submitted_date="2025-05-25",
            review_period_days=14,
            due_date="2025-06-08",
            approved_date=None,
            reviews=[],
            current_revision="1",
            total_revisions=1,
            documents=[
                SubmittalDocument(
                    doc_id="doc-002",
                    filename="hvac_product_data.pdf",
                    file_type="PDF",
                    file_size=8421504,
                    upload_date="2025-05-25",
                    uploaded_by="Tom Brown",
                    description="Rooftop HVAC unit specifications",
                    revision="1"
                )
            ],
            contractor_notes="Equipment meets all specified performance requirements",
            design_team_notes="",
            days_in_review=2,
            is_overdue=False,
            created_at="2025-05-25 14:00:00",
            updated_at="2025-05-25 14:00:00"
        )
        
        # Sample submittal 3 - Revise and Resubmit
        sample_submittal_3 = Submittal(
            submittal_id="sub-003",
            submittal_number="SUB-2025-003",
            title="Curtain Wall Shop Drawings - East Facade",
            description="Shop drawings for curtain wall system on east facade",
            submittal_type=SubmittalType.SHOP_DRAWINGS,
            status=SubmittalStatus.REVISE_AND_RESUBMIT,
            project_name="Highland Tower Development",
            spec_section="08 44 00 - Curtain Wall Systems",
            drawing_reference="A-301, A-401",
            work_package="Facade",
            location="East Facade - Levels 5-15",
            contractor="Highland Construction Co.",
            subcontractor="Facade Systems Ltd.",
            contact_person="Lisa Chen",
            contact_email="lchen@facadesystems.com",
            required_date="2025-05-20",
            submitted_date="2025-05-15",
            review_period_days=10,
            due_date="2025-05-25",
            approved_date=None,
            reviews=[
                SubmittalReview(
                    review_id="rev-002",
                    reviewer_name="John Smith",
                    reviewer_role="Architect",
                    review_date="2025-05-22",
                    action=ReviewAction.REVISE_AND_RESUBMIT,
                    comments="Revise glazing details at Level 10 transition. Update thermal calculations for energy compliance.",
                    markup_file="markup_sub003_rev1.pdf",
                    signature="J. Smith, AIA"
                )
            ],
            current_revision="1",
            total_revisions=1,
            documents=[
                SubmittalDocument(
                    doc_id="doc-003",
                    filename="curtain_wall_drawings.pdf",
                    file_type="PDF",
                    file_size=25165824,
                    upload_date="2025-05-15",
                    uploaded_by="Lisa Chen",
                    description="East facade curtain wall shop drawings",
                    revision="1"
                )
            ],
            contractor_notes="Initial submission based on design development drawings",
            design_team_notes="Revisions required for energy code compliance",
            days_in_review=7,
            is_overdue=True,
            created_at="2025-05-15 11:00:00",
            updated_at="2025-05-22 15:45:00"
        )
        
        self.submittals[sample_submittal_1.submittal_id] = sample_submittal_1
        self.submittals[sample_submittal_2.submittal_id] = sample_submittal_2
        self.submittals[sample_submittal_3.submittal_id] = sample_submittal_3
        self.next_submittal_number = 4
    
    def create_submittal(self, submittal_data: Dict[str, Any]) -> str:
        """Create a new submittal"""
        submittal_id = f"sub-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        submittal_number = f"SUB-2025-{self.next_submittal_number:03d}"
        
        # Calculate due date based on review period
        required_date = datetime.strptime(submittal_data['required_date'], '%Y-%m-%d')
        review_days = submittal_data.get('review_period_days', 14)
        due_date = (required_date - timedelta(days=review_days)).strftime('%Y-%m-%d')
        
        submittal_data.update({
            "submittal_id": submittal_id,
            "submittal_number": submittal_number,
            "status": SubmittalStatus.NOT_SUBMITTED,
            "due_date": due_date,
            "reviews": [],
            "current_revision": "0",
            "total_revisions": 0,
            "documents": [],
            "days_in_review": 0,
            "is_overdue": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        submittal_data["submittal_type"] = SubmittalType(submittal_data["submittal_type"])
        submittal_data["status"] = SubmittalStatus(submittal_data["status"])
        
        submittal = Submittal(**submittal_data)
        self.submittals[submittal_id] = submittal
        self.next_submittal_number += 1
        
        return submittal_id
    
    def get_submittal(self, submittal_id: str) -> Optional[Submittal]:
        """Get a specific submittal"""
        return self.submittals.get(submittal_id)
    
    def get_all_submittals(self) -> List[Submittal]:
        """Get all submittals sorted by date (newest first)"""
        submittals = list(self.submittals.values())
        
        # Update calculated fields
        for submittal in submittals:
            submittal.days_in_review = submittal.calculate_days_in_review()
            submittal.is_overdue = submittal.check_overdue_status()
        
        return sorted(submittals, key=lambda s: s.created_at, reverse=True)
    
    def update_submittal(self, submittal_id: str, updates: Dict[str, Any]) -> bool:
        """Update a submittal"""
        if submittal_id not in self.submittals:
            return False
        
        submittal = self.submittals[submittal_id]
        
        for key, value in updates.items():
            if hasattr(submittal, key):
                setattr(submittal, key, value)
        
        submittal.updated_at = datetime.now().isoformat()
        return True
    
    def add_review(self, submittal_id: str, review_data: Dict[str, Any]) -> bool:
        """Add a review to a submittal"""
        submittal = self.submittals.get(submittal_id)
        if not submittal:
            return False
        
        review_id = f"rev-{len(submittal.reviews) + 1:03d}"
        review_data.update({
            "review_id": review_id,
            "review_date": datetime.now().strftime('%Y-%m-%d')
        })
        
        # Convert enum
        review_data["action"] = ReviewAction(review_data["action"])
        
        review = SubmittalReview(**review_data)
        submittal.reviews.append(review)
        
        # Update submittal status based on review action
        if review.action == ReviewAction.NO_EXCEPTION_TAKEN:
            submittal.status = SubmittalStatus.APPROVED
            submittal.approved_date = review.review_date
        elif review.action == ReviewAction.MAKE_CORRECTIONS_NOTED:
            submittal.status = SubmittalStatus.APPROVED_WITH_COMMENTS
            submittal.approved_date = review.review_date
        elif review.action == ReviewAction.REVISE_AND_RESUBMIT:
            submittal.status = SubmittalStatus.REVISE_AND_RESUBMIT
        elif review.action == ReviewAction.REJECTED:
            submittal.status = SubmittalStatus.REJECTED
        
        submittal.updated_at = datetime.now().isoformat()
        return True
    
    def submit_submittal(self, submittal_id: str) -> bool:
        """Submit a submittal for review"""
        submittal = self.submittals.get(submittal_id)
        if not submittal:
            return False
        
        submittal.status = SubmittalStatus.SUBMITTED
        submittal.submitted_date = datetime.now().strftime('%Y-%m-%d')
        submittal.current_revision = str(int(submittal.current_revision) + 1)
        submittal.total_revisions += 1
        submittal.updated_at = datetime.now().isoformat()
        
        return True
    
    def get_submittals_by_status(self, status: SubmittalStatus) -> List[Submittal]:
        """Get submittals by status"""
        return [s for s in self.get_all_submittals() if s.status == status]
    
    def get_overdue_submittals(self) -> List[Submittal]:
        """Get all overdue submittals"""
        return [s for s in self.get_all_submittals() if s.is_overdue]
    
    def generate_submittal_metrics(self) -> Dict[str, Any]:
        """Generate submittal performance metrics"""
        submittals = list(self.submittals.values())
        
        if not submittals:
            return {}
        
        total_submittals = len(submittals)
        
        # Status counts
        status_counts = {}
        for status in SubmittalStatus:
            status_counts[status.value] = len([s for s in submittals if s.status == status])
        
        # Type counts
        type_counts = {}
        for sub_type in SubmittalType:
            type_counts[sub_type.value] = len([s for s in submittals if s.submittal_type == sub_type])
        
        # Review metrics
        reviewed_submittals = [s for s in submittals if s.reviews]
        avg_review_time = sum(len(s.reviews) * s.days_in_review for s in reviewed_submittals) / len(reviewed_submittals) if reviewed_submittals else 0
        
        # Approval rate
        approved_submittals = len([s for s in submittals if s.status in [SubmittalStatus.APPROVED, SubmittalStatus.APPROVED_WITH_COMMENTS]])
        approval_rate = (approved_submittals / total_submittals * 100) if total_submittals > 0 else 0
        
        # Overdue count
        overdue_count = len([s for s in submittals if s.is_overdue])
        
        return {
            "total_submittals": total_submittals,
            "status_breakdown": status_counts,
            "type_breakdown": type_counts,
            "average_review_time": round(avg_review_time, 1),
            "approval_rate": round(approval_rate, 1),
            "overdue_count": overdue_count,
            "pending_review": status_counts.get("Under Review", 0) + status_counts.get("Submitted", 0)
        }
    
    def validate_submittal_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate submittal data"""
        errors = []
        
        required_fields = ["title", "submittal_type", "spec_section", "contractor", 
                          "contact_person", "required_date", "review_period_days"]
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        if data.get("review_period_days", 0) <= 0:
            errors.append("Review period days must be greater than 0")
        
        return errors

# Global instance for use across the application
submittals_manager = SubmittalsManager()