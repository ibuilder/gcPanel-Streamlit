"""
Highland Tower Development - Document Management Backend
Enterprise-grade document management with version control and collaboration.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class DocumentStatus(Enum):
    DRAFT = "Draft"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    SUPERSEDED = "Superseded"
    ARCHIVED = "Archived"

class DocumentCategory(Enum):
    DRAWINGS = "Drawings & Plans"
    SPECIFICATIONS = "Specifications"
    CONTRACTS = "Contracts"
    PERMITS = "Permits & Approvals"
    REPORTS = "Reports"
    CORRESPONDENCE = "Correspondence"
    PHOTOS = "Photos & Images"
    SUBMITTALS = "Submittals"
    RFIS = "RFIs"
    CHANGE_ORDERS = "Change Orders"

class AccessLevel(Enum):
    PUBLIC = "Public"
    PROJECT_TEAM = "Project Team"
    MANAGEMENT = "Management Only"
    CONFIDENTIAL = "Confidential"

@dataclass
class DocumentVersion:
    """Document version history record"""
    version_id: str
    version_number: str
    upload_date: str
    uploaded_by: str
    file_size: int
    changes_description: str
    review_status: str

@dataclass
class DocumentReview:
    """Document review record"""
    review_id: str
    reviewer_name: str
    review_date: str
    status: str  # "Approved", "Rejected", "Needs Changes"
    comments: str
    markup_file: Optional[str]

@dataclass
class Document:
    """Complete document record"""
    document_id: str
    document_number: str
    title: str
    description: str
    category: DocumentCategory
    status: DocumentStatus
    
    # File information
    filename: str
    file_type: str
    file_size: int
    file_path: str
    
    # Project details
    project_name: str
    discipline: str
    work_package: str
    drawing_number: Optional[str]
    
    # Version control
    current_version: str
    version_history: List[DocumentVersion]
    
    # Access and security
    access_level: AccessLevel
    password_protected: bool
    
    # Review and approval
    requires_approval: bool
    reviews: List[DocumentReview]
    approved_by: Optional[str]
    approval_date: Optional[str]
    
    # Metadata
    keywords: List[str]
    related_documents: List[str]
    supersedes: Optional[str]
    superseded_by: Optional[str]
    
    # Dates
    created_date: str
    modified_date: str
    expiry_date: Optional[str]
    
    # Workflow
    created_by: str
    last_modified_by: str
    checked_out_by: Optional[str]
    checkout_date: Optional[str]
    
    # Notes and tracking
    notes: str
    review_comments: str
    distribution_list: List[str]
    
    def is_checked_out(self) -> bool:
        """Check if document is currently checked out"""
        return self.checked_out_by is not None
    
    def is_expired(self) -> bool:
        """Check if document has expired"""
        if self.expiry_date:
            return datetime.strptime(self.expiry_date, '%Y-%m-%d').date() < date.today()
        return False
    
    def needs_review(self) -> bool:
        """Check if document needs review"""
        return self.requires_approval and self.status == DocumentStatus.UNDER_REVIEW

class DocumentManager:
    """Enterprise document management system"""
    
    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.next_document_number = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample document data"""
        
        # Sample document 1 - Architectural Drawing
        sample_document_1 = Document(
            document_id="doc-001",
            document_number="HTD-DOC-001",
            title="Level 15 Floor Plan - Penthouse Layout",
            description="Architectural floor plan for penthouse level including unit layouts and common areas",
            category=DocumentCategory.DRAWINGS,
            status=DocumentStatus.APPROVED,
            filename="HTD-A-L15-FloorPlan-Rev3.pdf",
            file_type="PDF",
            file_size=8450000,  # 8.45 MB
            file_path="/project/drawings/architectural/",
            project_name="Highland Tower Development",
            discipline="Architecture",
            work_package="Architectural Plans",
            drawing_number="A-301",
            current_version="Rev 3",
            version_history=[
                DocumentVersion(
                    version_id="ver-001",
                    version_number="Rev 1",
                    upload_date="2025-03-15",
                    uploaded_by="Sarah Johnson - Architect",
                    file_size=7200000,
                    changes_description="Initial design submission",
                    review_status="Superseded"
                ),
                DocumentVersion(
                    version_id="ver-002",
                    version_number="Rev 2",
                    upload_date="2025-04-20",
                    uploaded_by="Sarah Johnson - Architect",
                    file_size=7800000,
                    changes_description="Updated per client feedback - enlarged master bedroom",
                    review_status="Superseded"
                ),
                DocumentVersion(
                    version_id="ver-003",
                    version_number="Rev 3",
                    upload_date="2025-05-10",
                    uploaded_by="Sarah Johnson - Architect",
                    file_size=8450000,
                    changes_description="Final revisions - MEP coordination updates",
                    review_status="Current"
                )
            ],
            access_level=AccessLevel.PROJECT_TEAM,
            password_protected=False,
            requires_approval=True,
            reviews=[
                DocumentReview(
                    review_id="rev-001",
                    reviewer_name="John Smith - Project Manager",
                    review_date="2025-05-12",
                    status="Approved",
                    comments="Looks good, ready for construction",
                    markup_file=None
                ),
                DocumentReview(
                    review_id="rev-002",
                    reviewer_name="Michael Chen - Structural Engineer",
                    review_date="2025-05-11",
                    status="Approved",
                    comments="No structural conflicts, approved",
                    markup_file=None
                )
            ],
            approved_by="John Smith - Project Manager",
            approval_date="2025-05-12",
            keywords=["floor plan", "penthouse", "level 15", "residential"],
            related_documents=["doc-002", "doc-003"],
            supersedes="HTD-DOC-001-Rev2",
            superseded_by=None,
            created_date="2025-03-15",
            modified_date="2025-05-10",
            expiry_date=None,
            created_by="Sarah Johnson - Architect",
            last_modified_by="Sarah Johnson - Architect",
            checked_out_by=None,
            checkout_date=None,
            notes="Coordinated with MEP drawings and structural plans",
            review_comments="All discipline reviews completed successfully",
            distribution_list=["Project Team", "Highland Properties LLC", "City Planning Department"]
        )
        
        # Sample document 2 - Structural Specifications
        sample_document_2 = Document(
            document_id="doc-002",
            document_number="HTD-DOC-002",
            title="Structural Steel Specifications - High Strength Steel",
            description="Technical specifications for structural steel requirements including grades, welding procedures, and quality standards",
            category=DocumentCategory.SPECIFICATIONS,
            status=DocumentStatus.APPROVED,
            filename="HTD-S-SteelSpec-ASTM-A992.pdf",
            file_type="PDF",
            file_size=2100000,  # 2.1 MB
            file_path="/project/specifications/structural/",
            project_name="Highland Tower Development",
            discipline="Structural Engineering",
            work_package="Structural Steel",
            drawing_number=None,
            current_version="Rev 2",
            version_history=[
                DocumentVersion(
                    version_id="ver-004",
                    version_number="Rev 1",
                    upload_date="2025-02-28",
                    uploaded_by="Michael Chen - Structural Engineer",
                    file_size=1950000,
                    changes_description="Initial specification document",
                    review_status="Superseded"
                ),
                DocumentVersion(
                    version_id="ver-005",
                    version_number="Rev 2",
                    upload_date="2025-04-15",
                    uploaded_by="Michael Chen - Structural Engineer",
                    file_size=2100000,
                    changes_description="Updated welding procedures and inspection requirements",
                    review_status="Current"
                )
            ],
            access_level=AccessLevel.PROJECT_TEAM,
            password_protected=False,
            requires_approval=True,
            reviews=[
                DocumentReview(
                    review_id="rev-003",
                    reviewer_name="Steel Fabricators Inc. - QA Manager",
                    review_date="2025-04-18",
                    status="Approved",
                    comments="Specifications are clear and achievable",
                    markup_file=None
                )
            ],
            approved_by="John Smith - Project Manager",
            approval_date="2025-04-20",
            keywords=["steel", "specifications", "ASTM A992", "welding", "structural"],
            related_documents=["doc-001", "doc-004"],
            supersedes="HTD-DOC-002-Rev1",
            superseded_by=None,
            created_date="2025-02-28",
            modified_date="2025-04-15",
            expiry_date=None,
            created_by="Michael Chen - Structural Engineer",
            last_modified_by="Michael Chen - Structural Engineer",
            checked_out_by=None,
            checkout_date=None,
            notes="Coordinated with steel fabricator and meets all code requirements",
            review_comments="Fabricator review completed, no issues identified",
            distribution_list=["Project Team", "Steel Fabricators Inc.", "Building Department"]
        )
        
        # Sample document 3 - Contract Document (Under Review)
        sample_document_3 = Document(
            document_id="doc-003",
            document_number="HTD-DOC-003",
            title="MEP Subcontractor Agreement - HVAC Systems",
            description="Subcontractor agreement for HVAC system installation including scope, schedule, and payment terms",
            category=DocumentCategory.CONTRACTS,
            status=DocumentStatus.UNDER_REVIEW,
            filename="HTD-Contract-HVAC-Systems-LLC.pdf",
            file_type="PDF",
            file_size=3200000,  # 3.2 MB
            file_path="/project/contracts/subcontractors/",
            project_name="Highland Tower Development",
            discipline="Contracts & Legal",
            work_package="MEP Contracts",
            drawing_number=None,
            current_version="Rev 1",
            version_history=[
                DocumentVersion(
                    version_id="ver-006",
                    version_number="Rev 1",
                    upload_date="2025-05-25",
                    uploaded_by="Tom Brown - Contract Manager",
                    file_size=3200000,
                    changes_description="Initial contract draft for review",
                    review_status="Under Review"
                )
            ],
            access_level=AccessLevel.MANAGEMENT,
            password_protected=True,
            requires_approval=True,
            reviews=[
                DocumentReview(
                    review_id="rev-004",
                    reviewer_name="Legal Department",
                    review_date="2025-05-27",
                    status="Needs Changes",
                    comments="Minor revisions needed in payment terms section",
                    markup_file="HTD-Contract-HVAC-Legal-Markup.pdf"
                )
            ],
            approved_by=None,
            approval_date=None,
            keywords=["contract", "HVAC", "subcontractor", "MEP", "agreement"],
            related_documents=["doc-004", "doc-005"],
            supersedes=None,
            superseded_by=None,
            created_date="2025-05-25",
            modified_date="2025-05-25",
            expiry_date="2025-06-25",  # Contract offer expires
            created_by="Tom Brown - Contract Manager",
            last_modified_by="Tom Brown - Contract Manager",
            checked_out_by="Legal Department",
            checkout_date="2025-05-27",
            notes="Awaiting legal review completion, minor revisions expected",
            review_comments="Legal review in progress, payment terms need adjustment",
            distribution_list=["Management Team", "Legal Department", "HVAC Systems LLC"]
        )
        
        self.documents[sample_document_1.document_id] = sample_document_1
        self.documents[sample_document_2.document_id] = sample_document_2
        self.documents[sample_document_3.document_id] = sample_document_3
        self.next_document_number = 4
    
    def create_document(self, document_data: Dict[str, Any]) -> str:
        """Create a new document record"""
        document_id = f"doc-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        document_number = f"HTD-DOC-{self.next_document_number:03d}"
        
        document_data.update({
            "document_id": document_id,
            "document_number": document_number,
            "status": DocumentStatus.DRAFT,
            "current_version": "Rev 1",
            "version_history": [
                DocumentVersion(
                    version_id=f"ver-{self.next_document_number:03d}",
                    version_number="Rev 1",
                    upload_date=datetime.now().strftime('%Y-%m-%d'),
                    uploaded_by=document_data.get("created_by", "Current User"),
                    file_size=document_data.get("file_size", 0),
                    changes_description="Initial document creation",
                    review_status="Current"
                )
            ],
            "reviews": [],
            "approved_by": None,
            "approval_date": None,
            "supersedes": None,
            "superseded_by": None,
            "checked_out_by": None,
            "checkout_date": None,
            "created_date": datetime.now().strftime('%Y-%m-%d'),
            "modified_date": datetime.now().strftime('%Y-%m-%d')
        })
        
        # Convert enums
        document_data["category"] = DocumentCategory(document_data["category"])
        document_data["status"] = DocumentStatus(document_data["status"])
        document_data["access_level"] = AccessLevel(document_data["access_level"])
        
        document = Document(**document_data)
        self.documents[document_id] = document
        self.next_document_number += 1
        
        return document_id
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """Get a specific document"""
        return self.documents.get(document_id)
    
    def get_all_documents(self) -> List[Document]:
        """Get all documents sorted by modified date (newest first)"""
        return sorted(self.documents.values(),
                     key=lambda d: d.modified_date, reverse=True)
    
    def get_documents_by_status(self, status: DocumentStatus) -> List[Document]:
        """Get documents by status"""
        return [doc for doc in self.documents.values() if doc.status == status]
    
    def get_documents_by_category(self, category: DocumentCategory) -> List[Document]:
        """Get documents by category"""
        return [doc for doc in self.documents.values() if doc.category == category]
    
    def get_documents_needing_review(self) -> List[Document]:
        """Get documents that need review"""
        return [doc for doc in self.documents.values() if doc.needs_review()]
    
    def get_expired_documents(self) -> List[Document]:
        """Get documents that have expired"""
        return [doc for doc in self.documents.values() if doc.is_expired()]
    
    def checkout_document(self, document_id: str, user: str) -> bool:
        """Check out a document for editing"""
        document = self.documents.get(document_id)
        if not document or document.is_checked_out():
            return False
        
        document.checked_out_by = user
        document.checkout_date = datetime.now().strftime('%Y-%m-%d')
        return True
    
    def checkin_document(self, document_id: str) -> bool:
        """Check in a document after editing"""
        document = self.documents.get(document_id)
        if not document:
            return False
        
        document.checked_out_by = None
        document.checkout_date = None
        document.modified_date = datetime.now().strftime('%Y-%m-%d')
        return True
    
    def add_review(self, document_id: str, review_data: Dict[str, Any]) -> bool:
        """Add a review to a document"""
        document = self.documents.get(document_id)
        if not document:
            return False
        
        review_id = f"rev-{len(document.reviews) + 1:03d}"
        review_data.update({"review_id": review_id})
        
        review = DocumentReview(**review_data)
        document.reviews.append(review)
        
        # Update status based on reviews
        if review.status == "Approved":
            all_approved = all(r.status == "Approved" for r in document.reviews)
            if all_approved and document.requires_approval:
                document.status = DocumentStatus.APPROVED
                document.approved_by = review.reviewer_name
                document.approval_date = review.review_date
        
        return True
    
    def search_documents(self, query: str) -> List[Document]:
        """Search documents by title, description, or keywords"""
        query_lower = query.lower()
        results = []
        
        for document in self.documents.values():
            if (query_lower in document.title.lower() or 
                query_lower in document.description.lower() or
                any(query_lower in keyword.lower() for keyword in document.keywords)):
                results.append(document)
        
        return results
    
    def generate_document_metrics(self) -> Dict[str, Any]:
        """Generate document management metrics"""
        documents = list(self.documents.values())
        
        if not documents:
            return {}
        
        total_documents = len(documents)
        
        # Status counts
        status_counts = {}
        for status in DocumentStatus:
            status_counts[status.value] = len([d for d in documents if d.status == status])
        
        # Category counts
        category_counts = {}
        for category in DocumentCategory:
            category_counts[category.value] = len([d for d in documents if d.category == category])
        
        # File size metrics
        total_file_size = sum(d.file_size for d in documents)
        avg_file_size = total_file_size / len(documents) if documents else 0
        
        # Review metrics
        documents_needing_review = len(self.get_documents_needing_review())
        expired_documents = len(self.get_expired_documents())
        checked_out_documents = len([d for d in documents if d.is_checked_out()])
        
        # Version metrics
        total_versions = sum(len(d.version_history) for d in documents)
        
        return {
            "total_documents": total_documents,
            "status_breakdown": status_counts,
            "category_breakdown": category_counts,
            "total_file_size_mb": round(total_file_size / 1024 / 1024, 1),
            "average_file_size_mb": round(avg_file_size / 1024 / 1024, 1),
            "documents_needing_review": documents_needing_review,
            "expired_documents": expired_documents,
            "checked_out_documents": checked_out_documents,
            "total_versions": total_versions,
            "approved_documents": status_counts.get("Approved", 0),
            "draft_documents": status_counts.get("Draft", 0)
        }

# Global instance for use across the application
document_manager = DocumentManager()