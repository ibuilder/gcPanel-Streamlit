"""
Submittal Model for gcPanel Construction Management Platform
"""

from models.base_model import BaseModel

class SubmittalModel(BaseModel):
    """Submittal model with Highland Tower Development data"""
    
    def __init__(self):
        schema = {
            'id_prefix': 'SUB',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'title': {'type': 'string', 'required': True},
                'spec_section': {'type': 'string', 'required': True},
                'discipline': {'type': 'string', 'required': True},
                'submitted_by': {'type': 'string', 'required': True},
                'date_submitted': {'type': 'date', 'required': True},
                'status': {'type': 'string', 'required': True},
                'reviewer': {'type': 'string'},
                'review_due_date': {'type': 'date'},
                'description': {'type': 'string'},
                'manufacturer': {'type': 'string'},
                'model_number': {'type': 'string'},
                'revision': {'type': 'string'},
                'review_comments': {'type': 'string'}
            }
        }
        
        super().__init__('submittals', schema)
        self._init_highland_tower_data()
    
    def _init_highland_tower_data(self):
        """Initialize with Highland Tower Development submittal data"""
        if not self.get_all():
            highland_submittals = [
                {
                    "id": "SUB-001",
                    "title": "Structural Steel Shop Drawings - Phase 1",
                    "spec_section": "05 12 00",
                    "discipline": "Structural",
                    "submitted_by": "Morrison Construction LLC",
                    "date_submitted": "2024-12-10",
                    "status": "Under Review",
                    "reviewer": "Highland Structural Engineering",
                    "review_due_date": "2024-12-24",
                    "description": "Shop drawings for structural steel framing floors 1-10",
                    "manufacturer": "American Steel Fabricators",
                    "revision": "Rev A"
                },
                {
                    "id": "SUB-002",
                    "title": "Curtain Wall System Details",
                    "spec_section": "08 44 00",
                    "discipline": "Architectural",
                    "submitted_by": "Premium Glass & Facade Co",
                    "date_submitted": "2024-12-08",
                    "status": "Approved",
                    "reviewer": "Highland Architectural Team",
                    "review_due_date": "2024-12-22",
                    "description": "Curtain wall system specifications and installation details",
                    "manufacturer": "Guardian Glass Technologies",
                    "model_number": "CW-2800 Series",
                    "revision": "Rev B",
                    "review_comments": "Approved with minor revisions to anchor details. See marked drawings."
                },
                {
                    "id": "SUB-003", 
                    "title": "High-Speed Elevator Equipment",
                    "spec_section": "14 21 00",
                    "discipline": "Vertical Transportation",
                    "submitted_by": "Elite Elevator Solutions",
                    "date_submitted": "2024-12-05",
                    "status": "Resubmit Required",
                    "reviewer": "Highland MEP Engineering",
                    "review_due_date": "2024-12-19",
                    "description": "High-speed passenger elevator specifications and performance data",
                    "manufacturer": "Otis Elevator Company",
                    "model_number": "Gen3 Core",
                    "revision": "Rev A",
                    "review_comments": "Motor specifications do not meet energy efficiency requirements. Please revise and resubmit."
                },
                {
                    "id": "SUB-004",
                    "title": "HVAC Equipment Schedules",
                    "spec_section": "23 05 00",
                    "discipline": "Mechanical",
                    "submitted_by": "Advanced Building Systems Inc",
                    "date_submitted": "2024-12-12",
                    "status": "Under Review",
                    "reviewer": "Highland MEP Engineering", 
                    "review_due_date": "2024-12-26",
                    "description": "HVAC equipment schedules and performance specifications for all floors",
                    "manufacturer": "Trane Technologies",
                    "model_number": "Intellipak Series",
                    "revision": "Rev A"
                }
            ]
            
            for submittal in highland_submittals:
                super().create(submittal)
    
    def get_submittals_by_status(self, status: str):
        """Get submittals by status"""
        return self.filter_records({'status': status})
    
    def get_submittals_by_discipline(self, discipline: str):
        """Get submittals by discipline"""
        return self.filter_records({'discipline': discipline})
    
    def get_overdue_reviews(self):
        """Get submittals with overdue reviews"""
        from datetime import datetime
        today = datetime.now().date()
        overdue = []
        
        for submittal in self.get_all():
            if submittal.get('review_due_date') and submittal.get('status') == 'Under Review':
                due_date = datetime.strptime(submittal['review_due_date'], '%Y-%m-%d').date()
                if due_date < today:
                    overdue.append(submittal)
        
        return overdue
    
    def get_resubmit_required(self):
        """Get submittals requiring resubmission"""
        return self.filter_records({'status': 'Resubmit Required'})