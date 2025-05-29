"""
Highland Tower Development - Inspections Management Backend
Enterprise-grade inspection tracking with compliance workflows and defect management.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class InspectionType(Enum):
    FOUNDATION = "Foundation Inspection"
    STRUCTURAL = "Structural Inspection"
    MEP = "MEP Systems Inspection"
    FIRE_SAFETY = "Fire Safety Inspection"
    ELECTRICAL = "Electrical Inspection"
    PLUMBING = "Plumbing Inspection"
    HVAC = "HVAC Inspection"
    FINAL = "Final Inspection"
    PUNCH_LIST = "Punch List Inspection"
    CODE_COMPLIANCE = "Code Compliance Inspection"

class InspectionStatus(Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    PASSED = "Passed"
    FAILED = "Failed"
    CONDITIONAL = "Conditional Pass"
    CANCELLED = "Cancelled"
    RESCHEDULED = "Rescheduled"

class DefectSeverity(Enum):
    MINOR = "Minor"
    MODERATE = "Moderate"
    MAJOR = "Major"
    CRITICAL = "Critical"

class InspectorType(Enum):
    CITY_INSPECTOR = "City Inspector"
    THIRD_PARTY = "Third Party Inspector"
    INTERNAL_QC = "Internal QC Inspector"
    ENGINEER = "Engineer"
    ARCHITECT = "Architect"

@dataclass
class InspectionDefect:
    """Individual defect found during inspection"""
    defect_id: str
    description: str
    location: str
    severity: DefectSeverity
    code_reference: Optional[str]
    photo_reference: Optional[str]
    corrective_action: str
    responsible_party: str
    due_date: str
    resolved_date: Optional[str]
    resolution_notes: str
    is_resolved: bool

@dataclass
class InspectionChecklistItem:
    """Individual checklist item for inspection"""
    item_id: str
    description: str
    code_reference: Optional[str]
    status: str  # "Pass", "Fail", "N/A"
    notes: str
    photo_required: bool
    photo_attached: bool

@dataclass
class Inspection:
    """Complete inspection record"""
    inspection_id: str
    inspection_number: str
    inspection_type: InspectionType
    status: InspectionStatus
    
    # Project details
    project_name: str
    location: str
    work_package: str
    permit_number: Optional[str]
    
    # Scheduling
    scheduled_date: str
    scheduled_time: str
    actual_date: Optional[str]
    actual_time: Optional[str]
    duration_hours: Optional[float]
    
    # Inspector details
    inspector_name: str
    inspector_type: InspectorType
    inspector_company: str
    inspector_license: Optional[str]
    inspector_contact: str
    
    # Scope and results
    scope_description: str
    checklist_items: List[InspectionChecklistItem]
    defects_found: List[InspectionDefect]
    overall_result: str  # "Pass", "Fail", "Conditional"
    
    # Documentation
    inspection_report: Optional[str]
    photos_attached: List[str]
    documents_attached: List[str]
    
    # Notes and comments
    inspector_notes: str
    contractor_notes: str
    follow_up_required: bool
    follow_up_date: Optional[str]
    
    # Compliance
    code_compliance: bool
    permit_closed: bool
    certificate_issued: bool
    certificate_number: Optional[str]
    
    # Workflow
    requested_by: str
    approved_by: Optional[str]
    
    # Tracking
    created_at: str
    updated_at: str
    
    def calculate_defect_summary(self) -> Dict[str, int]:
        """Calculate summary of defects by severity"""
        summary = {severity.value: 0 for severity in DefectSeverity}
        for defect in self.defects_found:
            summary[defect.severity.value] += 1
        return summary
    
    def calculate_completion_rate(self) -> float:
        """Calculate inspection checklist completion rate"""
        if not self.checklist_items:
            return 100.0
        
        completed_items = len([item for item in self.checklist_items if item.status in ["Pass", "Fail"]])
        return (completed_items / len(self.checklist_items)) * 100

class InspectionsManager:
    """Enterprise inspections management system"""
    
    def __init__(self):
        self.inspections: Dict[str, Inspection] = {}
        self.next_inspection_number = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample inspection data"""
        
        # Sample inspection 1 - Passed structural inspection
        sample_inspection_1 = Inspection(
            inspection_id="insp-001",
            inspection_number="HTD-INS-2025-001",
            inspection_type=InspectionType.STRUCTURAL,
            status=InspectionStatus.PASSED,
            project_name="Highland Tower Development",
            location="Level 15 - Structural Frame",
            work_package="Structure",
            permit_number="BP-2024-15847",
            scheduled_date="2025-05-25",
            scheduled_time="09:00",
            actual_date="2025-05-25",
            actual_time="09:15",
            duration_hours=2.5,
            inspector_name="Robert Chen",
            inspector_type=InspectorType.CITY_INSPECTOR,
            inspector_company="City Building Department",
            inspector_license="CI-12345",
            inspector_contact="rchen@city.gov",
            scope_description="Structural frame inspection for Level 15 concrete and steel work",
            checklist_items=[
                InspectionChecklistItem(
                    item_id="item-001",
                    description="Concrete strength verification",
                    code_reference="ACI 318-19",
                    status="Pass",
                    notes="28-day strength test results acceptable",
                    photo_required=True,
                    photo_attached=True
                ),
                InspectionChecklistItem(
                    item_id="item-002",
                    description="Rebar placement and coverage",
                    code_reference="ACI 318-19 Section 7.7",
                    status="Pass",
                    notes="Proper spacing and coverage verified",
                    photo_required=True,
                    photo_attached=True
                ),
                InspectionChecklistItem(
                    item_id="item-003",
                    description="Steel connection details",
                    code_reference="AISC 360-16",
                    status="Pass",
                    notes="All connections per approved shop drawings",
                    photo_required=False,
                    photo_attached=False
                )
            ],
            defects_found=[],
            overall_result="Pass",
            inspection_report="structural_inspection_L15_report.pdf",
            photos_attached=["structural_L15_01.jpg", "structural_L15_02.jpg"],
            documents_attached=["strength_test_results.pdf"],
            inspector_notes="Excellent workmanship. All structural elements meet code requirements.",
            contractor_notes="Ready to proceed with Level 16 construction",
            follow_up_required=False,
            follow_up_date=None,
            code_compliance=True,
            permit_closed=True,
            certificate_issued=True,
            certificate_number="CERT-2025-15001",
            requested_by="John Smith - Project Manager",
            approved_by="Robert Chen - City Inspector",
            created_at="2025-05-20 10:00:00",
            updated_at="2025-05-25 14:30:00"
        )
        
        # Sample inspection 2 - Failed MEP inspection with defects
        sample_inspection_2 = Inspection(
            inspection_id="insp-002",
            inspection_number="HTD-INS-2025-002",
            inspection_type=InspectionType.MEP,
            status=InspectionStatus.FAILED,
            project_name="Highland Tower Development",
            location="Level 12 - Mechanical Room",
            work_package="MEP Systems",
            permit_number="MP-2024-12456",
            scheduled_date="2025-05-27",
            scheduled_time="14:00",
            actual_date="2025-05-27",
            actual_time="14:15",
            duration_hours=3.0,
            inspector_name="Lisa Wong",
            inspector_type=InspectorType.THIRD_PARTY,
            inspector_company="MEP Inspection Services",
            inspector_license="MEP-9876",
            inspector_contact="lwong@mepinspect.com",
            scope_description="MEP rough-in inspection for Level 12 mechanical systems",
            checklist_items=[
                InspectionChecklistItem(
                    item_id="item-004",
                    description="HVAC ductwork installation",
                    code_reference="IMC 603.9",
                    status="Fail",
                    notes="Ductwork interference with structural beam",
                    photo_required=True,
                    photo_attached=True
                ),
                InspectionChecklistItem(
                    item_id="item-005",
                    description="Electrical conduit routing",
                    code_reference="NEC 314.16",
                    status="Pass",
                    notes="Proper conduit installation and support",
                    photo_required=False,
                    photo_attached=False
                ),
                InspectionChecklistItem(
                    item_id="item-006",
                    description="Fire damper installation",
                    code_reference="NFPA 90A",
                    status="Fail",
                    notes="Missing fire damper at corridor penetration",
                    photo_required=True,
                    photo_attached=True
                )
            ],
            defects_found=[
                InspectionDefect(
                    defect_id="def-001",
                    description="HVAC ductwork conflicts with structural beam at grid line B-5",
                    location="Level 12 - Grid B-5",
                    severity=DefectSeverity.MAJOR,
                    code_reference="IMC 603.9",
                    photo_reference="defect_001.jpg",
                    corrective_action="Reroute ductwork below beam or coordinate beam modification",
                    responsible_party="Highland MEP Contractors",
                    due_date="2025-06-01",
                    resolved_date=None,
                    resolution_notes="",
                    is_resolved=False
                ),
                InspectionDefect(
                    defect_id="def-002",
                    description="Missing fire damper at corridor wall penetration",
                    location="Level 12 - Corridor Wall",
                    severity=DefectSeverity.CRITICAL,
                    code_reference="NFPA 90A Section 5.3",
                    photo_reference="defect_002.jpg",
                    corrective_action="Install fire damper per approved drawings",
                    responsible_party="Highland MEP Contractors",
                    due_date="2025-05-30",
                    resolved_date=None,
                    resolution_notes="",
                    is_resolved=False
                )
            ],
            overall_result="Fail",
            inspection_report="mep_inspection_L12_report.pdf",
            photos_attached=["mep_L12_01.jpg", "defect_001.jpg", "defect_002.jpg"],
            documents_attached=["mep_drawings_L12.pdf"],
            inspector_notes="Two major defects identified. Reinspection required after corrections.",
            contractor_notes="Will coordinate with structural team on ductwork routing",
            follow_up_required=True,
            follow_up_date="2025-06-02",
            code_compliance=False,
            permit_closed=False,
            certificate_issued=False,
            certificate_number=None,
            requested_by="Tom Brown - MEP Coordinator",
            approved_by=None,
            created_at="2025-05-25 09:00:00",
            updated_at="2025-05-27 17:30:00"
        )
        
        # Sample inspection 3 - Scheduled electrical inspection
        sample_inspection_3 = Inspection(
            inspection_id="insp-003",
            inspection_number="HTD-INS-2025-003",
            inspection_type=InspectionType.ELECTRICAL,
            status=InspectionStatus.SCHEDULED,
            project_name="Highland Tower Development",
            location="Level 10 - Electrical Room",
            work_package="Electrical Systems",
            permit_number="EP-2024-10234",
            scheduled_date="2025-05-30",
            scheduled_time="10:00",
            actual_date=None,
            actual_time=None,
            duration_hours=None,
            inspector_name="David Martinez",
            inspector_type=InspectorType.CITY_INSPECTOR,
            inspector_company="City Electrical Department",
            inspector_license="EI-5432",
            inspector_contact="dmartinez@city.gov",
            scope_description="Electrical rough-in inspection for Level 10 distribution panels",
            checklist_items=[
                InspectionChecklistItem(
                    item_id="item-007",
                    description="Panel installation and grounding",
                    code_reference="NEC 408.3",
                    status="N/A",
                    notes="",
                    photo_required=True,
                    photo_attached=False
                ),
                InspectionChecklistItem(
                    item_id="item-008",
                    description="Conduit and wire installation",
                    code_reference="NEC 314.28",
                    status="N/A",
                    notes="",
                    photo_required=True,
                    photo_attached=False
                )
            ],
            defects_found=[],
            overall_result="Pending",
            inspection_report=None,
            photos_attached=[],
            documents_attached=["electrical_drawings_L10.pdf"],
            inspector_notes="",
            contractor_notes="Electrical rough-in 95% complete, ready for inspection",
            follow_up_required=False,
            follow_up_date=None,
            code_compliance=True,
            permit_closed=False,
            certificate_issued=False,
            certificate_number=None,
            requested_by="Sarah Wilson - Electrical Contractor",
            approved_by=None,
            created_at="2025-05-28 11:00:00",
            updated_at="2025-05-28 11:00:00"
        )
        
        self.inspections[sample_inspection_1.inspection_id] = sample_inspection_1
        self.inspections[sample_inspection_2.inspection_id] = sample_inspection_2
        self.inspections[sample_inspection_3.inspection_id] = sample_inspection_3
        self.next_inspection_number = 4
    
    def create_inspection(self, inspection_data: Dict[str, Any]) -> str:
        """Create a new inspection"""
        inspection_id = f"insp-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        inspection_number = f"HTD-INS-2025-{self.next_inspection_number:03d}"
        
        inspection_data.update({
            "inspection_id": inspection_id,
            "inspection_number": inspection_number,
            "status": InspectionStatus.SCHEDULED,
            "checklist_items": inspection_data.get("checklist_items", []),
            "defects_found": [],
            "photos_attached": [],
            "documents_attached": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        inspection_data["inspection_type"] = InspectionType(inspection_data["inspection_type"])
        inspection_data["status"] = InspectionStatus(inspection_data["status"])
        inspection_data["inspector_type"] = InspectorType(inspection_data["inspector_type"])
        
        inspection = Inspection(**inspection_data)
        self.inspections[inspection_id] = inspection
        self.next_inspection_number += 1
        
        return inspection_id
    
    def get_inspection(self, inspection_id: str) -> Optional[Inspection]:
        """Get a specific inspection"""
        return self.inspections.get(inspection_id)
    
    def get_all_inspections(self) -> List[Inspection]:
        """Get all inspections sorted by date (newest first)"""
        return sorted(self.inspections.values(),
                     key=lambda i: i.scheduled_date,
                     reverse=True)
    
    def get_inspections_by_status(self, status: InspectionStatus) -> List[Inspection]:
        """Get inspections by status"""
        return [insp for insp in self.inspections.values() if insp.status == status]
    
    def get_inspections_by_type(self, inspection_type: InspectionType) -> List[Inspection]:
        """Get inspections by type"""
        return [insp for insp in self.inspections.values() if insp.inspection_type == inspection_type]
    
    def add_defect(self, inspection_id: str, defect_data: Dict[str, Any]) -> bool:
        """Add a defect to an inspection"""
        inspection = self.inspections.get(inspection_id)
        if not inspection:
            return False
        
        defect_id = f"def-{len(inspection.defects_found) + 1:03d}"
        defect_data.update({
            "defect_id": defect_id,
            "is_resolved": False
        })
        
        # Convert enum
        defect_data["severity"] = DefectSeverity(defect_data["severity"])
        
        defect = InspectionDefect(**defect_data)
        inspection.defects_found.append(defect)
        inspection.updated_at = datetime.now().isoformat()
        
        return True
    
    def resolve_defect(self, inspection_id: str, defect_id: str, resolution_notes: str) -> bool:
        """Mark a defect as resolved"""
        inspection = self.inspections.get(inspection_id)
        if not inspection:
            return False
        
        for defect in inspection.defects_found:
            if defect.defect_id == defect_id:
                defect.is_resolved = True
                defect.resolved_date = datetime.now().strftime('%Y-%m-%d')
                defect.resolution_notes = resolution_notes
                break
        
        inspection.updated_at = datetime.now().isoformat()
        return True
    
    def complete_inspection(self, inspection_id: str, result: str, notes: str) -> bool:
        """Complete an inspection with final result"""
        inspection = self.inspections.get(inspection_id)
        if not inspection:
            return False
        
        inspection.overall_result = result
        inspection.inspector_notes = notes
        inspection.actual_date = datetime.now().strftime('%Y-%m-%d')
        inspection.actual_time = datetime.now().strftime('%H:%M')
        
        # Update status based on result
        if result == "Pass":
            inspection.status = InspectionStatus.PASSED
            inspection.code_compliance = True
        elif result == "Fail":
            inspection.status = InspectionStatus.FAILED
            inspection.code_compliance = False
        else:  # Conditional
            inspection.status = InspectionStatus.CONDITIONAL
            inspection.code_compliance = True
        
        inspection.updated_at = datetime.now().isoformat()
        return True
    
    def generate_inspection_metrics(self) -> Dict[str, Any]:
        """Generate inspection performance metrics"""
        inspections = list(self.inspections.values())
        
        if not inspections:
            return {}
        
        total_inspections = len(inspections)
        
        # Status counts
        status_counts = {}
        for status in InspectionStatus:
            status_counts[status.value] = len([i for i in inspections if i.status == status])
        
        # Type counts
        type_counts = {}
        for insp_type in InspectionType:
            type_counts[insp_type.value] = len([i for i in inspections if i.inspection_type == insp_type])
        
        # Pass rate
        passed_inspections = len([i for i in inspections if i.status == InspectionStatus.PASSED])
        pass_rate = (passed_inspections / total_inspections * 100) if total_inspections > 0 else 0
        
        # Defect analysis
        total_defects = sum(len(i.defects_found) for i in inspections)
        resolved_defects = sum(len([d for d in i.defects_found if d.is_resolved]) for i in inspections)
        defect_resolution_rate = (resolved_defects / total_defects * 100) if total_defects > 0 else 100
        
        # Critical defects
        critical_defects = sum(len([d for d in i.defects_found if d.severity == DefectSeverity.CRITICAL]) for i in inspections)
        
        return {
            "total_inspections": total_inspections,
            "status_breakdown": status_counts,
            "type_breakdown": type_counts,
            "pass_rate": round(pass_rate, 1),
            "total_defects": total_defects,
            "resolved_defects": resolved_defects,
            "defect_resolution_rate": round(defect_resolution_rate, 1),
            "critical_defects": critical_defects,
            "pending_inspections": status_counts.get("Scheduled", 0)
        }

# Global instance for use across the application
inspections_manager = InspectionsManager()