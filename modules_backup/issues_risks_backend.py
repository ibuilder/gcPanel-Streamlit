"""
Highland Tower Development - Issues & Risks Management Backend
Enterprise-grade risk management with mitigation tracking and impact analysis.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class IssueType(Enum):
    TECHNICAL = "Technical Issue"
    SCHEDULE = "Schedule Issue"
    QUALITY = "Quality Issue"
    SAFETY = "Safety Issue"
    COORDINATION = "Coordination Issue"
    RESOURCE = "Resource Issue"
    EXTERNAL = "External Issue"

class RiskType(Enum):
    SCHEDULE_RISK = "Schedule Risk"
    COST_RISK = "Cost Risk"
    QUALITY_RISK = "Quality Risk"
    SAFETY_RISK = "Safety Risk"
    TECHNICAL_RISK = "Technical Risk"
    REGULATORY_RISK = "Regulatory Risk"
    WEATHER_RISK = "Weather Risk"
    SUPPLY_CHAIN_RISK = "Supply Chain Risk"

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Status(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    MONITORING = "Monitoring"

class Probability(Enum):
    VERY_LOW = "Very Low (10%)"
    LOW = "Low (25%)"
    MEDIUM = "Medium (50%)"
    HIGH = "High (75%)"
    VERY_HIGH = "Very High (90%)"

class Impact(Enum):
    MINIMAL = "Minimal"
    MINOR = "Minor"
    MODERATE = "Moderate"
    MAJOR = "Major"
    SEVERE = "Severe"

@dataclass
class MitigationAction:
    """Risk mitigation or issue resolution action"""
    action_id: str
    description: str
    assigned_to: str
    due_date: str
    status: Status
    completion_date: Optional[str]
    notes: str
    effectiveness: Optional[str]  # "High", "Medium", "Low"

@dataclass
class Issue:
    """Project issue tracking"""
    issue_id: str
    issue_number: str
    title: str
    description: str
    issue_type: IssueType
    priority: Priority
    status: Status
    
    # Project details
    project_name: str
    location: str
    work_package: str
    
    # People
    reported_by: str
    assigned_to: str
    
    # Dates
    reported_date: str
    due_date: str
    resolved_date: Optional[str]
    
    # Impact
    cost_impact: float
    schedule_impact_days: int
    description_impact: str
    
    # Resolution
    resolution_description: str
    mitigation_actions: List[MitigationAction]
    
    # Tracking
    days_open: int
    created_at: str
    updated_at: str
    
    def calculate_days_open(self) -> int:
        """Calculate days issue has been open"""
        if self.status == Status.CLOSED and self.resolved_date:
            end_date = datetime.strptime(self.resolved_date, '%Y-%m-%d').date()
        else:
            end_date = date.today()
        
        start_date = datetime.strptime(self.reported_date, '%Y-%m-%d').date()
        return (end_date - start_date).days

@dataclass
class Risk:
    """Project risk tracking"""
    risk_id: str
    risk_number: str
    title: str
    description: str
    risk_type: RiskType
    probability: Probability
    impact: Impact
    priority: Priority
    status: Status
    
    # Project details
    project_name: str
    category: str
    triggers: str
    
    # People
    identified_by: str
    risk_owner: str
    
    # Dates
    identified_date: str
    review_date: str
    last_updated: str
    
    # Analysis
    potential_cost_impact: float
    potential_schedule_impact: int
    likelihood_percentage: int
    risk_score: float  # probability x impact
    
    # Response
    response_strategy: str  # "Avoid", "Mitigate", "Transfer", "Accept"
    mitigation_actions: List[MitigationAction]
    contingency_plan: str
    
    # Monitoring
    early_warning_signs: List[str]
    monitoring_frequency: str
    next_review_date: str
    
    created_at: str
    updated_at: str
    
    def calculate_risk_score(self) -> float:
        """Calculate risk score based on probability and impact"""
        prob_values = {
            Probability.VERY_LOW: 0.1,
            Probability.LOW: 0.25,
            Probability.MEDIUM: 0.5,
            Probability.HIGH: 0.75,
            Probability.VERY_HIGH: 0.9
        }
        
        impact_values = {
            Impact.MINIMAL: 1,
            Impact.MINOR: 2,
            Impact.MODERATE: 3,
            Impact.MAJOR: 4,
            Impact.SEVERE: 5
        }
        
        return prob_values.get(self.probability, 0.5) * impact_values.get(self.impact, 3)

class IssuesRisksManager:
    """Enterprise issues and risks management system"""
    
    def __init__(self):
        self.issues: Dict[str, Issue] = {}
        self.risks: Dict[str, Risk] = {}
        self.next_issue_number = 1
        self.next_risk_number = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample data"""
        
        # Sample Issue 1 - Schedule Issue
        sample_issue_1 = Issue(
            issue_id="iss-001",
            issue_number="ISS-2025-001",
            title="Concrete Delivery Delay - Level 15",
            description="Concrete supplier experiencing delivery delays due to plant maintenance",
            issue_type=IssueType.SCHEDULE,
            priority=Priority.HIGH,
            status=Status.RESOLVED,
            project_name="Highland Tower Development",
            location="Level 15",
            work_package="Structure",
            reported_by="John Smith - Project Manager",
            assigned_to="Mike Johnson - Site Supervisor",
            reported_date="2025-05-20",
            due_date="2025-05-25",
            resolved_date="2025-05-23",
            cost_impact=15000.0,
            schedule_impact_days=2,
            description_impact="2-day delay in structural work, potential impact on MEP schedule",
            resolution_description="Secured alternative concrete supplier with expedited delivery",
            mitigation_actions=[
                MitigationAction(
                    action_id="act-001",
                    description="Contact backup concrete suppliers",
                    assigned_to="Mike Johnson",
                    due_date="2025-05-21",
                    status=Status.CLOSED,
                    completion_date="2025-05-21",
                    notes="ABC Concrete Supply agreed to expedited delivery",
                    effectiveness="High"
                ),
                MitigationAction(
                    action_id="act-002",
                    description="Revise schedule for following trades",
                    assigned_to="John Smith",
                    due_date="2025-05-22",
                    status=Status.CLOSED,
                    completion_date="2025-05-22",
                    notes="MEP schedule adjusted, no critical path impact",
                    effectiveness="High"
                )
            ],
            days_open=3,
            created_at="2025-05-20 08:00:00",
            updated_at="2025-05-23 16:30:00"
        )
        
        # Sample Issue 2 - Technical Issue
        sample_issue_2 = Issue(
            issue_id="iss-002",
            issue_number="ISS-2025-002",
            title="HVAC Ductwork Interference with Structural Beam",
            description="Main supply ductwork routing conflicts with structural beam placement",
            issue_type=IssueType.TECHNICAL,
            priority=Priority.CRITICAL,
            status=Status.IN_PROGRESS,
            project_name="Highland Tower Development",
            location="Level 12 - Mechanical Room",
            work_package="MEP Systems",
            reported_by="Tom Brown - MEP Coordinator",
            assigned_to="Sarah Wilson - Design Team",
            reported_date="2025-05-25",
            due_date="2025-06-01",
            resolved_date=None,
            cost_impact=0.0,  # TBD
            schedule_impact_days=0,  # TBD
            description_impact="Potential delay in MEP rough-in, redesign may be required",
            resolution_description="",
            mitigation_actions=[
                MitigationAction(
                    action_id="act-003",
                    description="Coordinate with structural engineer for beam relocation feasibility",
                    assigned_to="Lisa Chen",
                    due_date="2025-05-28",
                    status=Status.IN_PROGRESS,
                    completion_date=None,
                    notes="Meeting scheduled with structural team",
                    effectiveness=None
                ),
                MitigationAction(
                    action_id="act-004",
                    description="Develop alternative ductwork routing options",
                    assigned_to="Tom Brown",
                    due_date="2025-05-30",
                    status=Status.OPEN,
                    completion_date=None,
                    notes="Exploring routing below beam with additional supports",
                    effectiveness=None
                )
            ],
            days_open=2,
            created_at="2025-05-25 10:00:00",
            updated_at="2025-05-27 14:00:00"
        )
        
        # Sample Risk 1 - Weather Risk
        sample_risk_1 = Risk(
            risk_id="risk-001",
            risk_number="RISK-2025-001",
            title="Extended Winter Weather Impact on Facade Work",
            description="Potential for extended cold weather affecting exterior facade installation",
            risk_type=RiskType.WEATHER_RISK,
            probability=Probability.MEDIUM,
            impact=Impact.MODERATE,
            priority=Priority.MEDIUM,
            status=Status.MONITORING,
            project_name="Highland Tower Development",
            category="External Factors",
            triggers="Temperature below 40°F for more than 3 consecutive days",
            identified_by="John Smith - Project Manager",
            risk_owner="Mike Johnson - Site Supervisor",
            identified_date="2025-05-01",
            review_date="2025-05-27",
            last_updated="2025-05-27",
            potential_cost_impact=75000.0,
            potential_schedule_impact=10,
            likelihood_percentage=50,
            risk_score=1.5,
            response_strategy="Mitigate",
            mitigation_actions=[
                MitigationAction(
                    action_id="act-005",
                    description="Procure temporary weather protection systems",
                    assigned_to="Mike Johnson",
                    due_date="2025-11-01",
                    status=Status.OPEN,
                    completion_date=None,
                    notes="Researching enclosure options for winter work",
                    effectiveness=None
                ),
                MitigationAction(
                    action_id="act-006",
                    description="Develop winter work procedures",
                    assigned_to="Safety Manager",
                    due_date="2025-10-15",
                    status=Status.OPEN,
                    completion_date=None,
                    notes="Cold weather protocols for facade installation",
                    effectiveness=None
                )
            ],
            contingency_plan="Move facade work to interior areas during extreme weather, prioritize interior finishes",
            early_warning_signs=["Extended weather forecasts showing cold patterns", "First hard freeze of season"],
            monitoring_frequency="Weekly during winter months",
            next_review_date="2025-06-01",
            created_at="2025-05-01 09:00:00",
            updated_at="2025-05-27 11:00:00"
        )
        
        # Sample Risk 2 - Supply Chain Risk
        sample_risk_2 = Risk(
            risk_id="risk-002",
            risk_number="RISK-2025-002",
            title="Steel Delivery Delays from Primary Supplier",
            description="Risk of structural steel delivery delays due to supplier capacity constraints",
            risk_type=RiskType.SUPPLY_CHAIN_RISK,
            probability=Probability.LOW,
            impact=Impact.MAJOR,
            priority=Priority.MEDIUM,
            status=Status.MONITORING,
            project_name="Highland Tower Development",
            category="Supply Chain",
            triggers="Supplier reports capacity issues or delivery delays to other projects",
            identified_by="Sarah Wilson - Procurement",
            risk_owner="John Smith - Project Manager",
            identified_date="2025-05-15",
            review_date="2025-05-27",
            last_updated="2025-05-27",
            potential_cost_impact=200000.0,
            potential_schedule_impact=21,
            likelihood_percentage=25,
            risk_score=1.0,
            response_strategy="Mitigate",
            mitigation_actions=[
                MitigationAction(
                    action_id="act-007",
                    description="Identify and qualify backup steel suppliers",
                    assigned_to="Sarah Wilson",
                    due_date="2025-06-15",
                    status=Status.IN_PROGRESS,
                    completion_date=None,
                    notes="Contacted 3 potential backup suppliers",
                    effectiveness=None
                ),
                MitigationAction(
                    action_id="act-008",
                    description="Increase steel delivery monitoring frequency",
                    assigned_to="Mike Johnson",
                    due_date="2025-06-01",
                    status=Status.OPEN,
                    completion_date=None,
                    notes="Weekly check-ins with primary supplier",
                    effectiveness=None
                )
            ],
            contingency_plan="Engage backup supplier with expedited delivery, adjust schedule for critical path items",
            early_warning_signs=["Supplier reports production delays", "Other projects experience steel delays", "Market shortages reported"],
            monitoring_frequency="Bi-weekly",
            next_review_date="2025-06-10",
            created_at="2025-05-15 14:00:00",
            updated_at="2025-05-27 10:30:00"
        )
        
        self.issues[sample_issue_1.issue_id] = sample_issue_1
        self.issues[sample_issue_2.issue_id] = sample_issue_2
        self.risks[sample_risk_1.risk_id] = sample_risk_1
        self.risks[sample_risk_2.risk_id] = sample_risk_2
        self.next_issue_number = 3
        self.next_risk_number = 3
    
    def create_issue(self, issue_data: Dict[str, Any]) -> str:
        """Create a new issue"""
        issue_id = f"iss-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        issue_number = f"ISS-2025-{self.next_issue_number:03d}"
        
        issue_data.update({
            "issue_id": issue_id,
            "issue_number": issue_number,
            "status": Status.OPEN,
            "mitigation_actions": [],
            "days_open": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        issue_data["issue_type"] = IssueType(issue_data["issue_type"])
        issue_data["priority"] = Priority(issue_data["priority"])
        issue_data["status"] = Status(issue_data["status"])
        
        issue = Issue(**issue_data)
        self.issues[issue_id] = issue
        self.next_issue_number += 1
        
        return issue_id
    
    def create_risk(self, risk_data: Dict[str, Any]) -> str:
        """Create a new risk"""
        risk_id = f"risk-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        risk_number = f"RISK-2025-{self.next_risk_number:03d}"
        
        # Calculate next review date (default 30 days)
        next_review = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        risk_data.update({
            "risk_id": risk_id,
            "risk_number": risk_number,
            "status": Status.MONITORING,
            "next_review_date": next_review,
            "mitigation_actions": [],
            "early_warning_signs": risk_data.get("early_warning_signs", []),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        risk_data["risk_type"] = RiskType(risk_data["risk_type"])
        risk_data["probability"] = Probability(risk_data["probability"])
        risk_data["impact"] = Impact(risk_data["impact"])
        risk_data["priority"] = Priority(risk_data["priority"])
        risk_data["status"] = Status(risk_data["status"])
        
        risk = Risk(**risk_data)
        risk.risk_score = risk.calculate_risk_score()
        
        self.risks[risk_id] = risk
        self.next_risk_number += 1
        
        return risk_id
    
    def get_all_issues(self) -> List[Issue]:
        """Get all issues sorted by priority and date"""
        issues = list(self.issues.values())
        for issue in issues:
            issue.days_open = issue.calculate_days_open()
        
        # Sort by priority (Critical first) then by date
        priority_order = {Priority.CRITICAL: 0, Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
        return sorted(issues, key=lambda i: (priority_order.get(i.priority, 3), i.reported_date), reverse=True)
    
    def get_all_risks(self) -> List[Risk]:
        """Get all risks sorted by risk score"""
        risks = list(self.risks.values())
        for risk in risks:
            risk.risk_score = risk.calculate_risk_score()
        
        return sorted(risks, key=lambda r: r.risk_score, reverse=True)
    
    def generate_issues_metrics(self) -> Dict[str, Any]:
        """Generate issues performance metrics"""
        issues = list(self.issues.values())
        
        if not issues:
            return {}
        
        total_issues = len(issues)
        
        # Status counts
        status_counts = {}
        for status in Status:
            status_counts[status.value] = len([i for i in issues if i.status == status])
        
        # Priority counts
        priority_counts = {}
        for priority in Priority:
            priority_counts[priority.value] = len([i for i in issues if i.priority == priority])
        
        # Type counts
        type_counts = {}
        for issue_type in IssueType:
            type_counts[issue_type.value] = len([i for i in issues if i.issue_type == issue_type])
        
        # Resolution metrics
        resolved_issues = [i for i in issues if i.status == Status.RESOLVED]
        avg_resolution_time = sum(i.days_open for i in resolved_issues) / len(resolved_issues) if resolved_issues else 0
        
        # Cost impact
        total_cost_impact = sum(i.cost_impact for i in issues)
        
        return {
            "total_issues": total_issues,
            "open_issues": status_counts.get("Open", 0) + status_counts.get("In Progress", 0),
            "status_breakdown": status_counts,
            "priority_breakdown": priority_counts,
            "type_breakdown": type_counts,
            "average_resolution_time": round(avg_resolution_time, 1),
            "total_cost_impact": total_cost_impact,
            "critical_issues": priority_counts.get("Critical", 0)
        }
    
    def generate_risks_metrics(self) -> Dict[str, Any]:
        """Generate risks performance metrics"""
        risks = list(self.risks.values())
        
        if not risks:
            return {}
        
        total_risks = len(risks)
        
        # Risk score analysis
        risk_scores = [r.calculate_risk_score() for r in risks]
        avg_risk_score = sum(risk_scores) / len(risk_scores)
        high_risk_count = len([r for r in risks if r.calculate_risk_score() >= 3.0])
        
        # Type counts
        type_counts = {}
        for risk_type in RiskType:
            type_counts[risk_type.value] = len([r for r in risks if r.risk_type == risk_type])
        
        # Status counts
        status_counts = {}
        for status in Status:
            status_counts[status.value] = len([r for r in risks if r.status == status])
        
        # Impact analysis
        total_potential_cost = sum(r.potential_cost_impact for r in risks)
        total_potential_schedule = sum(r.potential_schedule_impact for r in risks)
        
        return {
            "total_risks": total_risks,
            "average_risk_score": round(avg_risk_score, 2),
            "high_risk_count": high_risk_count,
            "type_breakdown": type_counts,
            "status_breakdown": status_counts,
            "total_potential_cost_impact": total_potential_cost,
            "total_potential_schedule_impact": total_potential_schedule,
            "active_monitoring": status_counts.get("Monitoring", 0)
        }

# Global instance for use across the application
issues_risks_manager = IssuesRisksManager()