"""
Contract Model for gcPanel Construction Management Platform
"""

from models.base_model import BaseModel

class ContractModel(BaseModel):
    """Contract-specific model with Highland Tower Development data"""
    
    def __init__(self):
        schema = {
            'id_prefix': 'CTR',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'title': {'type': 'string', 'required': True},
                'contractor': {'type': 'string', 'required': True},
                'contract_value': {'type': 'number', 'required': True},
                'type': {'type': 'string', 'required': True},
                'status': {'type': 'string', 'required': True},
                'start_date': {'type': 'date', 'required': True},
                'end_date': {'type': 'date', 'required': True},
                'description': {'type': 'string'},
                'project_phase': {'type': 'string'},
                'retention_percentage': {'type': 'number'},
                'payment_terms': {'type': 'string'}
            }
        }
        
        super().__init__('contracts', schema)
        self._init_highland_tower_data()
    
    def _init_highland_tower_data(self):
        """Initialize with Highland Tower Development contract data"""
        if not self.get_all():
            highland_contracts = [
                {
                    "id": "CTR-001",
                    "title": "Highland Tower Foundation & Structural Work",
                    "contractor": "Morrison Construction LLC",
                    "contract_value": 18500000,
                    "type": "Prime Contract",
                    "status": "Active",
                    "start_date": "2024-01-15",
                    "end_date": "2025-08-30",
                    "description": "Complete foundation, structural steel, and concrete work for Highland Tower mixed-use development",
                    "project_phase": "Phase 1 - Structural",
                    "retention_percentage": 5.0,
                    "payment_terms": "Net 30"
                },
                {
                    "id": "CTR-002", 
                    "title": "Highland Tower MEP Systems Installation",
                    "contractor": "Advanced Building Systems Inc",
                    "contract_value": 12750000,
                    "type": "Prime Contract",
                    "status": "Active",
                    "start_date": "2024-06-01",
                    "end_date": "2025-10-15",
                    "description": "Mechanical, electrical, and plumbing systems for 28-story mixed-use tower",
                    "project_phase": "Phase 2 - MEP",
                    "retention_percentage": 5.0,
                    "payment_terms": "Net 30"
                },
                {
                    "id": "CTR-003",
                    "title": "Highland Tower Elevator Systems",
                    "contractor": "Elite Elevator Solutions",
                    "contract_value": 3250000,
                    "type": "Subcontract",
                    "status": "Active", 
                    "start_date": "2024-09-15",
                    "end_date": "2025-06-30",
                    "description": "High-speed elevator installation and maintenance systems",
                    "project_phase": "Phase 2 - Vertical Transportation",
                    "retention_percentage": 10.0,
                    "payment_terms": "Net 45"
                },
                {
                    "id": "CTR-004",
                    "title": "Highland Tower Facade & Curtain Wall",
                    "contractor": "Premium Glass & Facade Co",
                    "contract_value": 8900000,
                    "type": "Subcontract", 
                    "status": "In Progress",
                    "start_date": "2024-11-01",
                    "end_date": "2025-09-30",
                    "description": "Complete exterior facade, curtain wall, and window systems",
                    "project_phase": "Phase 3 - Envelope",
                    "retention_percentage": 7.5,
                    "payment_terms": "Net 30"
                },
                {
                    "id": "CTR-005",
                    "title": "Highland Tower Interior Finishes",
                    "contractor": "Luxury Interiors Group",
                    "contract_value": 6850000,
                    "type": "Prime Contract",
                    "status": "Pending",
                    "start_date": "2025-03-01",
                    "end_date": "2025-12-15",
                    "description": "High-end interior finishes for residential and commercial spaces",
                    "project_phase": "Phase 4 - Finishes",
                    "retention_percentage": 5.0,
                    "payment_terms": "Net 30"
                }
            ]
            
            for contract in highland_contracts:
                super().create(contract)
    
    def get_active_contracts(self):
        """Get all active contracts"""
        return self.filter_records({'status': 'Active'})
    
    def get_contracts_by_phase(self, phase: str):
        """Get contracts by project phase"""
        return self.filter_records({'project_phase': phase})
    
    def get_total_contract_value(self):
        """Calculate total value of all contracts"""
        return sum(contract.get('contract_value', 0) for contract in self.get_all())
    
    def get_contracts_by_type(self, contract_type: str):
        """Get contracts by type (Prime Contract, Subcontract, etc.)"""
        return self.filter_records({'type': contract_type})