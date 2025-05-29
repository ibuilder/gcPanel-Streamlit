"""
Pure Python Data Models for Highland Tower Development
Enterprise Construction Management Platform

Core data structures using standard Python classes for maximum longevity
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from enum import Enum


class ProjectStatus(Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"


class RFIStatus(Enum):
    OPEN = "open"
    IN_REVIEW = "in_review"
    ANSWERED = "answered"
    CLOSED = "closed"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Discipline(Enum):
    STRUCTURAL = "structural"
    MEP = "mep"
    ARCHITECTURAL = "architectural"
    ELECTRICAL = "electrical"
    MECHANICAL = "mechanical"
    PLUMBING = "plumbing"
    FIRE_SAFETY = "fire_safety"
    CIVIL = "civil"
    GEOTECHNICAL = "geotechnical"


@dataclass
class Project:
    """Core project data model"""
    id: str
    name: str
    value: float
    status: ProjectStatus
    start_date: date
    end_date: date
    residential_units: int = 0
    retail_units: int = 0
    floors_above: int = 0
    floors_below: int = 0
    progress_percent: float = 0.0
    budget_remaining: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class RFI:
    """Request for Information data model"""
    id: str
    number: str
    subject: str
    description: str
    location: str
    discipline: Discipline
    priority: Priority
    status: RFIStatus
    submitted_by: str
    assigned_to: str
    submitted_date: date
    due_date: date
    cost_impact: str
    schedule_impact: str
    project_id: str
    attachments: List[str] = field(default_factory=list)
    responses: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @property
    def days_open(self) -> int:
        """Calculate days since RFI was submitted"""
        return (date.today() - self.submitted_date).days
    
    @property
    def is_overdue(self) -> bool:
        """Check if RFI is past due date"""
        return date.today() > self.due_date and self.status not in [RFIStatus.ANSWERED, RFIStatus.CLOSED]


@dataclass
class Subcontractor:
    """Subcontractor data model"""
    id: str
    company_name: str
    contact_person: str
    email: str
    phone: str
    license_number: str
    insurance_expiry: date
    specialties: List[str]
    performance_rating: float = 0.0
    active_projects: int = 0
    total_contract_value: float = 0.0
    safety_record: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DailyReport:
    """Daily construction report data model"""
    id: str
    date: date
    weather: str
    temperature_high: int
    temperature_low: int
    crew_count: int
    hours_worked: float
    work_performed: List[str]
    materials_delivered: List[Dict[str, Any]]
    safety_incidents: List[Dict[str, Any]]
    quality_issues: List[str]
    delays_encountered: List[str]
    project_id: str
    submitted_by: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Inspection:
    """Quality inspection data model"""
    id: str
    inspection_type: str
    location: str
    inspector: str
    date_scheduled: date
    date_completed: Optional[date]
    status: str
    checklist_items: List[Dict[str, Any]]
    deficiencies: List[Dict[str, Any]]
    photos: List[str]
    overall_rating: str
    project_id: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Issue:
    """Project issue/risk data model"""
    id: str
    title: str
    description: str
    category: str
    severity: Priority
    probability: str
    impact: str
    mitigation_plan: str
    assigned_to: str
    status: str
    due_date: date
    project_id: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Document:
    """Document management data model"""
    id: str
    title: str
    filename: str
    file_path: str
    document_type: str
    category: str
    version: str
    uploaded_by: str
    upload_date: datetime
    file_size: int
    tags: List[str]
    project_id: str
    is_confidential: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class User:
    """User data model"""
    id: str
    username: str
    email: str
    role: str
    full_name: str
    phone: Optional[str] = None
    department: Optional[str] = None
    permissions: List[str] = field(default_factory=list)
    active: bool = True
    last_login: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)


# Highland Tower Development Project Instance
HIGHLAND_TOWER_PROJECT = Project(
    id="HTD-2024-001",
    name="Highland Tower Development",
    value=45500000.0,
    status=ProjectStatus.ACTIVE,
    start_date=date(2024, 1, 15),
    end_date=date(2025, 12, 31),
    residential_units=120,
    retail_units=8,
    floors_above=15,
    floors_below=2,
    progress_percent=67.3,
    budget_remaining=15600000.0
)