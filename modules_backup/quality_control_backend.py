"""
Highland Tower Development - Quality Control Backend
Enterprise-grade quality management with inspection workflows and compliance tracking.
"""

import json
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class InspectionType(Enum):
    FOUNDATION = "Foundation"
    STRUCTURAL = "Structural"
    MEP = "MEP Systems"
    FIRE_SAFETY = "Fire Safety"
    ELEVATOR = "Elevator"
    FACADE = "Facade"
    INTERIOR = "Interior Finishes"
    FINAL = "Final Inspection"

class InspectionStatus(Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    PASSED = "Passed"
    FAILED = "Failed"
    CONDITIONAL_PASS = "Conditional Pass"
    CANCELLED = "Cancelled"

class DefectSeverity(Enum):
    MINOR = "Minor"
    MAJOR = "Major"
    CRITICAL = "Critical"

class DefectStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    VERIFIED = "Verified"

@dataclass
class QualityPhoto:
    """Quality control photo documentation"""
    photo_id: str
    filename: str
    description: str
    location: str
    timestamp: str
    taken_by: str
    file_size: int
    tags: List[str]

@dataclass
class QualityDefect:
    """Quality defect tracking"""
    defect_id: str
    description: str
    location: str
    severity: DefectSeverity
    status: DefectStatus
    
    # Details
    discovered_date: str
    discovered_by: str
    assigned_to: str
    due_date: str
    
    # Resolution
    corrective_action: str
    resolution_notes: str
    resolved_date: Optional[str]
    verified_by: Optional[str]
    
    # Documentation
    photos: List[QualityPhoto]
    
    created_at: str
    updated_at: str

@dataclass
class QualityChecklist:
    """Quality control checklist"""
    checklist_id: str
    name: str
    inspection_type: InspectionType
    items: List[Dict[str, Any]]  # List of checklist items with status
    completed_items: int
    total_items: int
    completion_percentage: float
    
    def calculate_completion(self):
        """Calculate completion percentage"""
        if self.total_items == 0:
            self.completion_percentage = 0.0
        else:
            self.completion_percentage = (self.completed_items / self.total_items) * 100

@dataclass
class QualityInspection:
    """Complete quality inspection record"""
    inspection_id: str
    inspection_number: str
    inspection_type: InspectionType
    status: InspectionStatus
    
    # Project details
    project_name: str
    location: str
    work_description: str
    contractor: str
    
    # Schedule
    scheduled_date: str
    scheduled_time: str
    actual_start_time: Optional[str]
    actual_end_time: Optional[str]
    
    # Personnel
    inspector: str
    inspector_certification: str
    attendees: List[str]
    
    # Results
    overall_result: str  # "Pass", "Fail", "Conditional"
    inspection_notes: str
    defects_found: List[QualityDefect]
    
    # Documentation
    checklist_used: Optional[QualityChecklist]
    photos: List[QualityPhoto]
    report_generated: bool
    
    # Compliance
    code_references: List[str]
    permit_numbers: List[str]
    
    created_at: str
    updated_at: str

class QualityManager:
    """Enterprise quality control management system"""
    
    def __init__(self):
        self.inspections: Dict[str, QualityInspection] = {}
        self.defects: Dict[str, QualityDefect] = {}
        self.checklists: Dict[str, QualityChecklist] = {}
        self.next_inspection_number = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample quality data"""
        
        # Sample checklist
        structural_checklist = QualityChecklist(
            checklist_id="cl-struct-001",
            name="Structural Inspection - Level 15",
            inspection_type=InspectionType.STRUCTURAL,
            items=[
                {"item": "Concrete strength verification", "status": "completed", "notes": "7-day break test passed"},
                {"item": "Rebar placement and spacing", "status": "completed", "notes": "Per structural drawings"},
                {"item": "Formwork removal inspection", "status": "completed", "notes": "No damage observed"},
                {"item": "Connection details verification", "status": "pending", "notes": "Awaiting final welding"},
                {"item": "Elevation and alignment check", "status": "completed", "notes": "Within tolerance"}
            ],
            completed_items=4,
            total_items=5,
            completion_percentage=80.0
        )
        
        # Sample defect
        sample_defect = QualityDefect(
            defect_id="def-001",
            description="Minor concrete surface imperfection on north wall",
            location="Level 15 - North Wall, Grid E-F",
            severity=DefectSeverity.MINOR,
            status=DefectStatus.RESOLVED,
            discovered_date="2025-05-25",
            discovered_by="Quality Inspector - Mike Johnson",
            assigned_to="Concrete Contractor",
            due_date="2025-05-30",
            corrective_action="Surface grinding and patching as per ACI standards",
            resolution_notes="Surface repaired and meets specification requirements",
            resolved_date="2025-05-28",
            verified_by="Mike Johnson",
            photos=[],
            created_at="2025-05-25 10:00:00",
            updated_at="2025-05-28 15:30:00"
        )
        
        # Sample inspection
        sample_inspection = QualityInspection(
            inspection_id="insp-001",
            inspection_number="QI-2025-001",
            inspection_type=InspectionType.STRUCTURAL,
            status=InspectionStatus.PASSED,
            project_name="Highland Tower Development",
            location="Level 15 - North Wing",
            work_description="Structural concrete and steel inspection",
            contractor="Highland Construction Co.",
            scheduled_date="2025-05-27",
            scheduled_time="09:00",
            actual_start_time="09:15",
            actual_end_time="11:30",
            inspector="Mike Johnson - PE",
            inspector_certification="ICC Structural Inspector",
            attendees=["John Smith - Project Manager", "Sarah Wilson - Site Supervisor"],
            overall_result="Pass",
            inspection_notes="All structural elements meet design specifications. Minor surface defect noted and corrected.",
            defects_found=[sample_defect],
            checklist_used=structural_checklist,
            photos=[],
            report_generated=True,
            code_references=["IBC 2021", "ACI 318-19", "AISC 360-16"],
            permit_numbers=["BP-2024-5678"],
            created_at="2025-05-27 09:00:00",
            updated_at="2025-05-27 11:45:00"
        )
        
        # Sample MEP inspection
        mep_inspection = QualityInspection(
            inspection_id="insp-002",
            inspection_number="QI-2025-002",
            inspection_type=InspectionType.MEP,
            status=InspectionStatus.IN_PROGRESS,
            project_name="Highland Tower Development",
            location="Levels 12-14 - Mechanical Rooms",
            work_description="MEP rough-in inspection",
            contractor="Highland MEP Contractors",
            scheduled_date="2025-05-28",
            scheduled_time="14:00",
            actual_start_time="14:00",
            actual_end_time=None,
            inspector="Tom Brown - MEP Inspector",
            inspector_certification="NECA Electrical Inspector",
            attendees=["Mike Johnson - MEP Coordinator"],
            overall_result="In Progress",
            inspection_notes="Inspection in progress. HVAC ductwork 80% complete.",
            defects_found=[],
            checklist_used=None,
            photos=[],
            report_generated=False,
            code_references=["NEC 2020", "IMC 2021", "IPC 2021"],
            permit_numbers=["MP-2024-1234", "EP-2024-5678"],
            created_at="2025-05-28 14:00:00",
            updated_at="2025-05-28 14:00:00"
        )
        
        self.inspections[sample_inspection.inspection_id] = sample_inspection
        self.inspections[mep_inspection.inspection_id] = mep_inspection
        self.defects[sample_defect.defect_id] = sample_defect
        self.checklists[structural_checklist.checklist_id] = structural_checklist
        self.next_inspection_number = 3
    
    def create_inspection(self, inspection_data: Dict[str, Any]) -> str:
        """Create a new quality inspection"""
        inspection_id = f"insp-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        inspection_number = f"QI-2025-{self.next_inspection_number:03d}"
        
        inspection_data.update({
            "inspection_id": inspection_id,
            "inspection_number": inspection_number,
            "status": InspectionStatus.SCHEDULED,
            "defects_found": [],
            "photos": [],
            "report_generated": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        inspection_data["inspection_type"] = InspectionType(inspection_data["inspection_type"])
        inspection_data["status"] = InspectionStatus(inspection_data["status"])
        
        inspection = QualityInspection(**inspection_data)
        self.inspections[inspection_id] = inspection
        self.next_inspection_number += 1
        
        return inspection_id
    
    def get_inspection(self, inspection_id: str) -> Optional[QualityInspection]:
        """Get a specific inspection"""
        return self.inspections.get(inspection_id)
    
    def get_all_inspections(self) -> List[QualityInspection]:
        """Get all inspections sorted by date (newest first)"""
        return sorted(self.inspections.values(),
                     key=lambda i: i.scheduled_date,
                     reverse=True)
    
    def update_inspection(self, inspection_id: str, updates: Dict[str, Any]) -> bool:
        """Update an inspection"""
        if inspection_id not in self.inspections:
            return False
        
        inspection = self.inspections[inspection_id]
        
        for key, value in updates.items():
            if hasattr(inspection, key):
                setattr(inspection, key, value)
        
        inspection.updated_at = datetime.now().isoformat()
        return True
    
    def create_defect(self, defect_data: Dict[str, Any]) -> str:
        """Create a new quality defect"""
        defect_id = f"def-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        defect_data.update({
            "defect_id": defect_id,
            "status": DefectStatus.OPEN,
            "photos": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        defect_data["severity"] = DefectSeverity(defect_data["severity"])
        defect_data["status"] = DefectStatus(defect_data["status"])
        
        defect = QualityDefect(**defect_data)
        self.defects[defect_id] = defect
        
        return defect_id
    
    def get_defects_by_status(self, status: DefectStatus) -> List[QualityDefect]:
        """Get defects by status"""
        return [defect for defect in self.defects.values() if defect.status == status]
    
    def get_defects_by_severity(self, severity: DefectSeverity) -> List[QualityDefect]:
        """Get defects by severity"""
        return [defect for defect in self.defects.values() if defect.severity == severity]
    
    def get_inspections_by_type(self, inspection_type: InspectionType) -> List[QualityInspection]:
        """Get inspections by type"""
        return [insp for insp in self.inspections.values() if insp.inspection_type == inspection_type]
    
    def get_inspections_by_status(self, status: InspectionStatus) -> List[QualityInspection]:
        """Get inspections by status"""
        return [insp for insp in self.inspections.values() if insp.status == status]
    
    def generate_quality_metrics(self) -> Dict[str, Any]:
        """Generate quality performance metrics"""
        inspections = list(self.inspections.values())
        defects = list(self.defects.values())
        
        # Inspection metrics
        total_inspections = len(inspections)
        passed_inspections = len([i for i in inspections if i.overall_result == "Pass"])
        failed_inspections = len([i for i in inspections if i.overall_result == "Fail"])
        
        pass_rate = (passed_inspections / total_inspections * 100) if total_inspections > 0 else 0
        
        # Defect metrics
        total_defects = len(defects)
        open_defects = len([d for d in defects if d.status == DefectStatus.OPEN])
        resolved_defects = len([d for d in defects if d.status == DefectStatus.RESOLVED])
        
        # Defect severity breakdown
        severity_counts = {}
        for severity in DefectSeverity:
            severity_counts[severity.value] = len([d for d in defects if d.severity == severity])
        
        # Inspection type breakdown
        type_counts = {}
        for insp_type in InspectionType:
            type_counts[insp_type.value] = len([i for i in inspections if i.inspection_type == insp_type])
        
        return {
            "total_inspections": total_inspections,
            "passed_inspections": passed_inspections,
            "failed_inspections": failed_inspections,
            "pass_rate": round(pass_rate, 1),
            "total_defects": total_defects,
            "open_defects": open_defects,
            "resolved_defects": resolved_defects,
            "defect_resolution_rate": round((resolved_defects / total_defects * 100), 1) if total_defects > 0 else 0,
            "severity_breakdown": severity_counts,
            "inspection_types": type_counts
        }
    
    def validate_inspection_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate inspection data"""
        errors = []
        
        required_fields = ["inspection_type", "location", "work_description", "contractor", 
                          "scheduled_date", "inspector"]
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        return errors
    
    def validate_defect_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate defect data"""
        errors = []
        
        required_fields = ["description", "location", "severity", "discovered_by", "assigned_to"]
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        return errors

# Global instance for use across the application
quality_manager = QualityManager()