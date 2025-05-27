"""
Highland Tower Development - RFI Management Backend
Enterprise-grade Request for Information (RFI) tracking and workflow management.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class RFIStatus(Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    ANSWERED = "Answered"
    CLOSED = "Closed"
    OVERDUE = "Overdue"

class RFIPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class RFICategory(Enum):
    DESIGN_CLARIFICATION = "Design Clarification"
    SPECIFICATION_QUESTION = "Specification Question"
    COORDINATION_ISSUE = "Coordination Issue"
    MATERIAL_SUBSTITUTION = "Material Substitution"
    CONSTRUCTION_METHOD = "Construction Method"
    SCHEDULE_IMPACT = "Schedule Impact"
    COST_IMPACT = "Cost Impact"
    SAFETY_CONCERN = "Safety Concern"

@dataclass
class RFIAttachment:
    """RFI document attachment"""
    attachment_id: str
    filename: str
    file_type: str
    file_size: int  # bytes
    uploaded_by: str
    upload_date: str
    description: str

@dataclass
class RFIResponse:
    """RFI response from reviewer"""
    response_id: str
    responded_by: str
    response_date: str
    response_text: str
    attachments: List[RFIAttachment]
    requires_further_clarification: bool

@dataclass
class RFI:
    """Complete RFI structure"""
    rfi_id: str
    rfi_number: str  # e.g., "RFI-2025-001"
    title: str
    description: str
    category: RFICategory
    priority: RFIPriority
    status: RFIStatus
    
    # Project info
    project_name: str
    location: str
    drawing_references: List[str]
    specification_sections: List[str]
    
    # People and dates
    submitted_by: str
    assigned_to: str
    reviewers: List[str]
    submitted_date: str
    due_date: str
    response_date: Optional[str]
    closed_date: Optional[str]
    
    # Content
    question: str
    justification: str
    proposed_solution: str
    schedule_impact: str
    cost_impact: str
    
    # Responses and attachments
    responses: List[RFIResponse]
    attachments: List[RFIAttachment]
    
    # Tracking
    created_at: str
    updated_at: str
    days_open: int
    
    def calculate_days_open(self) -> int:
        """Calculate days RFI has been open"""
        if self.status == RFIStatus.CLOSED and self.closed_date:
            end_date = datetime.strptime(self.closed_date, '%Y-%m-%d').date()
        else:
            end_date = date.today()
        
        start_date = datetime.strptime(self.submitted_date, '%Y-%m-%d').date()
        return (end_date - start_date).days
    
    def is_overdue(self) -> bool:
        """Check if RFI is overdue"""
        if self.status in [RFIStatus.CLOSED]:
            return False
        
        due_date = datetime.strptime(self.due_date, '%Y-%m-%d').date()
        return date.today() > due_date

class RFIManager:
    """Enterprise RFI management system"""
    
    def __init__(self):
        self.rfis: Dict[str, RFI] = {}
        self.next_rfi_number = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample RFI data"""
        
        # Sample RFI
        sample_rfi = RFI(
            rfi_id="rfi-2025-001",
            rfi_number="RFI-2025-001",
            title="Concrete Mix Design Clarification - Level 15",
            description="Need clarification on concrete mix specifications for high-rise pour",
            category=RFICategory.SPECIFICATION_QUESTION,
            priority=RFIPriority.HIGH,
            status=RFIStatus.ANSWERED,
            project_name="Highland Tower Development",
            location="Level 15 - North Wing",
            drawing_references=["S-301", "S-302", "A-151"],
            specification_sections=["03 30 00", "03 31 00"],
            submitted_by="John Smith - Project Manager",
            assigned_to="Sarah Wilson - Design Team Lead",
            reviewers=["Sarah Wilson", "Mike Johnson - Structural Engineer"],
            submitted_date="2025-05-20",
            due_date="2025-05-27",
            response_date="2025-05-25",
            closed_date=None,
            question="The structural drawings show 4000 PSI concrete for Level 15, but the specifications call for 5000 PSI. Which requirement takes precedence?",
            justification="This discrepancy could impact structural integrity and project schedule if not resolved before pour date.",
            proposed_solution="Use 5000 PSI concrete as specified in technical specifications",
            schedule_impact="2-day delay if concrete mix needs to be changed",
            cost_impact="Estimated $12,000 additional cost for higher strength concrete",
            responses=[
                RFIResponse(
                    response_id="resp-001",
                    responded_by="Sarah Wilson - Design Team Lead",
                    response_date="2025-05-25",
                    response_text="Use 5000 PSI concrete per specifications. The drawings will be updated in the next revision. Please proceed with 5000 PSI mix.",
                    attachments=[],
                    requires_further_clarification=False
                )
            ],
            attachments=[
                RFIAttachment(
                    attachment_id="att-001",
                    filename="concrete_spec_detail.pdf",
                    file_type="PDF",
                    file_size=2048576,
                    uploaded_by="John Smith",
                    upload_date="2025-05-20",
                    description="Concrete specification detail from project manual"
                )
            ],
            created_at="2025-05-20 09:00:00",
            updated_at="2025-05-25 14:30:00",
            days_open=7
        )
        
        # Additional sample RFIs
        sample_rfi_2 = RFI(
            rfi_id="rfi-2025-002",
            rfi_number="RFI-2025-002", 
            title="MEP Coordination - HVAC Routing Conflict",
            description="HVAC ductwork conflicts with structural beam placement",
            category=RFICategory.COORDINATION_ISSUE,
            priority=RFIPriority.CRITICAL,
            status=RFIStatus.UNDER_REVIEW,
            project_name="Highland Tower Development",
            location="Level 12 - Mechanical Room",
            drawing_references=["M-401", "M-402", "S-201"],
            specification_sections=["23 00 00", "23 31 00"],
            submitted_by="Mike Johnson - MEP Coordinator",
            assigned_to="Tom Brown - MEP Engineer",
            reviewers=["Tom Brown", "Lisa Chen - Structural Engineer"],
            submitted_date="2025-05-25",
            due_date="2025-06-01",
            response_date=None,
            closed_date=None,
            question="Main supply ductwork routing shown on M-401 conflicts with structural beam on S-201. Need alternative routing solution.",
            justification="Current design prevents proper HVAC installation and could delay mechanical rough-in by 2 weeks.",
            proposed_solution="Route ductwork below beam with additional supports or relocate beam if structurally feasible",
            schedule_impact="Potential 2-week delay in mechanical rough-in",
            cost_impact="TBD - depends on selected solution",
            responses=[],
            attachments=[],
            created_at="2025-05-25 11:00:00",
            updated_at="2025-05-25 11:00:00",
            days_open=2
        )
        
        sample_rfi_3 = RFI(
            rfi_id="rfi-2025-003",
            rfi_number="RFI-2025-003",
            title="Window Installation Sequence",
            description="Clarification needed on window installation timing",
            category=RFICategory.CONSTRUCTION_METHOD,
            priority=RFIPriority.MEDIUM,
            status=RFIStatus.SUBMITTED,
            project_name="Highland Tower Development",
            location="Levels 8-12 - East Facade",
            drawing_references=["A-301", "A-302"],
            specification_sections=["08 50 00"],
            submitted_by="Sarah Wilson - Site Supervisor",
            assigned_to="Project Manager",
            reviewers=["John Smith"],
            submitted_date="2025-05-27",
            due_date="2025-06-03",
            response_date=None,
            closed_date=None,
            question="Should windows be installed before or after exterior insulation completion?",
            justification="Need to coordinate trades and ensure proper weather sealing sequence.",
            proposed_solution="Install windows after insulation to ensure proper integration",
            schedule_impact="May affect facade completion timeline",
            cost_impact="Minimal - mainly scheduling coordination",
            responses=[],
            attachments=[],
            created_at="2025-05-27 08:00:00",
            updated_at="2025-05-27 08:00:00",
            days_open=0
        )
        
        self.rfis[sample_rfi.rfi_id] = sample_rfi
        self.rfis[sample_rfi_2.rfi_id] = sample_rfi_2
        self.rfis[sample_rfi_3.rfi_id] = sample_rfi_3
        self.next_rfi_number = 4
    
    def create_rfi(self, rfi_data: Dict[str, Any]) -> str:
        """Create a new RFI"""
        rfi_id = f"rfi-{datetime.now().strftime('%Y-%m-%d')}-{str(uuid.uuid4())[:8]}"
        rfi_number = f"RFI-2025-{self.next_rfi_number:03d}"
        
        # Calculate due date (default 7 days)
        due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        rfi_data.update({
            'rfi_id': rfi_id,
            'rfi_number': rfi_number,
            'status': RFIStatus.DRAFT,
            'submitted_date': datetime.now().strftime('%Y-%m-%d'),
            'due_date': rfi_data.get('due_date', due_date),
            'responses': [],
            'attachments': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'days_open': 0
        })
        
        # Convert enums
        rfi_data['category'] = RFICategory(rfi_data['category'])
        rfi_data['priority'] = RFIPriority(rfi_data['priority'])
        rfi_data['status'] = RFIStatus(rfi_data['status'])
        
        rfi = RFI(**rfi_data)
        self.rfis[rfi_id] = rfi
        self.next_rfi_number += 1
        
        return rfi_id
    
    def get_rfi(self, rfi_id: str) -> Optional[RFI]:
        """Get a specific RFI"""
        return self.rfis.get(rfi_id)
    
    def get_all_rfis(self) -> List[RFI]:
        """Get all RFIs sorted by date (newest first)"""
        rfis = list(self.rfis.values())
        # Update days_open for each RFI
        for rfi in rfis:
            rfi.days_open = rfi.calculate_days_open()
            # Update status if overdue
            if rfi.is_overdue() and rfi.status not in [RFIStatus.CLOSED]:
                rfi.status = RFIStatus.OVERDUE
        
        return sorted(rfis, key=lambda r: r.submitted_date, reverse=True)
    
    def update_rfi(self, rfi_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing RFI"""
        if rfi_id not in self.rfis:
            return False
        
        rfi = self.rfis[rfi_id]
        
        for key, value in updates.items():
            if hasattr(rfi, key):
                setattr(rfi, key, value)
        
        rfi.updated_at = datetime.now().isoformat()
        return True
    
    def add_response(self, rfi_id: str, response_data: Dict[str, Any]) -> bool:
        """Add a response to an RFI"""
        rfi = self.rfis.get(rfi_id)
        if not rfi:
            return False
        
        response_id = f"resp-{len(rfi.responses) + 1:03d}"
        response_data.update({
            'response_id': response_id,
            'response_date': datetime.now().strftime('%Y-%m-%d'),
            'attachments': response_data.get('attachments', [])
        })
        
        response = RFIResponse(**response_data)
        rfi.responses.append(response)
        
        # Update RFI status
        if not response.requires_further_clarification:
            rfi.status = RFIStatus.ANSWERED
            rfi.response_date = response.response_date
        
        rfi.updated_at = datetime.now().isoformat()
        return True
    
    def close_rfi(self, rfi_id: str) -> bool:
        """Close an RFI"""
        rfi = self.rfis.get(rfi_id)
        if not rfi:
            return False
        
        rfi.status = RFIStatus.CLOSED
        rfi.closed_date = datetime.now().strftime('%Y-%m-%d')
        rfi.updated_at = datetime.now().isoformat()
        return True
    
    def get_rfis_by_status(self, status: RFIStatus) -> List[RFI]:
        """Get RFIs by status"""
        return [rfi for rfi in self.get_all_rfis() if rfi.status == status]
    
    def get_rfis_by_priority(self, priority: RFIPriority) -> List[RFI]:
        """Get RFIs by priority"""
        return [rfi for rfi in self.get_all_rfis() if rfi.priority == priority]
    
    def get_overdue_rfis(self) -> List[RFI]:
        """Get all overdue RFIs"""
        return [rfi for rfi in self.get_all_rfis() if rfi.is_overdue()]
    
    def generate_rfi_metrics(self) -> Dict[str, Any]:
        """Generate RFI performance metrics"""
        rfis = list(self.rfis.values())
        
        if not rfis:
            return {}
        
        total_rfis = len(rfis)
        
        # Status counts
        status_counts = {}
        for status in RFIStatus:
            status_counts[status.value] = len([r for r in rfis if r.status == status])
        
        # Priority counts
        priority_counts = {}
        for priority in RFIPriority:
            priority_counts[priority.value] = len([r for r in rfis if r.priority == priority])
        
        # Average response time
        answered_rfis = [r for r in rfis if r.response_date]
        if answered_rfis:
            total_response_days = sum(r.days_open for r in answered_rfis)
            avg_response_time = total_response_days / len(answered_rfis)
        else:
            avg_response_time = 0
        
        # Overdue count
        overdue_count = len([r for r in rfis if r.is_overdue()])
        
        return {
            'total_rfis': total_rfis,
            'status_breakdown': status_counts,
            'priority_breakdown': priority_counts,
            'average_response_time': round(avg_response_time, 1),
            'overdue_count': overdue_count,
            'response_rate': round((len(answered_rfis) / total_rfis) * 100, 1) if rfis else 0
        }
    
    def validate_rfi_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate RFI data"""
        errors = []
        
        required_fields = ['title', 'description', 'category', 'priority', 'question', 'submitted_by', 'assigned_to']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        return errors

# Global instance for use across the application
rfi_manager = RFIManager()