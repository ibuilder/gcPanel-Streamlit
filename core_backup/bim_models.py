"""
Pure Python BIM Data Models for Highland Tower Development
Advanced BIM collaboration data structures using standard Python

Integrated from comprehensive BIM platform specifications
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from enum import Enum
import json

from .data_models import Project


class SystemType(Enum):
    STRUCTURAL = "structural"
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    FIRE_PROTECTION = "fire_protection"
    ARCHITECTURAL = "architectural"
    CIVIL = "civil"


class ElementStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    ISSUE = "issue"
    ON_HOLD = "on_hold"


class ClashType(Enum):
    HARD_CLASH = "hard_clash"
    SOFT_CLASH = "soft_clash"
    CLEARANCE_CLASH = "clearance_clash"
    WORKFLOW_CLASH = "workflow_clash"


class ClashStatus(Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    IGNORED = "ignored"
    REVIEWING = "reviewing"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class BIMElement:
    """BIM element data model for Highland Tower Development"""
    id: str
    project_id: str
    model_id: str
    name: str
    custom_id: Optional[str]
    system_type: SystemType
    sub_system_type: Optional[str]
    element_type: str  # Beam, Column, Duct, Pipe, etc.
    status: ElementStatus
    level: str
    zone: Optional[str]
    grid_location: Optional[str]
    geometry: Dict[str, Any]  # 3D coordinates and shape data
    properties: Dict[str, Any]  # Material properties, dimensions, etc.
    ifc_guid: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @property
    def display_name(self) -> str:
        """Generate display name for element"""
        return f"{self.element_type} {self.custom_id or self.name}"
    
    @property
    def location_description(self) -> str:
        """Generate location description"""
        parts = [self.level]
        if self.zone:
            parts.append(f"Zone {self.zone}")
        if self.grid_location:
            parts.append(f"Grid {self.grid_location}")
        return " - ".join(parts)


@dataclass
class BIMModel:
    """BIM model data structure"""
    id: str
    project_id: str
    name: str
    file_path: str
    file_type: str  # IFC, RVT, etc.
    system_type: SystemType
    version: str
    uploaded_by: str
    upload_date: datetime
    file_size: int
    elements_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Clash:
    """BIM clash detection result"""
    id: str
    project_id: str
    element_a_id: str
    element_b_id: str
    clash_type: ClashType
    status: ClashStatus
    priority: Priority
    distance: float  # Distance in mm
    location: Dict[str, float]  # 3D coordinates
    description: str
    resolution: Optional[str]
    detected_by: str
    created_by: str
    assigned_to: Optional[str]
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    
    @property
    def is_critical(self) -> bool:
        """Check if clash is critical"""
        return self.priority == Priority.CRITICAL or self.clash_type == ClashType.HARD_CLASH
    
    @property
    def days_open(self) -> int:
        """Calculate days since clash was detected"""
        if self.resolved_at:
            return (self.resolved_at - self.created_at).days
        return (datetime.now() - self.created_at).days


@dataclass
class WorkInPlaceItem:
    """Work in place tracking item"""
    id: str
    element_id: str
    work_type: str  # Installation, Inspection, Testing, etc.
    description: str
    status: ElementStatus
    assigned_to: str
    start_date: Optional[date]
    target_completion: Optional[date]
    actual_completion: Optional[date]
    progress_percentage: float = 0.0
    notes: List[str] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)  # Photo file paths
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class QualityInspection:
    """Quality inspection for BIM elements"""
    id: str
    element_id: str
    inspection_type: str
    inspector: str
    inspection_date: date
    status: str  # PASS, FAIL, CONDITIONAL
    deficiencies: List[Dict[str, Any]]
    photos: List[str]
    notes: str
    follow_up_required: bool = False
    follow_up_date: Optional[date] = None


@dataclass
class ProgressPhoto:
    """Progress photo with BIM element association"""
    id: str
    element_id: Optional[str]
    photo_path: str
    caption: str
    taken_by: str
    taken_date: datetime
    location: Optional[Dict[str, float]]
    tags: List[str] = field(default_factory=list)
    linked_clash_id: Optional[str] = None


# Highland Tower Development BIM Data
HIGHLAND_TOWER_BIM_ELEMENTS = [
    BIMElement(
        id="HTD-BIM-STR-001",
        project_id="HTD-2024-001",
        model_id="HTD-MODEL-STR",
        name="Main Structural Beam L12-A",
        custom_id="STR-BEAM-L12-A-001",
        system_type=SystemType.STRUCTURAL,
        sub_system_type="Steel Frame",
        element_type="W24x68 Beam",
        status=ElementStatus.IN_PROGRESS,
        level="Level 12",
        zone="A",
        grid_location="A-B/12-13",
        geometry={
            "start_point": {"x": 0, "y": 0, "z": 36000},
            "end_point": {"x": 9000, "y": 0, "z": 36000},
            "width": 600,
            "height": 610,
            "length": 9000
        },
        properties={
            "material": "A992 Grade 50 Steel",
            "weight_per_foot": "68 lbs/ft",
            "moment_capacity": "723 ft-kips",
            "shear_capacity": "184 kips",
            "deflection_limit": "L/360"
        }
    ),
    BIMElement(
        id="HTD-BIM-MEP-001",
        project_id="HTD-2024-001",
        model_id="HTD-MODEL-MEP",
        name="HVAC Supply Duct L12-North",
        custom_id="HVAC-DUCT-L12-N-001",
        system_type=SystemType.MECHANICAL,
        sub_system_type="HVAC Supply",
        element_type="Rectangular Duct",
        status=ElementStatus.NOT_STARTED,
        level="Level 12",
        zone="North",
        grid_location="A-B/10-12",
        geometry={
            "start_point": {"x": 1000, "y": 500, "z": 35500},
            "end_point": {"x": 8000, "y": 500, "z": 35500},
            "width": 600,
            "height": 400,
            "length": 7000
        },
        properties={
            "material": "Galvanized Steel",
            "insulation": "2 inch fiberglass",
            "airflow_cfm": "2400",
            "static_pressure": "1.5 in. w.g.",
            "fire_rating": "1 hour"
        }
    ),
    BIMElement(
        id="HTD-BIM-ELE-001",
        project_id="HTD-2024-001",
        model_id="HTD-MODEL-ELE",
        name="Electrical Conduit Run L12-Power",
        custom_id="ELE-CONDUIT-L12-P-001",
        system_type=SystemType.ELECTRICAL,
        sub_system_type="Power Distribution",
        element_type="EMT Conduit",
        status=ElementStatus.COMPLETE,
        level="Level 12",
        zone="Central",
        grid_location="B-C/11-12",
        geometry={
            "start_point": {"x": 3000, "y": 300, "z": 35200},
            "end_point": {"x": 6000, "y": 300, "z": 35200},
            "diameter": 76,  # 3 inch EMT
            "length": 3000
        },
        properties={
            "material": "Electrical Metallic Tubing",
            "size": "3 inch",
            "conductor_count": "3 - #8 THWN",
            "voltage": "480V",
            "ampacity": "50A"
        }
    )
]

HIGHLAND_TOWER_BIM_CLASHES = [
    Clash(
        id="HTD-CLASH-001",
        project_id="HTD-2024-001",
        element_a_id="HTD-BIM-STR-001",
        element_b_id="HTD-BIM-MEP-001",
        clash_type=ClashType.HARD_CLASH,
        status=ClashStatus.ACTIVE,
        priority=Priority.HIGH,
        distance=0.0,  # Hard clash - 0 clearance
        location={"x": 4500, "y": 500, "z": 36000},
        description="Structural beam conflicts with HVAC duct routing at Grid A-B intersection",
        resolution=None,
        detected_by="BIM Coordinator",
        created_by="Highland BIM Team",
        assigned_to="MEP Engineer"
    ),
    Clash(
        id="HTD-CLASH-002",
        project_id="HTD-2024-001",
        element_a_id="HTD-BIM-ELE-001",
        element_b_id="HTD-BIM-MEP-001",
        clash_type=ClashType.SOFT_CLASH,
        status=ClashStatus.REVIEWING,
        priority=Priority.MEDIUM,
        distance=50.0,  # 50mm clearance - too close
        location={"x": 5000, "y": 400, "z": 35350},
        description="Electrical conduit and HVAC duct have insufficient clearance for maintenance access",
        resolution="Relocate conduit 200mm to the south",
        detected_by="BIM Coordinator",
        created_by="Highland BIM Team",
        assigned_to="Electrical Engineer"
    )
]

HIGHLAND_TOWER_WORK_IN_PLACE = [
    WorkInPlaceItem(
        id="HTD-WIP-001",
        element_id="HTD-BIM-STR-001",
        work_type="Steel Installation",
        description="Install W24x68 beam at Grid A-B, Level 12",
        status=ElementStatus.IN_PROGRESS,
        assigned_to="Highland Steel Crew",
        start_date=date(2025, 5, 20),
        target_completion=date(2025, 5, 28),
        actual_completion=None,
        progress_percentage=65.0,
        notes=[
            "Beam delivered to site on 5/20",
            "Crane operations scheduled for 5/26",
            "Connection details verified with engineer"
        ]
    ),
    WorkInPlaceItem(
        id="HTD-WIP-002",
        element_id="HTD-BIM-ELE-001",
        work_type="Electrical Installation",
        description="Install 3-inch EMT conduit run for power distribution",
        status=ElementStatus.COMPLETE,
        assigned_to="Elite Electrical Team",
        start_date=date(2025, 5, 15),
        target_completion=date(2025, 5, 18),
        actual_completion=date(2025, 5, 17),
        progress_percentage=100.0,
        notes=[
            "Conduit installation completed ahead of schedule",
            "All connections tested and verified",
            "Ready for wire pulling phase"
        ]
    )
]