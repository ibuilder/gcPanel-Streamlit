"""
Highland Tower Development - Project Closeout Backend
Enterprise-grade project completion, warranty tracking, and handover management.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class CloseoutStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    UNDER_REVIEW = "Under Review"
    COMPLETED = "Completed"
    APPROVED = "Approved"
    ARCHIVED = "Archived"

class DocumentType(Enum):
    WARRANTY = "Warranty Documentation"
    MANUAL = "Operation & Maintenance Manual"
    AS_BUILT = "As-Built Drawing"
    CERTIFICATE = "Certificate of Compliance"
    TEST_REPORT = "Test Report"
    TRAINING = "Training Documentation"
    INSPECTION = "Final Inspection Report"
    PERMIT = "Permit & Approval"

class PunchStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    VERIFIED = "Verified"
    CLOSED = "Closed"

@dataclass
class CloseoutDocument:
    """Project closeout document"""
    document_id: str
    document_code: str
    title: str
    document_type: DocumentType
    
    # Content information
    description: str
    discipline: str
    trade: str
    system: str
    
    # File information
    file_name: str
    file_path: str
    file_size: int
    file_format: str
    
    # Status and workflow
    status: CloseoutStatus
    required: bool
    priority: str  # "Critical", "High", "Medium", "Low"
    
    # Responsibility
    responsible_party: str
    submitted_by: str
    reviewed_by: Optional[str]
    approved_by: Optional[str]
    
    # Dates
    due_date: str
    submitted_date: Optional[str]
    review_date: Optional[str]
    approval_date: Optional[str]
    
    # Warranty information
    warranty_period: Optional[str]
    warranty_start_date: Optional[str]
    warranty_end_date: Optional[str]
    
    # Notes and comments
    submission_notes: str
    review_comments: str
    rejection_reason: str
    
    # Workflow tracking
    created_at: str
    updated_at: str

@dataclass
class PunchListItem:
    """Punch list deficiency item"""
    punch_id: str
    punch_code: str
    title: str
    description: str
    
    # Location and classification
    location: str
    level: str
    room: str
    discipline: str
    trade: str
    
    # Severity and priority
    severity: str  # "Critical", "Major", "Minor", "Cosmetic"
    priority: int
    
    # Status and responsibility
    status: PunchStatus
    assigned_to: str
    identified_by: str
    
    # Resolution tracking
    estimated_hours: float
    actual_hours: float
    estimated_cost: float
    actual_cost: float
    
    # Dates
    identified_date: str
    due_date: str
    completed_date: Optional[str]
    verified_date: Optional[str]
    closed_date: Optional[str]
    
    # Documentation
    photos_before: List[str]
    photos_after: List[str]
    work_description: str
    completion_notes: str
    
    # Quality control
    inspector: Optional[str]
    inspection_date: Optional[str]
    inspection_passed: bool
    
    # Workflow tracking
    created_at: str
    updated_at: str

@dataclass
class SystemCommissioning:
    """Building system commissioning record"""
    commissioning_id: str
    system_name: str
    system_type: str  # "HVAC", "Electrical", "Plumbing", "Fire Safety", "Security"
    
    # Scope and description
    description: str
    equipment_list: List[str]
    performance_criteria: List[str]
    
    # Testing and verification
    test_procedures: List[str]
    test_results: Dict[str, Any]
    performance_verified: bool
    
    # Status and responsibility
    status: CloseoutStatus
    commissioning_agent: str
    contractor: str
    
    # Dates
    start_date: str
    completion_date: Optional[str]
    acceptance_date: Optional[str]
    
    # Documentation
    test_reports: List[str]
    certificates: List[str]
    training_completed: bool
    training_date: Optional[str]
    
    # Warranty and maintenance
    warranty_period: str
    maintenance_requirements: List[str]
    preventive_schedule: str
    
    # Notes
    commissioning_notes: str
    deficiencies: List[str]
    
    # Workflow tracking
    created_at: str
    updated_at: str

class CloseoutManager:
    """Enterprise project closeout management system"""
    
    def __init__(self):
        self.documents: Dict[str, CloseoutDocument] = {}
        self.punch_items: Dict[str, PunchListItem] = {}
        self.commissioning: Dict[str, SystemCommissioning] = {}
        self.next_document_code = 1
        self.next_punch_code = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample closeout data"""
        
        # Sample Closeout Documents
        sample_documents = [
            CloseoutDocument(
                document_id="doc-001",
                document_code="HTD-DOC-001",
                title="HVAC System Operation & Maintenance Manual",
                document_type=DocumentType.MANUAL,
                description="Complete O&M manual for HVAC systems including VAV boxes, chillers, and controls",
                discipline="Mechanical",
                trade="HVAC Systems LLC",
                system="HVAC - Primary Systems",
                file_name="HTD_HVAC_OM_Manual_v2.1.pdf",
                file_path="/closeout/documents/manuals/HTD_HVAC_OM_Manual_v2.1.pdf",
                file_size=45000000,  # 45 MB
                file_format="PDF",
                status=CloseoutStatus.COMPLETED,
                required=True,
                priority="Critical",
                responsible_party="HVAC Systems LLC",
                submitted_by="Lisa Park - Mechanical Engineer",
                reviewed_by="Tom Brown - MEP Manager",
                approved_by="John Smith - Project Manager",
                due_date="2025-06-15",
                submitted_date="2025-05-25",
                review_date="2025-05-27",
                approval_date="2025-05-28",
                warranty_period="24 months",
                warranty_start_date="2025-06-01",
                warranty_end_date="2027-06-01",
                submission_notes="Complete manual with all equipment specifications and maintenance schedules",
                review_comments="Excellent documentation. All requirements met.",
                rejection_reason="",
                created_at="2025-05-20 09:00:00",
                updated_at="2025-05-28 14:30:00"
            ),
            CloseoutDocument(
                document_id="doc-002",
                document_code="HTD-DOC-002",
                title="Structural Steel As-Built Drawings",
                document_type=DocumentType.AS_BUILT,
                description="Final as-built drawings for structural steel frame with all field modifications",
                discipline="Structural",
                trade="Steel Fabricators Inc.",
                system="Structural Frame",
                file_name="HTD_Structural_AsBuilt_Rev_Final.dwg",
                file_path="/closeout/documents/asbuilts/HTD_Structural_AsBuilt_Rev_Final.dwg",
                file_size=125000000,  # 125 MB
                file_format="DWG",
                status=CloseoutStatus.UNDER_REVIEW,
                required=True,
                priority="High",
                responsible_party="Steel Fabricators Inc.",
                submitted_by="Mike Rodriguez - Structural Engineer",
                reviewed_by="John Smith - Project Manager",
                approved_by=None,
                due_date="2025-06-10",
                submitted_date="2025-05-26",
                review_date="2025-05-28",
                approval_date=None,
                warranty_period="12 months",
                warranty_start_date="2025-06-01",
                warranty_end_date="2026-06-01",
                submission_notes="As-built drawings reflect all field changes and RFI resolutions",
                review_comments="Minor revisions needed for connection details on Level 12-15",
                rejection_reason="",
                created_at="2025-05-18 10:00:00",
                updated_at="2025-05-28 16:15:00"
            ),
            CloseoutDocument(
                document_id="doc-003",
                document_code="HTD-DOC-003",
                title="Electrical Panel Schedules and Test Reports",
                document_type=DocumentType.TEST_REPORT,
                description="Electrical testing reports and final panel schedules for all electrical systems",
                discipline="Electrical",
                trade="Power Systems Inc.",
                system="Electrical Distribution",
                file_name="HTD_Electrical_Testing_Final.pdf",
                file_path="/closeout/documents/testing/HTD_Electrical_Testing_Final.pdf",
                file_size=28000000,  # 28 MB
                file_format="PDF",
                status=CloseoutStatus.IN_PROGRESS,
                required=True,
                priority="Critical",
                responsible_party="Power Systems Inc.",
                submitted_by="Mark Johnson - Electrical Engineer",
                reviewed_by=None,
                approved_by=None,
                due_date="2025-06-20",
                submitted_date=None,
                review_date=None,
                approval_date=None,
                warranty_period="36 months",
                warranty_start_date="2025-07-01",
                warranty_end_date="2028-07-01",
                submission_notes="",
                review_comments="",
                rejection_reason="",
                created_at="2025-05-15 11:00:00",
                updated_at="2025-05-28 09:45:00"
            )
        ]
        
        for doc in sample_documents:
            self.documents[doc.document_id] = doc
        
        # Sample Punch List Items
        sample_punch_items = [
            PunchListItem(
                punch_id="punch-001",
                punch_code="HTD-PUNCH-001",
                title="Incomplete Paint Touch-up in Lobby",
                description="Paint touch-up required on column covers in main lobby area - visible scuff marks",
                location="Level 1 - Main Lobby",
                level="Level 1",
                room="Lobby",
                discipline="Architectural",
                trade="Interior Finishes Co.",
                severity="Minor",
                priority=3,
                status=PunchStatus.IN_PROGRESS,
                assigned_to="Interior Finishes Co.",
                identified_by="Sarah Wilson - Quality Control",
                estimated_hours=4.0,
                actual_hours=0.0,
                estimated_cost=250.0,
                actual_cost=0.0,
                identified_date="2025-05-25",
                due_date="2025-06-05",
                completed_date=None,
                verified_date=None,
                closed_date=None,
                photos_before=["/punch/photos/HTD-PUNCH-001-before.jpg"],
                photos_after=[],
                work_description="Touch-up paint on column covers and wall surfaces in lobby",
                completion_notes="",
                inspector=None,
                inspection_date=None,
                inspection_passed=False,
                created_at="2025-05-25 14:30:00",
                updated_at="2025-05-27 10:15:00"
            ),
            PunchListItem(
                punch_id="punch-002",
                punch_code="HTD-PUNCH-002",
                title="HVAC Vent Damper Not Operating",
                description="VAV box damper in office space not responding to controls - remains fully open",
                location="Level 12 - Office Suite 1205",
                level="Level 12",
                room="Office Suite 1205",
                discipline="Mechanical",
                trade="HVAC Systems LLC",
                severity="Major",
                priority=2,
                status=PunchStatus.COMPLETED,
                assigned_to="HVAC Systems LLC",
                identified_by="Tom Brown - MEP Manager",
                estimated_hours=6.0,
                actual_hours=5.5,
                estimated_cost=450.0,
                actual_cost=425.0,
                identified_date="2025-05-22",
                due_date="2025-05-30",
                completed_date="2025-05-28",
                verified_date=None,
                closed_date=None,
                photos_before=["/punch/photos/HTD-PUNCH-002-before.jpg"],
                photos_after=["/punch/photos/HTD-PUNCH-002-after.jpg"],
                work_description="Replaced faulty actuator and recalibrated VAV box controls",
                completion_notes="Damper now operating correctly, controls tested and verified",
                inspector="Tom Brown - MEP Manager",
                inspection_date="2025-05-28",
                inspection_passed=True,
                created_at="2025-05-22 11:45:00",
                updated_at="2025-05-28 15:20:00"
            ),
            PunchListItem(
                punch_id="punch-003",
                punch_code="HTD-PUNCH-003",
                title="Fire Alarm Strobe Light Misaligned",
                description="Fire alarm strobe light not properly aligned in corridor - visibility issue",
                location="Level 8 - Corridor East",
                level="Level 8",
                room="Corridor East",
                discipline="Fire Protection",
                trade="Safety Systems Inc.",
                severity="Critical",
                priority=1,
                status=PunchStatus.OPEN,
                assigned_to="Safety Systems Inc.",
                identified_by="Sarah Wilson - Safety Manager",
                estimated_hours=2.0,
                actual_hours=0.0,
                estimated_cost=150.0,
                actual_cost=0.0,
                identified_date="2025-05-28",
                due_date="2025-05-30",
                completed_date=None,
                verified_date=None,
                closed_date=None,
                photos_before=["/punch/photos/HTD-PUNCH-003-before.jpg"],
                photos_after=[],
                work_description="Realign strobe light for proper visibility coverage",
                completion_notes="",
                inspector=None,
                inspection_date=None,
                inspection_passed=False,
                created_at="2025-05-28 16:00:00",
                updated_at="2025-05-28 16:00:00"
            )
        ]
        
        for punch in sample_punch_items:
            self.punch_items[punch.punch_id] = punch
        
        # Sample System Commissioning
        sample_commissioning = SystemCommissioning(
            commissioning_id="comm-001",
            system_name="HVAC Primary Systems",
            system_type="HVAC",
            description="Complete commissioning of HVAC primary systems including chillers, boilers, and air handling units",
            equipment_list=["Chiller #1 (500 Ton)", "Chiller #2 (500 Ton)", "Boiler #1 (2000 MBH)", "AHU-1 through AHU-8"],
            performance_criteria=["Temperature control ±2°F", "Humidity control 45-55% RH", "Energy efficiency targets met"],
            test_procedures=["Functional performance testing", "Sequence of operations verification", "Energy performance testing"],
            test_results={"temperature_control": "±1.5°F achieved", "humidity_control": "48-52% RH achieved", "energy_efficiency": "105% of target"},
            performance_verified=True,
            status=CloseoutStatus.COMPLETED,
            commissioning_agent="Building Systems Commissioning LLC",
            contractor="HVAC Systems LLC",
            start_date="2025-05-01",
            completion_date="2025-05-25",
            acceptance_date="2025-05-28",
            test_reports=["/commissioning/HVAC_FPT_Report.pdf", "/commissioning/HVAC_SOO_Report.pdf"],
            certificates=["/commissioning/HVAC_Commissioning_Certificate.pdf"],
            training_completed=True,
            training_date="2025-05-27",
            warranty_period="24 months",
            maintenance_requirements=["Quarterly filter changes", "Semi-annual coil cleaning", "Annual belt inspection"],
            preventive_schedule="Quarterly inspections, annual comprehensive service",
            commissioning_notes="All systems performing above specifications. Energy efficiency exceeds targets.",
            deficiencies=[],
            created_at="2025-05-01 08:00:00",
            updated_at="2025-05-28 17:00:00"
        )
        
        self.commissioning[sample_commissioning.commissioning_id] = sample_commissioning
        self.next_document_code = 4
        self.next_punch_code = 4
    
    def create_closeout_document(self, doc_data: Dict[str, Any]) -> str:
        """Create a new closeout document"""
        document_id = f"doc-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        document_code = f"HTD-DOC-{self.next_document_code:03d}"
        
        doc_data.update({
            "document_id": document_id,
            "document_code": document_code,
            "submitted_date": None,
            "review_date": None,
            "approval_date": None,
            "reviewed_by": None,
            "approved_by": None,
            "submission_notes": "",
            "review_comments": "",
            "rejection_reason": "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        doc_data["document_type"] = DocumentType(doc_data["document_type"])
        doc_data["status"] = CloseoutStatus(doc_data["status"])
        
        document = CloseoutDocument(**doc_data)
        self.documents[document_id] = document
        self.next_document_code += 1
        
        return document_id
    
    def create_punch_item(self, punch_data: Dict[str, Any]) -> str:
        """Create a new punch list item"""
        punch_id = f"punch-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        punch_code = f"HTD-PUNCH-{self.next_punch_code:03d}"
        
        punch_data.update({
            "punch_id": punch_id,
            "punch_code": punch_code,
            "status": PunchStatus.OPEN,
            "completed_date": None,
            "verified_date": None,
            "closed_date": None,
            "actual_hours": 0.0,
            "actual_cost": 0.0,
            "photos_before": [],
            "photos_after": [],
            "completion_notes": "",
            "inspector": None,
            "inspection_date": None,
            "inspection_passed": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        punch_item = PunchListItem(**punch_data)
        self.punch_items[punch_id] = punch_item
        self.next_punch_code += 1
        
        return punch_id
    
    def get_closeout_document(self, document_id: str) -> Optional[CloseoutDocument]:
        """Get a specific closeout document"""
        return self.documents.get(document_id)
    
    def get_all_documents(self) -> List[CloseoutDocument]:
        """Get all closeout documents sorted by due date"""
        return sorted(self.documents.values(), key=lambda d: d.due_date)
    
    def get_documents_by_status(self, status: CloseoutStatus) -> List[CloseoutDocument]:
        """Get documents by status"""
        return [doc for doc in self.documents.values() if doc.status == status]
    
    def get_documents_by_type(self, doc_type: DocumentType) -> List[CloseoutDocument]:
        """Get documents by type"""
        return [doc for doc in self.documents.values() if doc.document_type == doc_type]
    
    def get_all_punch_items(self) -> List[PunchListItem]:
        """Get all punch list items sorted by priority and due date"""
        return sorted(self.punch_items.values(), key=lambda p: (p.priority, p.due_date))
    
    def get_punch_items_by_status(self, status: PunchStatus) -> List[PunchListItem]:
        """Get punch items by status"""
        return [punch for punch in self.punch_items.values() if punch.status == status]
    
    def get_open_punch_items(self) -> List[PunchListItem]:
        """Get open punch list items"""
        return [punch for punch in self.punch_items.values() if punch.status in [PunchStatus.OPEN, PunchStatus.IN_PROGRESS]]
    
    def complete_punch_item(self, punch_id: str, completion_notes: str, actual_hours: float, actual_cost: float) -> bool:
        """Mark a punch item as completed"""
        punch = self.punch_items.get(punch_id)
        if not punch:
            return False
        
        punch.status = PunchStatus.COMPLETED
        punch.completed_date = datetime.now().strftime('%Y-%m-%d')
        punch.completion_notes = completion_notes
        punch.actual_hours = actual_hours
        punch.actual_cost = actual_cost
        punch.updated_at = datetime.now().isoformat()
        
        return True
    
    def approve_document(self, document_id: str, approved_by: str) -> bool:
        """Approve a closeout document"""
        document = self.documents.get(document_id)
        if not document:
            return False
        
        document.status = CloseoutStatus.APPROVED
        document.approved_by = approved_by
        document.approval_date = datetime.now().strftime('%Y-%m-%d')
        document.updated_at = datetime.now().isoformat()
        
        return True
    
    def generate_closeout_metrics(self) -> Dict[str, Any]:
        """Generate project closeout metrics"""
        documents = list(self.documents.values())
        punch_items = list(self.punch_items.values())
        commissioning_items = list(self.commissioning.values())
        
        if not documents and not punch_items:
            return {}
        
        # Document metrics
        total_documents = len(documents)
        
        # Document status counts
        doc_status_counts = {}
        for status in CloseoutStatus:
            doc_status_counts[status.value] = len([d for d in documents if d.status == status])
        
        # Document type counts
        doc_type_counts = {}
        for doc_type in DocumentType:
            doc_type_counts[doc_type.value] = len([d for d in documents if d.document_type == doc_type])
        
        # Punch list metrics
        total_punch_items = len(punch_items)
        open_punch_items = len([p for p in punch_items if p.status in [PunchStatus.OPEN, PunchStatus.IN_PROGRESS]])
        completed_punch_items = len([p for p in punch_items if p.status == PunchStatus.COMPLETED])
        
        # Punch severity counts
        punch_severity_counts = {}
        severities = ["Critical", "Major", "Minor", "Cosmetic"]
        for severity in severities:
            punch_severity_counts[severity] = len([p for p in punch_items if p.severity == severity])
        
        # Commissioning metrics
        total_commissioning = len(commissioning_items)
        completed_commissioning = len([c for c in commissioning_items if c.status == CloseoutStatus.COMPLETED])
        
        # Calculate completion percentages
        doc_completion_rate = (doc_status_counts.get("Completed", 0) + doc_status_counts.get("Approved", 0)) / total_documents * 100 if total_documents > 0 else 0
        punch_completion_rate = completed_punch_items / total_punch_items * 100 if total_punch_items > 0 else 0
        commissioning_completion_rate = completed_commissioning / total_commissioning * 100 if total_commissioning > 0 else 0
        
        return {
            "total_documents": total_documents,
            "total_punch_items": total_punch_items,
            "open_punch_items": open_punch_items,
            "completed_punch_items": completed_punch_items,
            "total_commissioning": total_commissioning,
            "document_status_breakdown": doc_status_counts,
            "document_type_breakdown": doc_type_counts,
            "punch_severity_breakdown": punch_severity_counts,
            "document_completion_rate": round(doc_completion_rate, 1),
            "punch_completion_rate": round(punch_completion_rate, 1),
            "commissioning_completion_rate": round(commissioning_completion_rate, 1),
            "critical_punch_items": punch_severity_counts.get("Critical", 0),
            "overdue_documents": len([d for d in documents if d.due_date < datetime.now().strftime('%Y-%m-%d') and d.status not in [CloseoutStatus.COMPLETED, CloseoutStatus.APPROVED]])
        }

# Global instance for use across the application
closeout_manager = CloseoutManager()