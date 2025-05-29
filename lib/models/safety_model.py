"""
Safety Model for gcPanel Construction Management Platform
"""

from lib.models.base_model import BaseModel

class SafetyModel(BaseModel):
    """Safety incident model with Highland Tower Development data"""
    
    def __init__(self):
        schema = {
            'id_prefix': 'SAF',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'date': {'type': 'date', 'required': True},
                'type': {'type': 'string', 'required': True},
                'severity': {'type': 'string', 'required': True},
                'location': {'type': 'string', 'required': True},
                'description': {'type': 'string', 'required': True},
                'reported_by': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'investigation_notes': {'type': 'string'},
                'corrective_actions': {'type': 'string'},
                'follow_up_required': {'type': 'boolean'}
            }
        }
        
        super().__init__('safety_incidents', schema)
        self._init_highland_tower_data()
    
    def _init_highland_tower_data(self):
        """Initialize with Highland Tower Development safety data"""
        if not self.get_all():
            highland_incidents = [
                {
                    "id": "SAF-001",
                    "date": "2024-12-10",
                    "type": "Near Miss",
                    "severity": "Medium",
                    "location": "Floor 15 - North Wing",
                    "description": "Worker nearly slipped on wet concrete surface during pour operation",
                    "reported_by": "John Martinez, Site Supervisor",
                    "status": "Investigated",
                    "investigation_notes": "Surface was not properly marked as wet. Additional signage installed.",
                    "corrective_actions": "Implemented mandatory wet surface protocol and additional warning signs",
                    "follow_up_required": False
                },
                {
                    "id": "SAF-002", 
                    "date": "2024-12-08",
                    "type": "First Aid",
                    "severity": "Low",
                    "location": "Ground Level - Loading Dock",
                    "description": "Minor cut on hand from handling steel materials without proper gloves",
                    "reported_by": "Sarah Johnson, Safety Officer",
                    "status": "Closed",
                    "investigation_notes": "Worker bypassed PPE requirements. Retrained on safety protocols.",
                    "corrective_actions": "Mandatory PPE refresher training for all steel handling crews",
                    "follow_up_required": False
                },
                {
                    "id": "SAF-003",
                    "date": "2024-12-05",
                    "type": "Equipment Incident", 
                    "severity": "High",
                    "location": "Floor 22 - Crane Operation Area",
                    "description": "Crane load swing exceeded safe parameters during steel beam placement",
                    "reported_by": "Mike Chen, Crane Operator",
                    "status": "Under Investigation",
                    "investigation_notes": "Wind conditions and load calculation being reviewed by engineering team",
                    "corrective_actions": "Suspended crane operations in winds >15mph, enhanced weather monitoring",
                    "follow_up_required": True
                }
            ]
            
            for incident in highland_incidents:
                super().create(incident)
    
    def get_incidents_by_severity(self, severity: str):
        """Get incidents by severity level"""
        return self.filter_records({'severity': severity})
    
    def get_open_incidents(self):
        """Get all open/under investigation incidents"""
        return [inc for inc in self.get_all() if inc.get('status') in ['Open', 'Under Investigation']]
    
    def get_incidents_requiring_followup(self):
        """Get incidents that require follow-up"""
        return [inc for inc in self.get_all() if inc.get('follow_up_required', False)]