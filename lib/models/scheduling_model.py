"""
Scheduling Model for gcPanel Construction Management Platform
"""

from models.base_model import BaseModel

class SchedulingModel(BaseModel):
    """Project scheduling model with Highland Tower Development data"""
    
    def __init__(self):
        schema = {
            'id_prefix': 'SCH',
            'fields': {
                'id': {'type': 'string', 'required': True},
                'task_name': {'type': 'string', 'required': True},
                'start_date': {'type': 'date', 'required': True},
                'end_date': {'type': 'date', 'required': True},
                'duration': {'type': 'number', 'required': True},
                'predecessor': {'type': 'string'},
                'resource': {'type': 'string', 'required': True},
                'progress': {'type': 'number', 'required': True},
                'status': {'type': 'string', 'required': True},
                'phase': {'type': 'string'},
                'critical_path': {'type': 'boolean'},
                'notes': {'type': 'string'}
            }
        }
        
        super().__init__('schedule_items', schema)
        self._init_highland_tower_data()
    
    def _init_highland_tower_data(self):
        """Initialize with Highland Tower Development schedule data"""
        if not self.get_all():
            highland_schedule = [
                {
                    "id": "SCH-001",
                    "task_name": "Foundation Excavation",
                    "start_date": "2024-01-15",
                    "end_date": "2024-02-15",
                    "duration": 31,
                    "predecessor": "",
                    "resource": "Morrison Construction - Excavation Crew",
                    "progress": 100,
                    "status": "Completed",
                    "phase": "Phase 1 - Foundation",
                    "critical_path": True,
                    "notes": "Completed ahead of schedule due to favorable weather"
                },
                {
                    "id": "SCH-002",
                    "task_name": "Foundation Concrete Pour",
                    "start_date": "2024-02-16",
                    "end_date": "2024-03-30",
                    "duration": 43,
                    "predecessor": "SCH-001",
                    "resource": "Morrison Construction - Concrete Crew",
                    "progress": 100,
                    "status": "Completed",
                    "phase": "Phase 1 - Foundation",
                    "critical_path": True,
                    "notes": "Quality control inspections passed all requirements"
                },
                {
                    "id": "SCH-003",
                    "task_name": "Structural Steel Erection - Floors 1-10",
                    "start_date": "2024-04-01",
                    "end_date": "2024-07-15",
                    "duration": 105,
                    "predecessor": "SCH-002",
                    "resource": "Morrison Construction - Steel Crew",
                    "progress": 95,
                    "status": "In Progress",
                    "phase": "Phase 2 - Structural",
                    "critical_path": True,
                    "notes": "Minor delay due to steel delivery, recovered through overtime"
                },
                {
                    "id": "SCH-004",
                    "task_name": "MEP Rough-In - Floors 1-5",
                    "start_date": "2024-06-01",
                    "end_date": "2024-08-30",
                    "duration": 90,
                    "predecessor": "SCH-003",
                    "resource": "Advanced Building Systems - MEP Team",
                    "progress": 75,
                    "status": "In Progress",
                    "phase": "Phase 2 - MEP Systems",
                    "critical_path": False,
                    "notes": "Coordination with structural team ongoing"
                },
                {
                    "id": "SCH-005",
                    "task_name": "Curtain Wall Installation",
                    "start_date": "2024-09-01",
                    "end_date": "2025-02-28",
                    "duration": 180,
                    "predecessor": "SCH-003",
                    "resource": "Premium Glass & Facade Co",
                    "progress": 25,
                    "status": "In Progress",
                    "phase": "Phase 3 - Building Envelope",
                    "critical_path": True,
                    "notes": "Weather-dependent activities scheduled for favorable seasons"
                }
            ]
            
            for task in highland_schedule:
                super().create(task)
    
    def get_critical_path_tasks(self):
        """Get all critical path tasks"""
        return [task for task in self.get_all() if task.get('critical_path', False)]
    
    def get_tasks_by_phase(self, phase: str):
        """Get tasks by project phase"""
        return self.filter_records({'phase': phase})
    
    def get_delayed_tasks(self):
        """Get tasks that are behind schedule"""
        from datetime import datetime
        today = datetime.now().date()
        delayed = []
        
        for task in self.get_all():
            if task.get('status') == 'In Progress':
                end_date = datetime.strptime(task['end_date'], '%Y-%m-%d').date()
                progress = task.get('progress', 0)
                if end_date < today and progress < 100:
                    delayed.append(task)
        
        return delayed