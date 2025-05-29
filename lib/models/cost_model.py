"""
Cost Management Model for gcPanel Construction Management Platform
"""

from models.base_model import BaseModel

class CostModel(BaseModel):
    """Cost management model with Highland Tower Development data"""
    
    def __init__(self):
        schema = {
            'id_prefix': 'CST',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'category': {'type': 'string', 'required': True},
                'description': {'type': 'string', 'required': True},
                'budgeted': {'type': 'number', 'required': True},
                'actual': {'type': 'number'},
                'committed': {'type': 'number'},
                'variance': {'type': 'number'},
                'date': {'type': 'date', 'required': True},
                'status': {'type': 'string', 'required': True},
                'phase': {'type': 'string'},
                'cost_code': {'type': 'string'},
                'vendor': {'type': 'string'}
            }
        }
        
        super().__init__('cost_items', schema)
        self._init_highland_tower_data()
    
    def _init_highland_tower_data(self):
        """Initialize with Highland Tower Development cost data"""
        if not self.get_all():
            highland_costs = [
                {
                    "id": "CST-001",
                    "category": "Labor",
                    "description": "Foundation Work - Phase 1",
                    "budgeted": 2850000,
                    "actual": 2785000,
                    "committed": 2785000,
                    "variance": -65000,
                    "date": "2024-03-30",
                    "status": "Completed",
                    "phase": "Phase 1 - Foundation",
                    "cost_code": "03-3000",
                    "vendor": "Morrison Construction LLC"
                },
                {
                    "id": "CST-002",
                    "category": "Materials",
                    "description": "Structural Steel - Floors 1-15",
                    "budgeted": 8750000,
                    "actual": 8900000,
                    "committed": 9100000,
                    "variance": 150000,
                    "date": "2024-12-15",
                    "status": "In Progress",
                    "phase": "Phase 2 - Structural",
                    "cost_code": "05-1200",
                    "vendor": "American Steel Fabricators"
                },
                {
                    "id": "CST-003",
                    "category": "Equipment",
                    "description": "Tower Crane Rental - 18 Months",
                    "budgeted": 450000,
                    "actual": 425000,
                    "committed": 450000,
                    "variance": -25000,
                    "date": "2024-06-30",
                    "status": "Completed",
                    "phase": "Phase 2 - Structural",
                    "cost_code": "01-5400",
                    "vendor": "Premier Crane Services"
                },
                {
                    "id": "CST-004",
                    "category": "Subcontractors",
                    "description": "MEP Systems Installation",
                    "budgeted": 12750000,
                    "actual": 6200000,
                    "committed": 12750000,
                    "variance": 0,
                    "date": "2024-12-15",
                    "status": "In Progress",
                    "phase": "Phase 2 - MEP Systems",
                    "cost_code": "23-0000",
                    "vendor": "Advanced Building Systems Inc"
                },
                {
                    "id": "CST-005",
                    "category": "Materials",
                    "description": "Curtain Wall System",
                    "budgeted": 8900000,
                    "actual": 2200000,
                    "committed": 8900000,
                    "variance": 0,
                    "date": "2024-12-15",
                    "status": "In Progress",
                    "phase": "Phase 3 - Building Envelope",
                    "cost_code": "08-4400",
                    "vendor": "Premium Glass & Facade Co"
                }
            ]
            
            for cost in highland_costs:
                super().create(cost)
    
    def get_total_budget(self):
        """Calculate total project budget"""
        return sum(item.get('budgeted', 0) for item in self.get_all())
    
    def get_total_actual(self):
        """Calculate total actual costs"""
        return sum(item.get('actual', 0) for item in self.get_all())
    
    def get_total_committed(self):
        """Calculate total committed costs"""
        return sum(item.get('committed', 0) for item in self.get_all())
    
    def get_cost_variance(self):
        """Calculate total cost variance"""
        return sum(item.get('variance', 0) for item in self.get_all())
    
    def get_costs_by_category(self, category: str):
        """Get costs by category"""
        return self.filter_records({'category': category})
    
    def get_over_budget_items(self):
        """Get items that are over budget"""
        return [item for item in self.get_all() if item.get('variance', 0) > 0]