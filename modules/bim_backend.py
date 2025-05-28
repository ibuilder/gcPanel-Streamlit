"""
Highland Tower Development - BIM Management Backend
Enterprise-grade Building Information Modeling with 3D coordination and clash detection.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ModelType(Enum):
    ARCHITECTURAL = "Architectural"
    STRUCTURAL = "Structural" 
    MECHANICAL = "Mechanical"
    ELECTRICAL = "Electrical"
    PLUMBING = "Plumbing"
    FIRE_PROTECTION = "Fire Protection"
    CIVIL = "Civil"
    LANDSCAPE = "Landscape"
    COMBINED = "Combined Model"

class ModelStatus(Enum):
    DRAFT = "Draft"
    IN_REVIEW = "In Review"
    APPROVED = "Approved"
    CURRENT = "Current"
    SUPERSEDED = "Superseded"
    ARCHIVED = "Archived"

class ClashSeverity(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATION = "Information"

class ClashStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    ACCEPTED = "Accepted"
    CLOSED = "Closed"

@dataclass
class BIMModel:
    """BIM model record"""
    model_id: str
    model_code: str
    model_name: str
    model_type: ModelType
    discipline: str
    
    # Version information
    version: str
    revision: str
    status: ModelStatus
    
    # File information
    file_name: str
    file_path: str
    file_size: int  # in bytes
    file_format: str  # "RVT", "IFC", "DWG", "NWD"
    
    # Project information
    project_phase: str
    level_range: str
    building_section: str
    
    # Metadata
    created_by: str
    reviewed_by: Optional[str]
    approved_by: Optional[str]
    
    # Dates
    created_date: str
    last_modified: str
    review_date: Optional[str]
    approval_date: Optional[str]
    
    # Coordination
    clash_detection_run: bool
    federated_model: bool
    coordinate_system: str
    
    # Notes and comments
    description: str
    review_comments: str
    change_log: List[str]
    
    # Workflow tracking
    workflow_stage: str
    next_milestone: str
    assigned_to: str

@dataclass
class ClashDetection:
    """Clash detection result"""
    clash_id: str
    clash_code: str
    clash_name: str
    
    # Models involved
    model_a: str
    model_b: str
    element_a: str
    element_b: str
    
    # Classification
    clash_type: str  # "Hard Clash", "Soft Clash", "Clearance"
    severity: ClashSeverity
    discipline_conflict: str
    
    # Location
    building_level: str
    zone: str
    coordinates: Dict[str, float]  # x, y, z
    
    # Status and resolution
    status: ClashStatus
    assigned_to: str
    priority: int
    
    # Resolution tracking
    resolution_method: str
    resolution_notes: str
    estimated_cost: float
    
    # Dates
    detected_date: str
    assigned_date: str
    resolved_date: Optional[str]
    target_resolution: str
    
    # Documentation
    screenshot_path: str
    markup_files: List[str]
    related_rfis: List[str]
    
    # Workflow
    created_by: str
    reviewed_by: Optional[str]
    approved_resolution: bool

@dataclass
class ModelCoordination:
    """Model coordination session"""
    session_id: str
    session_name: str
    coordination_type: str  # "Design Review", "Clash Resolution", "Progress Review"
    
    # Participants
    meeting_date: str
    attendees: List[str]
    disciplines: List[str]
    
    # Models reviewed
    models_reviewed: List[str]
    federated_model: str
    
    # Issues and decisions
    issues_discussed: List[str]
    decisions_made: List[str]
    action_items: List[Dict[str, str]]
    
    # Clash resolution
    clashes_reviewed: List[str]
    clashes_resolved: List[str]
    new_clashes_identified: List[str]
    
    # Documentation
    meeting_notes: str
    presentation_files: List[str]
    markup_files: List[str]
    
    # Follow-up
    next_meeting_date: str
    outstanding_actions: int
    
    # Workflow
    created_by: str
    created_at: str

class BIMManager:
    """Enterprise BIM management system"""
    
    def __init__(self):
        self.models: Dict[str, BIMModel] = {}
        self.clashes: Dict[str, ClashDetection] = {}
        self.coordination_sessions: Dict[str, ModelCoordination] = {}
        self.next_model_code = 1
        self.next_clash_code = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample BIM data"""
        
        # Sample BIM Models
        sample_models = [
            BIMModel(
                model_id="model-001",
                model_code="HTD-ARCH-001",
                model_name="Highland Tower - Architectural Base Model",
                model_type=ModelType.ARCHITECTURAL,
                discipline="Architecture",
                version="2.5",
                revision="Rev-15",
                status=ModelStatus.CURRENT,
                file_name="Highland_Tower_Architectural_Rev15.rvt",
                file_path="/bim/models/architectural/Highland_Tower_Architectural_Rev15.rvt",
                file_size=145000000,  # 145 MB
                file_format="RVT",
                project_phase="Design Development",
                level_range="Level B1 to Penthouse",
                building_section="Full Building",
                created_by="David Chen - Lead Architect",
                reviewed_by="John Smith - Project Manager",
                approved_by="Highland Properties LLC",
                created_date="2025-03-15",
                last_modified="2025-05-28",
                review_date="2025-05-27",
                approval_date="2025-05-28",
                clash_detection_run=True,
                federated_model=True,
                coordinate_system="Shared Site Coordinates",
                description="Complete architectural model including all levels, exterior envelope, and interior layouts",
                review_comments="Model approved with minor revisions to penthouse layout. Excellent detail level.",
                change_log=["Rev 15: Updated penthouse layouts per client feedback", "Rev 14: Added detailed millwork", "Rev 13: Revised exterior materials"],
                workflow_stage="Construction Documentation",
                next_milestone="100% CD Set - June 15, 2025",
                assigned_to="Architecture Team"
            ),
            BIMModel(
                model_id="model-002",
                model_code="HTD-STRUC-001",
                model_name="Highland Tower - Structural Steel Model",
                model_type=ModelType.STRUCTURAL,
                discipline="Structural Engineering",
                version="1.8",
                revision="Rev-12",
                status=ModelStatus.CURRENT,
                file_name="Highland_Tower_Structural_Rev12.rvt",
                file_path="/bim/models/structural/Highland_Tower_Structural_Rev12.rvt",
                file_size=89000000,  # 89 MB
                file_format="RVT",
                project_phase="Construction Documentation",
                level_range="Foundation to Roof",
                building_section="Full Structure",
                created_by="Mike Rodriguez - Structural Engineer",
                reviewed_by="Tom Brown - MEP Manager",
                approved_by="Structural Consultant",
                created_date="2025-03-20",
                last_modified="2025-05-26",
                review_date="2025-05-25",
                approval_date="2025-05-26",
                clash_detection_run=True,
                federated_model=True,
                coordinate_system="Shared Site Coordinates",
                description="Complete structural model with steel framing, concrete slabs, and foundation systems",
                review_comments="Model coordination complete. Ready for steel fabrication drawings.",
                change_log=["Rev 12: Updated connection details", "Rev 11: Added penthouse structure", "Rev 10: Revised foundation per soil report"],
                workflow_stage="Fabrication Ready",
                next_milestone="Steel Shop Drawings - June 1, 2025",
                assigned_to="Structural Team"
            ),
            BIMModel(
                model_id="model-003",
                model_code="HTD-MECH-001",
                model_name="Highland Tower - HVAC Systems Model",
                model_type=ModelType.MECHANICAL,
                discipline="Mechanical Engineering",
                version="2.1",
                revision="Rev-08",
                status=ModelStatus.IN_REVIEW,
                file_name="Highland_Tower_HVAC_Rev08.rvt",
                file_path="/bim/models/mechanical/Highland_Tower_HVAC_Rev08.rvt",
                file_size=112000000,  # 112 MB
                file_format="RVT",
                project_phase="Design Development",
                level_range="Level B1 to Roof",
                building_section="Full Building",
                created_by="Lisa Park - Mechanical Engineer",
                reviewed_by="Tom Brown - MEP Manager",
                approved_by=None,
                created_date="2025-04-01",
                last_modified="2025-05-27",
                review_date="2025-05-27",
                approval_date=None,
                clash_detection_run=True,
                federated_model=True,
                coordinate_system="Shared Site Coordinates",
                description="Complete HVAC systems including VAV boxes, ductwork, and equipment",
                review_comments="Minor clashes with structural beams on Level 12-13. Requires coordination.",
                change_log=["Rev 08: Coordinated with electrical routing", "Rev 07: Added penthouse equipment", "Rev 06: Updated duct sizing"],
                workflow_stage="Coordination Review",
                next_milestone="MEP Coordination Meeting - May 30, 2025",
                assigned_to="Mechanical Team"
            )
        ]
        
        for model in sample_models:
            self.models[model.model_id] = model
        
        # Sample Clash Detection Results
        sample_clashes = [
            ClashDetection(
                clash_id="clash-001",
                clash_code="HTD-CLASH-001",
                clash_name="HVAC Duct vs Structural Beam Conflict",
                model_a="HTD-MECH-001",
                model_b="HTD-STRUC-001",
                element_a="24x18 Supply Duct - Level 12",
                element_b="W24x68 Steel Beam - Grid B-3",
                clash_type="Hard Clash",
                severity=ClashSeverity.HIGH,
                discipline_conflict="Mechanical vs Structural",
                building_level="Level 12",
                zone="Office Area - Zone B",
                coordinates={"x": 125.5, "y": 89.2, "z": 144.0},
                status=ClashStatus.IN_PROGRESS,
                assigned_to="Lisa Park - Mechanical Engineer",
                priority=2,
                resolution_method="Reroute ductwork around beam",
                resolution_notes="Coordinating with structural team to confirm beam location and clearances",
                estimated_cost=2850.0,
                detected_date="2025-05-25",
                assigned_date="2025-05-26",
                resolved_date=None,
                target_resolution="2025-05-30",
                screenshot_path="/bim/clashes/screenshots/clash-001.png",
                markup_files=["/bim/clashes/markups/clash-001-markup.bcf"],
                related_rfis=["RFI-023"],
                created_by="Clash Detection System",
                reviewed_by="Tom Brown - MEP Manager",
                approved_resolution=False
            ),
            ClashDetection(
                clash_id="clash-002",
                clash_code="HTD-CLASH-002",
                clash_name="Electrical Conduit vs Plumbing Pipe",
                model_a="HTD-ELEC-001",
                model_b="HTD-PLUMB-001",
                element_a="4-inch Electrical Conduit Run",
                element_b="6-inch Domestic Water Pipe",
                clash_type="Soft Clash",
                severity=ClashSeverity.MEDIUM,
                discipline_conflict="Electrical vs Plumbing",
                building_level="Level 13",
                zone="Utility Chase - East",
                coordinates={"x": 98.3, "y": 156.7, "z": 157.5},
                status=ClashStatus.RESOLVED,
                assigned_to="Mark Johnson - Electrical Engineer",
                priority=3,
                resolution_method="Adjusted conduit routing with 6-inch clearance",
                resolution_notes="Coordinated with plumbing team. New routing approved by both disciplines.",
                estimated_cost=450.0,
                detected_date="2025-05-22",
                assigned_date="2025-05-23",
                resolved_date="2025-05-27",
                target_resolution="2025-05-29",
                screenshot_path="/bim/clashes/screenshots/clash-002.png",
                markup_files=["/bim/clashes/markups/clash-002-markup.bcf", "/bim/clashes/markups/clash-002-resolution.bcf"],
                related_rfis=[],
                created_by="Clash Detection System",
                reviewed_by="Tom Brown - MEP Manager",
                approved_resolution=True
            ),
            ClashDetection(
                clash_id="clash-003",
                clash_code="HTD-CLASH-003",
                clash_name="Fire Sprinkler vs Ceiling Light Fixture",
                model_a="HTD-FIRE-001",
                model_b="HTD-ELEC-001",
                element_a="Sprinkler Head - Type A",
                element_b="Recessed LED Fixture - 2x2",
                clash_type="Clearance",
                severity=ClashSeverity.LOW,
                discipline_conflict="Fire Protection vs Electrical",
                building_level="Level 10",
                zone="Office Area - Zone C",
                coordinates={"x": 215.8, "y": 67.4, "z": 120.3},
                status=ClashStatus.OPEN,
                assigned_to="Safety Team",
                priority=4,
                resolution_method="Relocate light fixture 18 inches north",
                resolution_notes="Requires coordination with interior design for lighting layout adjustment",
                estimated_cost=125.0,
                detected_date="2025-05-28",
                assigned_date="2025-05-28",
                resolved_date=None,
                target_resolution="2025-06-05",
                screenshot_path="/bim/clashes/screenshots/clash-003.png",
                markup_files=[],
                related_rfis=[],
                created_by="Clash Detection System",
                reviewed_by=None,
                approved_resolution=False
            )
        ]
        
        for clash in sample_clashes:
            self.clashes[clash.clash_id] = clash
        
        # Sample Coordination Session
        sample_session = ModelCoordination(
            session_id="coord-001",
            session_name="Highland Tower MEP Coordination Meeting #12",
            coordination_type="Clash Resolution",
            meeting_date="2025-05-27",
            attendees=["Tom Brown - MEP Manager", "Lisa Park - Mechanical", "Mark Johnson - Electrical", "Sarah Chen - Plumbing", "John Smith - Project Manager"],
            disciplines=["Mechanical", "Electrical", "Plumbing", "Fire Protection"],
            models_reviewed=["HTD-MECH-001", "HTD-ELEC-001", "HTD-PLUMB-001", "HTD-FIRE-001"],
            federated_model="HTD-FEDERATED-Rev12",
            issues_discussed=["Level 12-13 HVAC routing conflicts", "Electrical panel clearances", "Domestic water riser coordination"],
            decisions_made=["Reroute main supply duct around beam grid B-3", "Relocate electrical panel EP-12A", "Approve plumbing riser route"],
            action_items=[
                {"task": "Update HVAC model with new routing", "assignee": "Lisa Park", "due_date": "2025-05-30"},
                {"task": "Coordinate with structural on beam clearances", "assignee": "Tom Brown", "due_date": "2025-05-29"},
                {"task": "Update electrical panel layout", "assignee": "Mark Johnson", "due_date": "2025-06-02"}
            ],
            clashes_reviewed=["HTD-CLASH-001", "HTD-CLASH-002"],
            clashes_resolved=["HTD-CLASH-002"],
            new_clashes_identified=["HTD-CLASH-003"],
            meeting_notes="Productive coordination session. Major HVAC conflicts identified and solutions agreed upon. Follow-up meeting scheduled for next week.",
            presentation_files=["/bim/coordination/presentations/MEP-Coord-12-Presentation.pdf"],
            markup_files=["/bim/coordination/markups/Level12-Coordination.bcf"],
            next_meeting_date="2025-06-03",
            outstanding_actions=3,
            created_by="Tom Brown - MEP Manager",
            created_at="2025-05-27 14:30:00"
        )
        
        self.coordination_sessions[sample_session.session_id] = sample_session
        self.next_model_code = 4
        self.next_clash_code = 4
    
    def create_bim_model(self, model_data: Dict[str, Any]) -> str:
        """Create a new BIM model"""
        model_id = f"model-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        model_code = f"HTD-{model_data['discipline'].upper()[:4]}-{self.next_model_code:03d}"
        
        model_data.update({
            "model_id": model_id,
            "model_code": model_code,
            "created_date": datetime.now().strftime('%Y-%m-%d'),
            "last_modified": datetime.now().strftime('%Y-%m-%d'),
            "change_log": [],
            "clash_detection_run": False,
            "federated_model": False
        })
        
        # Convert enums
        model_data["model_type"] = ModelType(model_data["model_type"])
        model_data["status"] = ModelStatus(model_data["status"])
        
        model = BIMModel(**model_data)
        self.models[model_id] = model
        self.next_model_code += 1
        
        return model_id
    
    def create_clash_detection(self, clash_data: Dict[str, Any]) -> str:
        """Create a new clash detection result"""
        clash_id = f"clash-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        clash_code = f"HTD-CLASH-{self.next_clash_code:03d}"
        
        clash_data.update({
            "clash_id": clash_id,
            "clash_code": clash_code,
            "detected_date": datetime.now().strftime('%Y-%m-%d'),
            "assigned_date": datetime.now().strftime('%Y-%m-%d'),
            "resolved_date": None,
            "status": ClashStatus.OPEN,
            "markup_files": [],
            "related_rfis": [],
            "approved_resolution": False
        })
        
        # Convert enums
        clash_data["severity"] = ClashSeverity(clash_data["severity"])
        
        clash = ClashDetection(**clash_data)
        self.clashes[clash_id] = clash
        self.next_clash_code += 1
        
        return clash_id
    
    def get_bim_model(self, model_id: str) -> Optional[BIMModel]:
        """Get a specific BIM model"""
        return self.models.get(model_id)
    
    def get_all_models(self) -> List[BIMModel]:
        """Get all BIM models sorted by last modified"""
        return sorted(self.models.values(), key=lambda m: m.last_modified, reverse=True)
    
    def get_models_by_discipline(self, discipline: str) -> List[BIMModel]:
        """Get models by discipline"""
        return [model for model in self.models.values() if model.discipline == discipline]
    
    def get_models_by_status(self, status: ModelStatus) -> List[BIMModel]:
        """Get models by status"""
        return [model for model in self.models.values() if model.status == status]
    
    def get_all_clashes(self) -> List[ClashDetection]:
        """Get all clash detections sorted by severity and date"""
        clashes = list(self.clashes.values())
        severity_order = {ClashSeverity.CRITICAL: 0, ClashSeverity.HIGH: 1, ClashSeverity.MEDIUM: 2, ClashSeverity.LOW: 3, ClashSeverity.INFORMATION: 4}
        return sorted(clashes, key=lambda c: (severity_order.get(c.severity, 5), c.detected_date), reverse=True)
    
    def get_open_clashes(self) -> List[ClashDetection]:
        """Get open clash detections"""
        return [clash for clash in self.clashes.values() if clash.status in [ClashStatus.OPEN, ClashStatus.IN_PROGRESS]]
    
    def get_clashes_by_severity(self, severity: ClashSeverity) -> List[ClashDetection]:
        """Get clashes by severity"""
        return [clash for clash in self.clashes.values() if clash.severity == severity]
    
    def resolve_clash(self, clash_id: str, resolution_notes: str) -> bool:
        """Mark a clash as resolved"""
        clash = self.clashes.get(clash_id)
        if not clash:
            return False
        
        clash.status = ClashStatus.RESOLVED
        clash.resolved_date = datetime.now().strftime('%Y-%m-%d')
        clash.resolution_notes = resolution_notes
        clash.approved_resolution = True
        
        return True
    
    def update_model_status(self, model_id: str, new_status: ModelStatus) -> bool:
        """Update BIM model status"""
        model = self.models.get(model_id)
        if not model:
            return False
        
        model.status = new_status
        model.last_modified = datetime.now().strftime('%Y-%m-%d')
        
        if new_status == ModelStatus.APPROVED:
            model.approval_date = datetime.now().strftime('%Y-%m-%d')
        
        return True
    
    def generate_bim_metrics(self) -> Dict[str, Any]:
        """Generate BIM system metrics"""
        models = list(self.models.values())
        clashes = list(self.clashes.values())
        
        if not models and not clashes:
            return {}
        
        # Model metrics
        total_models = len(models)
        
        # Model status counts
        status_counts = {}
        for status in ModelStatus:
            status_counts[status.value] = len([m for m in models if m.status == status])
        
        # Model type counts
        type_counts = {}
        for model_type in ModelType:
            type_counts[model_type.value] = len([m for m in models if m.model_type == model_type])
        
        # Clash metrics
        total_clashes = len(clashes)
        open_clashes = len([c for c in clashes if c.status in [ClashStatus.OPEN, ClashStatus.IN_PROGRESS]])
        resolved_clashes = len([c for c in clashes if c.status == ClashStatus.RESOLVED])
        
        # Clash severity counts
        severity_counts = {}
        for severity in ClashSeverity:
            severity_counts[severity.value] = len([c for c in clashes if c.severity == severity])
        
        # File size analysis
        total_file_size = sum(m.file_size for m in models if m.file_size > 0)
        
        # Coordination metrics
        coordination_sessions = len(self.coordination_sessions)
        
        return {
            "total_models": total_models,
            "total_clashes": total_clashes,
            "open_clashes": open_clashes,
            "resolved_clashes": resolved_clashes,
            "model_status_breakdown": status_counts,
            "model_type_breakdown": type_counts,
            "clash_severity_breakdown": severity_counts,
            "total_storage_gb": round(total_file_size / 1024 / 1024 / 1024, 2),
            "coordination_sessions": coordination_sessions,
            "critical_clashes": severity_counts.get("Critical", 0),
            "high_priority_clashes": severity_counts.get("High", 0),
            "clash_resolution_rate": round((resolved_clashes / total_clashes * 100) if total_clashes > 0 else 0, 1)
        }

# Global instance for use across the application
bim_manager = BIMManager()