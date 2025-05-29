"""
RFI Model for gcPanel Construction Management Platform
"""

from models.base_model import BaseModel

class RFIModel(BaseModel):
    """RFI model with Highland Tower Development data"""
    
    def __init__(self):
        schema = {
            'id_prefix': 'RFI',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'title': {'type': 'string', 'required': True},
                'description': {'type': 'string', 'required': True},
                'trade': {'type': 'string', 'required': True},
                'priority': {'type': 'string', 'required': True},
                'submitted_by': {'type': 'string', 'required': True},
                'date_submitted': {'type': 'date', 'required': True},
                'status': {'type': 'string', 'required': True},
                'assignee': {'type': 'string'},
                'due_date': {'type': 'date'},
                'response': {'type': 'string'},
                'location': {'type': 'string'},
                'drawing_reference': {'type': 'string'}
            }
        }
        
        super().__init__('rfis', schema)
        self._init_highland_tower_data()
    
    def _init_highland_tower_data(self):
        """Initialize with Highland Tower Development RFI data"""
        if not self.get_all():
            highland_rfis = [
                {
                    "id": "RFI-001",
                    "title": "Structural Steel Connection Detail Clarification",
                    "description": "Request clarification on beam-to-column connection detail at grid intersection 15-C for floors 20-25",
                    "trade": "Structural",
                    "priority": "High",
                    "submitted_by": "Morrison Construction LLC",
                    "date_submitted": "2024-12-12",
                    "status": "Under Review",
                    "assignee": "Highland Structural Engineering",
                    "due_date": "2024-12-20",
                    "location": "Floors 20-25, Grid 15-C",
                    "drawing_reference": "S-301, S-302"
                },
                {
                    "id": "RFI-002",
                    "title": "HVAC Duct Routing Coordination",
                    "description": "HVAC ductwork conflicts with structural members on Floor 18. Request alternate routing options",
                    "trade": "Mechanical",
                    "priority": "Medium",
                    "submitted_by": "Advanced Building Systems Inc",
                    "date_submitted": "2024-12-10",
                    "status": "Responded",
                    "assignee": "Highland MEP Engineering",
                    "due_date": "2024-12-18",
                    "response": "Approved alternate routing through east corridor. See revised drawing M-418 Rev B.",
                    "location": "Floor 18 - Central Mechanical Room",
                    "drawing_reference": "M-418, S-318"
                },
                {
                    "id": "RFI-003",
                    "title": "Elevator Shaft Dimensions Verification",
                    "description": "Verify elevator shaft dimensions match equipment specifications for high-speed passenger elevators",
                    "trade": "Vertical Transportation",
                    "priority": "High",
                    "submitted_by": "Elite Elevator Solutions",
                    "date_submitted": "2024-12-08",
                    "status": "Pending Response",
                    "assignee": "Highland Architectural Team",
                    "due_date": "2024-12-22",
                    "location": "Elevator Shafts 1-4, All Floors",
                    "drawing_reference": "A-601, A-602, EL-101"
                }
            ]
            
            for rfi in highland_rfis:
                super().create(rfi)
    
    def get_rfis_by_priority(self, priority: str):
        """Get RFIs by priority level"""
        return self.filter_records({'priority': priority})
    
    def get_pending_rfis(self):
        """Get all pending RFIs"""
        return self.filter_records({'status': 'Pending Response'})
    
    def get_overdue_rfis(self):
        """Get overdue RFIs (past due date)"""
        from datetime import datetime
        today = datetime.now().date()
        overdue = []
        
        for rfi in self.get_all():
            if rfi.get('due_date') and rfi.get('status') != 'Responded':
                due_date = datetime.strptime(rfi['due_date'], '%Y-%m-%d').date()
                if due_date < today:
                    overdue.append(rfi)
        
        return overdue