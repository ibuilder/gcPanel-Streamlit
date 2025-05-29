"""
Pure Python Business Logic for Highland Tower Development
Construction Management Platform

Core business operations using standard Python for maximum efficiency and longevity
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, date, timedelta
import json
from dataclasses import asdict
from .data_models import (
    Project, RFI, Subcontractor, DailyReport, Inspection, Issue, Document, User,
    RFIStatus, Priority, Discipline, ProjectStatus, HIGHLAND_TOWER_PROJECT
)


class ProjectManager:
    """Core project management business logic"""
    
    def __init__(self):
        self.project = HIGHLAND_TOWER_PROJECT
        self.rfis: List[RFI] = []
        self.subcontractors: List[Subcontractor] = []
        self.daily_reports: List[DailyReport] = []
        self.inspections: List[Inspection] = []
        self.issues: List[Issue] = []
        self.documents: List[Document] = []
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with Highland Tower Development data"""
        # Highland Tower RFI data
        self.rfis = [
            RFI(
                id="HTD-RFI-001",
                number="RFI-2025-001",
                subject="Steel beam connection detail clarification Level 12-13",
                description="Need clarification on connection detail for main structural beams at Grid Line A between floors 12-13. Current drawings show conflicting details.",
                location="Level 12-13, Grid Line A-B",
                discipline=Discipline.STRUCTURAL,
                priority=Priority.HIGH,
                status=RFIStatus.OPEN,
                submitted_by="Mike Chen - Site Superintendent",
                assigned_to="Highland Structural Engineering",
                submitted_date=date(2025, 5, 20),
                due_date=date(2025, 5, 27),
                cost_impact="$15,000 - $25,000",
                schedule_impact="2-3 days",
                project_id=self.project.id
            ),
            RFI(
                id="HTD-RFI-002",
                number="RFI-2025-002",
                subject="HVAC ductwork routing coordination Level 12 mechanical room",
                description="HVAC ductwork conflicts with structural beams in north mechanical room. Need routing solution.",
                location="Level 12 - Mechanical Room North",
                discipline=Discipline.MEP,
                priority=Priority.MEDIUM,
                status=RFIStatus.IN_REVIEW,
                submitted_by="Sarah Johnson - Project Manager",
                assigned_to="Highland MEP Consultants",
                submitted_date=date(2025, 5, 18),
                due_date=date(2025, 5, 25),
                cost_impact="$5,000 - $10,000",
                schedule_impact="1-2 days",
                project_id=self.project.id
            ),
            RFI(
                id="HTD-RFI-003",
                number="RFI-2025-003",
                subject="Exterior curtain wall material specification south facade",
                description="Clarification needed on glass specifications for south-facing residential units 8-12.",
                location="South Facade - Units 8-12",
                discipline=Discipline.ARCHITECTURAL,
                priority=Priority.MEDIUM,
                status=RFIStatus.ANSWERED,
                submitted_by="Robert Kim - Architecture Team",
                assigned_to="Highland Architecture Group",
                submitted_date=date(2025, 5, 15),
                due_date=date(2025, 5, 22),
                cost_impact="$8,000 - $12,000",
                schedule_impact="No impact",
                project_id=self.project.id
            ),
            RFI(
                id="HTD-RFI-004",
                number="RFI-2025-004",
                subject="Electrical panel location retail space ground floor",
                description="Electrical panel location conflicts with retail tenant requirements. Need alternative placement.",
                location="Ground Floor - Retail Space 3",
                discipline=Discipline.ELECTRICAL,
                priority=Priority.LOW,
                status=RFIStatus.OPEN,
                submitted_by="Lisa Rodriguez - Quality Inspector",
                assigned_to="Highland Electrical Consultants",
                submitted_date=date(2025, 5, 22),
                due_date=date(2025, 5, 29),
                cost_impact="$2,000 - $5,000",
                schedule_impact="1 day",
                project_id=self.project.id
            ),
            RFI(
                id="HTD-RFI-005",
                number="RFI-2025-005",
                subject="Fire safety system integration residential levels",
                description="Fire safety system requires integration with building automation. Critical for occupancy permit.",
                location="Levels 2-15 - Residential",
                discipline=Discipline.FIRE_SAFETY,
                priority=Priority.CRITICAL,
                status=RFIStatus.OPEN,
                submitted_by="John Davis - Safety Manager",
                assigned_to="Fire Safety Consultants Inc",
                submitted_date=date(2025, 5, 23),
                due_date=date(2025, 5, 26),
                cost_impact="$25,000 - $40,000",
                schedule_impact="5-7 days",
                project_id=self.project.id
            )
        ]

        # Highland Tower Subcontractors
        self.subcontractors = [
            Subcontractor(
                id="SUB-001",
                company_name="Highland Construction Corp",
                contact_person="Michael Torres",
                email="m.torres@highlandconstruction.com",
                phone="(555) 123-4567",
                license_number="CA-LIC-123456",
                insurance_expiry=date(2025, 12, 31),
                specialties=["General Construction", "Concrete", "Steel"],
                performance_rating=4.8,
                active_projects=3,
                total_contract_value=28500000.0
            ),
            Subcontractor(
                id="SUB-002", 
                company_name="Elite MEP Solutions",
                contact_person="Jennifer Walsh",
                email="j.walsh@elitemep.com",
                phone="(555) 234-5678",
                license_number="CA-MEP-789012",
                insurance_expiry=date(2025, 11, 15),
                specialties=["HVAC", "Electrical", "Plumbing"],
                performance_rating=4.5,
                active_projects=2,
                total_contract_value=8200000.0
            ),
            Subcontractor(
                id="SUB-003",
                company_name="Premium Interior Finishes",
                contact_person="David Chen",
                email="d.chen@premiuminteriors.com", 
                phone="(555) 345-6789",
                license_number="CA-INT-345678",
                insurance_expiry=date(2025, 10, 30),
                specialties=["Interior Finishes", "Flooring", "Millwork"],
                performance_rating=4.7,
                active_projects=1,
                total_contract_value=6100000.0
            )
        ]

    # RFI Management Methods
    def get_rfis(self, status: Optional[RFIStatus] = None, 
                 priority: Optional[Priority] = None) -> List[RFI]:
        """Get RFIs with optional filtering"""
        rfis = self.rfis.copy()
        
        if status:
            rfis = [rfi for rfi in rfis if rfi.status == status]
        
        if priority:
            rfis = [rfi for rfi in rfis if rfi.priority == priority]
            
        return rfis
    
    def create_rfi(self, rfi_data: Dict[str, Any]) -> RFI:
        """Create new RFI"""
        rfi_id = f"HTD-RFI-{len(self.rfis) + 1:03d}"
        rfi_number = f"RFI-2025-{len(self.rfis) + 1:03d}"
        
        rfi = RFI(
            id=rfi_id,
            number=rfi_number,
            project_id=self.project.id,
            **rfi_data
        )
        
        self.rfis.append(rfi)
        return rfi
    
    def update_rfi(self, rfi_id: str, updates: Dict[str, Any]) -> Optional[RFI]:
        """Update existing RFI"""
        for rfi in self.rfis:
            if rfi.id == rfi_id:
                for key, value in updates.items():
                    if hasattr(rfi, key):
                        setattr(rfi, key, value)
                rfi.updated_at = datetime.now()
                return rfi
        return None
    
    def get_rfi_statistics(self) -> Dict[str, Any]:
        """Calculate RFI statistics"""
        total_rfis = len(self.rfis)
        open_rfis = len([rfi for rfi in self.rfis if rfi.status == RFIStatus.OPEN])
        critical_rfis = len([rfi for rfi in self.rfis if rfi.priority == Priority.CRITICAL])
        overdue_rfis = len([rfi for rfi in self.rfis if rfi.is_overdue])
        
        if total_rfis > 0:
            avg_days_open = sum(rfi.days_open for rfi in self.rfis) / total_rfis
        else:
            avg_days_open = 0
        
        return {
            "total": total_rfis,
            "open": open_rfis,
            "critical": critical_rfis,
            "overdue": overdue_rfis,
            "avg_days_open": round(avg_days_open, 1)
        }

    # Subcontractor Management Methods
    def get_subcontractors(self, specialty: Optional[str] = None) -> List[Subcontractor]:
        """Get subcontractors with optional specialty filtering"""
        if specialty:
            return [sub for sub in self.subcontractors if specialty in sub.specialties]
        return self.subcontractors.copy()
    
    def add_subcontractor(self, sub_data: Dict[str, Any]) -> Subcontractor:
        """Add new subcontractor"""
        sub_id = f"SUB-{len(self.subcontractors) + 1:03d}"
        subcontractor = Subcontractor(id=sub_id, **sub_data)
        self.subcontractors.append(subcontractor)
        return subcontractor
    
    def get_subcontractor_performance_summary(self) -> Dict[str, Any]:
        """Calculate subcontractor performance metrics"""
        if not self.subcontractors:
            return {}
        
        avg_rating = sum(sub.performance_rating for sub in self.subcontractors) / len(self.subcontractors)
        total_contract_value = sum(sub.total_contract_value for sub in self.subcontractors)
        active_projects = sum(sub.active_projects for sub in self.subcontractors)
        
        return {
            "total_subcontractors": len(self.subcontractors),
            "average_rating": round(avg_rating, 2),
            "total_contract_value": total_contract_value,
            "active_projects": active_projects
        }

    # Project Analytics Methods
    def get_project_health_metrics(self) -> Dict[str, Any]:
        """Calculate overall project health metrics"""
        rfi_stats = self.get_rfi_statistics()
        sub_stats = self.get_subcontractor_performance_summary()
        
        # Calculate project health score based on multiple factors
        rfi_health = max(0, 100 - (rfi_stats["overdue"] * 10) - (rfi_stats["critical"] * 5))
        budget_health = (self.project.budget_remaining / self.project.value) * 100
        schedule_health = 100 if self.project.progress_percent >= 67 else self.project.progress_percent * 1.5
        
        overall_health = (rfi_health + budget_health + schedule_health) / 3
        
        return {
            "overall_health_score": round(overall_health, 1),
            "progress_percent": self.project.progress_percent,
            "budget_remaining": self.project.budget_remaining,
            "days_to_completion": (self.project.end_date - date.today()).days,
            "rfi_health": round(rfi_health, 1),
            "active_rfis": rfi_stats["open"],
            "critical_issues": rfi_stats["critical"]
        }

    # Data Export Methods
    def export_project_data(self) -> Dict[str, Any]:
        """Export all project data as JSON-serializable dictionary"""
        return {
            "project": asdict(self.project),
            "rfis": [asdict(rfi) for rfi in self.rfis],
            "subcontractors": [asdict(sub) for sub in self.subcontractors],
            "project_health": self.get_project_health_metrics(),
            "export_date": datetime.now().isoformat()
        }

    def search_rfis(self, query: str) -> List[RFI]:
        """Search RFIs by subject and description"""
        query_lower = query.lower()
        return [
            rfi for rfi in self.rfis 
            if query_lower in rfi.subject.lower() or query_lower in rfi.description.lower()
        ]


# Global instance for Highland Tower Development
highland_tower_manager = ProjectManager()