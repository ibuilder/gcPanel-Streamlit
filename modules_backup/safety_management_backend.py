"""
Highland Tower Development - Safety Management Backend
Enterprise-grade safety incident tracking and compliance management.
"""

import json
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class IncidentSeverity(Enum):
    MINOR = "Minor"
    MODERATE = "Moderate" 
    SERIOUS = "Serious"
    CRITICAL = "Critical"

class IncidentType(Enum):
    INJURY = "Personal Injury"
    NEAR_MISS = "Near Miss"
    PROPERTY_DAMAGE = "Property Damage"
    ENVIRONMENTAL = "Environmental"
    EQUIPMENT = "Equipment Related"
    PROCEDURAL = "Procedural Violation"

class IncidentStatus(Enum):
    REPORTED = "Reported"
    INVESTIGATING = "Under Investigation"
    CORRECTIVE_ACTION = "Corrective Action Required"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class TrainingStatus(Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    EXPIRED = "Expired"

@dataclass
class SafetyIncident:
    """Safety incident record with comprehensive tracking"""
    incident_id: str
    date: str
    time: str
    location: str
    incident_type: IncidentType
    severity: IncidentSeverity
    status: IncidentStatus
    
    # People involved
    reported_by: str
    people_involved: List[str]
    witnesses: List[str]
    
    # Incident details
    description: str
    immediate_action: str
    root_cause: str
    corrective_actions: str
    
    # Investigation
    investigator: str
    investigation_notes: str
    photos_attached: bool
    
    # Dates
    reported_date: str
    investigation_date: Optional[str]
    resolution_date: Optional[str]
    
    # Follow-up
    follow_up_required: bool
    follow_up_date: Optional[str]
    lessons_learned: str
    
    created_at: str
    updated_at: str

@dataclass
class SafetyTraining:
    """Safety training record"""
    training_id: str
    training_name: str
    description: str
    instructor: str
    scheduled_date: str
    duration_hours: float
    max_attendees: int
    status: TrainingStatus
    
    # Attendees
    registered_attendees: List[str]
    completed_attendees: List[str]
    
    # Certification
    certification_valid_period: int  # months
    certification_required: bool
    
    # Training materials
    materials_provided: List[str]
    assessment_required: bool
    passing_score: int
    
    created_at: str
    updated_at: str

@dataclass
class SafetyMetrics:
    """Safety performance metrics"""
    total_incidents: int
    incidents_by_severity: Dict[str, int]
    incidents_by_type: Dict[str, int]
    days_since_last_incident: int
    total_training_hours: float
    compliance_rate: float
    investigation_completion_rate: float

class SafetyManager:
    """Enterprise safety management system"""
    
    def __init__(self):
        self.incidents: Dict[str, SafetyIncident] = {}
        self.training_records: Dict[str, SafetyTraining] = {}
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample safety data"""
        
        # Sample incident
        sample_incident = SafetyIncident(
            incident_id="SI-2025-001",
            date="2025-05-26",
            time="14:30",
            location="Level 12 - South Wing",
            incident_type=IncidentType.NEAR_MISS,
            severity=IncidentSeverity.MINOR,
            status=IncidentStatus.RESOLVED,
            reported_by="Mike Johnson",
            people_involved=["John Smith"],
            witnesses=["Sarah Wilson", "Tom Brown"],
            description="Worker nearly slipped on wet concrete surface near elevator area",
            immediate_action="Area cordoned off, warning signs placed, surface dried",
            root_cause="Inadequate drainage during concrete curing process",
            corrective_actions="Improved drainage system installed, additional safety signage",
            investigator="Safety Manager - Lisa Chen",
            investigation_notes="Investigation completed. No injury occurred. Process improved.",
            photos_attached=True,
            reported_date="2025-05-26",
            investigation_date="2025-05-27",
            resolution_date="2025-05-27",
            follow_up_required=False,
            follow_up_date=None,
            lessons_learned="Ensure proper drainage during all concrete operations",
            created_at="2025-05-26 14:45:00",
            updated_at="2025-05-27 16:00:00"
        )
        
        # Sample training
        sample_training = SafetyTraining(
            training_id="ST-2025-001",
            training_name="Fall Protection Certification",
            description="Comprehensive fall protection training for heights over 6 feet",
            instructor="SafetyFirst Training Inc.",
            scheduled_date="2025-06-01",
            duration_hours=8.0,
            max_attendees=20,
            status=TrainingStatus.SCHEDULED,
            registered_attendees=["John Smith", "Mike Johnson", "Sarah Wilson", "Tom Brown"],
            completed_attendees=[],
            certification_valid_period=24,
            certification_required=True,
            materials_provided=["Training Manual", "Safety Harness", "Certificate"],
            assessment_required=True,
            passing_score=80,
            created_at="2025-05-20 09:00:00",
            updated_at="2025-05-27 10:00:00"
        )
        
        self.incidents[sample_incident.incident_id] = sample_incident
        self.training_records[sample_training.training_id] = sample_training
    
    # Incident Management
    def create_incident(self, incident_data: Dict[str, Any]) -> str:
        """Create a new safety incident"""
        incident_id = f"SI-{datetime.now().strftime('%Y-%m-%d')}-{str(uuid.uuid4())[:8]}"
        
        incident_data.update({
            'incident_id': incident_id,
            'status': IncidentStatus.REPORTED,
            'reported_date': datetime.now().strftime('%Y-%m-%d'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        })
        
        # Convert enums
        incident_data['incident_type'] = IncidentType(incident_data['incident_type'])
        incident_data['severity'] = IncidentSeverity(incident_data['severity'])
        incident_data['status'] = IncidentStatus(incident_data['status'])
        
        incident = SafetyIncident(**incident_data)
        self.incidents[incident_id] = incident
        
        return incident_id
    
    def get_incident(self, incident_id: str) -> Optional[SafetyIncident]:
        """Get a specific incident"""
        return self.incidents.get(incident_id)
    
    def get_all_incidents(self) -> List[SafetyIncident]:
        """Get all incidents sorted by date (newest first)"""
        return sorted(self.incidents.values(), 
                     key=lambda i: i.date, 
                     reverse=True)
    
    def update_incident(self, incident_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing incident"""
        if incident_id not in self.incidents:
            return False
        
        incident = self.incidents[incident_id]
        
        for key, value in updates.items():
            if hasattr(incident, key):
                setattr(incident, key, value)
        
        incident.updated_at = datetime.now().isoformat()
        return True
    
    def get_incidents_by_status(self, status: IncidentStatus) -> List[SafetyIncident]:
        """Get incidents by status"""
        return [incident for incident in self.incidents.values() 
                if incident.status == status]
    
    def get_incidents_by_severity(self, severity: IncidentSeverity) -> List[SafetyIncident]:
        """Get incidents by severity"""
        return [incident for incident in self.incidents.values() 
                if incident.severity == severity]
    
    # Training Management
    def create_training(self, training_data: Dict[str, Any]) -> str:
        """Create a new training session"""
        training_id = f"ST-{datetime.now().strftime('%Y-%m-%d')}-{str(uuid.uuid4())[:8]}"
        
        training_data.update({
            'training_id': training_id,
            'status': TrainingStatus.SCHEDULED,
            'registered_attendees': training_data.get('registered_attendees', []),
            'completed_attendees': training_data.get('completed_attendees', []),
            'materials_provided': training_data.get('materials_provided', []),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        })
        
        training_data['status'] = TrainingStatus(training_data['status'])
        
        training = SafetyTraining(**training_data)
        self.training_records[training_id] = training
        
        return training_id
    
    def get_training(self, training_id: str) -> Optional[SafetyTraining]:
        """Get a specific training session"""
        return self.training_records.get(training_id)
    
    def get_all_training(self) -> List[SafetyTraining]:
        """Get all training sessions"""
        return sorted(self.training_records.values(), 
                     key=lambda t: t.scheduled_date, 
                     reverse=True)
    
    def register_attendee(self, training_id: str, attendee_name: str) -> bool:
        """Register an attendee for training"""
        training = self.training_records.get(training_id)
        if not training:
            return False
        
        if len(training.registered_attendees) >= training.max_attendees:
            return False
        
        if attendee_name not in training.registered_attendees:
            training.registered_attendees.append(attendee_name)
            training.updated_at = datetime.now().isoformat()
        
        return True
    
    def complete_training(self, training_id: str, attendee_name: str) -> bool:
        """Mark attendee as having completed training"""
        training = self.training_records.get(training_id)
        if not training:
            return False
        
        if (attendee_name in training.registered_attendees and 
            attendee_name not in training.completed_attendees):
            training.completed_attendees.append(attendee_name)
            training.updated_at = datetime.now().isoformat()
            return True
        
        return False
    
    # Analytics and Metrics
    def generate_safety_metrics(self) -> SafetyMetrics:
        """Generate comprehensive safety metrics"""
        incidents = list(self.incidents.values())
        
        if not incidents:
            return SafetyMetrics(
                total_incidents=0,
                incidents_by_severity={},
                incidents_by_type={},
                days_since_last_incident=0,
                total_training_hours=0.0,
                compliance_rate=0.0,
                investigation_completion_rate=0.0
            )
        
        # Count by severity
        severity_counts = {}
        for severity in IncidentSeverity:
            severity_counts[severity.value] = len([i for i in incidents if i.severity == severity])
        
        # Count by type
        type_counts = {}
        for incident_type in IncidentType:
            type_counts[incident_type.value] = len([i for i in incidents if i.incident_type == incident_type])
        
        # Days since last incident
        latest_incident_date = max(incident.date for incident in incidents)
        days_since = (datetime.now().date() - datetime.strptime(latest_incident_date, '%Y-%m-%d').date()).days
        
        # Total training hours
        total_training_hours = sum(training.duration_hours for training in self.training_records.values())
        
        # Investigation completion rate
        investigated_count = len([i for i in incidents if i.investigation_date])
        investigation_rate = (investigated_count / len(incidents)) * 100 if incidents else 0
        
        # Compliance rate (based on resolved incidents)
        resolved_count = len([i for i in incidents if i.status == IncidentStatus.RESOLVED])
        compliance_rate = (resolved_count / len(incidents)) * 100 if incidents else 0
        
        return SafetyMetrics(
            total_incidents=len(incidents),
            incidents_by_severity=severity_counts,
            incidents_by_type=type_counts,
            days_since_last_incident=days_since,
            total_training_hours=total_training_hours,
            compliance_rate=compliance_rate,
            investigation_completion_rate=investigation_rate
        )
    
    def validate_incident_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate incident data"""
        errors = []
        
        required_fields = ['date', 'time', 'location', 'incident_type', 'severity', 'description', 'reported_by']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        return errors
    
    def validate_training_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate training data"""
        errors = []
        
        required_fields = ['training_name', 'instructor', 'scheduled_date', 'duration_hours', 'max_attendees']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        if data.get('duration_hours', 0) <= 0:
            errors.append("Duration hours must be greater than 0")
        
        if data.get('max_attendees', 0) <= 0:
            errors.append("Max attendees must be greater than 0")
        
        return errors

# Global instance for use across the application
safety_manager = SafetyManager()