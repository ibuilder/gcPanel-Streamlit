"""
Highland Tower Development - Daily Reports Backend
Enterprise-grade daily report management with proper data validation and persistence.
"""

import json
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ReportStatus(Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    APPROVED = "Approved"
    REVISION_REQUIRED = "Revision Required"

class WeatherCondition(Enum):
    SUNNY = "Sunny"
    CLOUDY = "Cloudy"
    RAINY = "Rainy"
    SNOW = "Snow"
    WINDY = "Windy"

@dataclass
class WorkActivity:
    """Individual work activity within a daily report"""
    activity_id: str
    description: str
    crew_size: int
    hours_worked: float
    location: str
    progress_percentage: int
    notes: str = ""
    
    def __post_init__(self):
        if self.progress_percentage < 0 or self.progress_percentage > 100:
            raise ValueError("Progress percentage must be between 0 and 100")

@dataclass
class SafetyIncident:
    """Safety incident record for daily reports"""
    incident_id: str
    description: str
    severity: str  # "Minor", "Moderate", "Severe"
    action_taken: str
    reported_by: str
    timestamp: str

@dataclass
class MaterialDelivery:
    """Material delivery record for daily reports"""
    delivery_id: str
    supplier: str
    material_type: str
    quantity: str
    received_by: str
    notes: str = ""

@dataclass
class DailyReport:
    """Complete daily report structure"""
    report_id: str
    date: str
    project_name: str
    weather: WeatherCondition
    temperature: int
    crew_size: int
    work_hours: float
    status: ReportStatus
    created_by: str
    created_at: str
    updated_at: str
    
    # Detailed sections
    work_activities: List[WorkActivity]
    safety_incidents: List[SafetyIncident]
    material_deliveries: List[MaterialDelivery]
    
    # Summary fields
    work_summary: str
    challenges: str
    next_day_plan: str
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary for serialization"""
        data = asdict(self)
        data['weather'] = self.weather.value
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DailyReport':
        """Create report from dictionary"""
        # Convert enum values back
        data['weather'] = WeatherCondition(data['weather'])
        data['status'] = ReportStatus(data['status'])
        
        # Convert nested objects
        data['work_activities'] = [WorkActivity(**activity) for activity in data['work_activities']]
        data['safety_incidents'] = [SafetyIncident(**incident) for incident in data['safety_incidents']]
        data['material_deliveries'] = [MaterialDelivery(**delivery) for delivery in data['material_deliveries']]
        
        return cls(**data)

class DailyReportsManager:
    """Enterprise daily reports management system"""
    
    def __init__(self):
        self.reports: Dict[str, DailyReport] = {}
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample data"""
        sample_report = DailyReport(
            report_id="DR-2025-001",
            date="2025-05-27",
            project_name="Highland Tower Development",
            weather=WeatherCondition.SUNNY,
            temperature=72,
            crew_size=24,
            work_hours=8.5,
            status=ReportStatus.APPROVED,
            created_by="John Smith",
            created_at="2025-05-27 08:00:00",
            updated_at="2025-05-27 17:30:00",
            work_activities=[
                WorkActivity(
                    activity_id="WA-001",
                    description="Level 15 concrete pour - North wing",
                    crew_size=8,
                    hours_worked=8.0,
                    location="Level 15 - North Wing",
                    progress_percentage=85,
                    notes="Excellent progress, no delays"
                ),
                WorkActivity(
                    activity_id="WA-002",
                    description="MEP rough-in - Levels 12-14",
                    crew_size=6,
                    hours_worked=8.5,
                    location="Levels 12-14",
                    progress_percentage=70,
                    notes="On schedule for inspection"
                )
            ],
            safety_incidents=[],
            material_deliveries=[
                MaterialDelivery(
                    delivery_id="MD-001",
                    supplier="ABC Concrete Supply",
                    material_type="Ready Mix Concrete",
                    quantity="15 cubic yards",
                    received_by="Mike Johnson",
                    notes="Quality approved, on-time delivery"
                )
            ],
            work_summary="Successful concrete pour on Level 15. MEP work progressing well.",
            challenges="Minor coordination needed between concrete and MEP crews.",
            next_day_plan="Continue MEP work, begin Level 16 prep work.",
            notes="Weather conditions excellent for outdoor work."
        )
        
        self.reports[sample_report.report_id] = sample_report
    
    def create_report(self, report_data: Dict[str, Any]) -> str:
        """Create a new daily report"""
        report_id = f"DR-{datetime.now().strftime('%Y-%m-%d')}-{str(uuid.uuid4())[:8]}"
        
        # Set default values
        report_data.update({
            'report_id': report_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': ReportStatus.DRAFT,
            'work_activities': report_data.get('work_activities', []),
            'safety_incidents': report_data.get('safety_incidents', []),
            'material_deliveries': report_data.get('material_deliveries', [])
        })
        
        report = DailyReport.from_dict(report_data)
        self.reports[report_id] = report
        
        return report_id
    
    def get_report(self, report_id: str) -> Optional[DailyReport]:
        """Get a specific report"""
        return self.reports.get(report_id)
    
    def get_all_reports(self) -> List[DailyReport]:
        """Get all reports sorted by date (newest first)"""
        return sorted(self.reports.values(), 
                     key=lambda r: r.date, 
                     reverse=True)
    
    def update_report(self, report_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing report"""
        if report_id not in self.reports:
            return False
        
        report = self.reports[report_id]
        
        # Update fields
        for key, value in updates.items():
            if hasattr(report, key):
                setattr(report, key, value)
        
        report.updated_at = datetime.now().isoformat()
        return True
    
    def delete_report(self, report_id: str) -> bool:
        """Delete a report"""
        if report_id in self.reports:
            del self.reports[report_id]
            return True
        return False
    
    def get_reports_by_date_range(self, start_date: str, end_date: str) -> List[DailyReport]:
        """Get reports within a date range"""
        return [report for report in self.reports.values() 
                if start_date <= report.date <= end_date]
    
    def get_reports_by_status(self, status: ReportStatus) -> List[DailyReport]:
        """Get reports by status"""
        return [report for report in self.reports.values() 
                if report.status == status]
    
    def generate_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics for all reports"""
        reports = list(self.reports.values())
        
        if not reports:
            return {}
        
        total_reports = len(reports)
        total_crew_hours = sum(r.crew_size * r.work_hours for r in reports)
        avg_crew_size = sum(r.crew_size for r in reports) / total_reports
        
        status_counts = {}
        for status in ReportStatus:
            status_counts[status.value] = len([r for r in reports if r.status == status])
        
        return {
            'total_reports': total_reports,
            'total_crew_hours': total_crew_hours,
            'average_crew_size': round(avg_crew_size, 1),
            'status_breakdown': status_counts,
            'latest_report_date': max(r.date for r in reports) if reports else None
        }
    
    def validate_report_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate report data and return list of errors"""
        errors = []
        
        required_fields = ['date', 'weather', 'crew_size', 'work_hours', 'created_by']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        # Validate crew size
        if data.get('crew_size', 0) <= 0:
            errors.append("Crew size must be greater than 0")
        
        # Validate work hours
        if data.get('work_hours', 0) <= 0 or data.get('work_hours', 0) > 24:
            errors.append("Work hours must be between 0 and 24")
        
        # Validate temperature
        temp = data.get('temperature')
        if temp is not None and (temp < -50 or temp > 150):
            errors.append("Temperature must be realistic (-50 to 150 F)")
        
        return errors

# Global instance for use across the application
daily_reports_manager = DailyReportsManager()