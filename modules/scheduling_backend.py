"""
Highland Tower Development - Scheduling Management Backend
Enterprise-grade project scheduling with task management and milestone tracking.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    CANCELLED = "Cancelled"

class TaskPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class TaskType(Enum):
    CONSTRUCTION = "Construction"
    INSPECTION = "Inspection"
    DELIVERY = "Delivery"
    MILESTONE = "Milestone"
    PLANNING = "Planning"
    REVIEW = "Review"

@dataclass
class TaskDependency:
    """Task dependency relationship"""
    dependency_id: str
    predecessor_task_id: str
    dependency_type: str  # "Finish-to-Start", "Start-to-Start", "Finish-to-Finish", "Start-to-Finish"
    lag_days: int

@dataclass
class TaskResource:
    """Resource assigned to task"""
    resource_id: str
    resource_name: str
    resource_type: str  # "Labor", "Equipment", "Material"
    allocation_percentage: float
    cost_per_unit: float
    units_required: float

@dataclass
class ScheduleTask:
    """Complete schedule task record"""
    task_id: str
    task_number: str
    task_name: str
    description: str
    task_type: TaskType
    status: TaskStatus
    priority: TaskPriority
    
    # Project details
    project_name: str
    phase: str
    work_package: str
    location: str
    
    # Schedule
    planned_start_date: str
    planned_end_date: str
    actual_start_date: Optional[str]
    actual_end_date: Optional[str]
    duration_days: int
    
    # Progress
    percent_complete: float
    work_completed: float
    work_remaining: float
    
    # Resources
    assigned_to: str
    resources: List[TaskResource]
    
    # Dependencies
    dependencies: List[TaskDependency]
    
    # Cost tracking
    budgeted_cost: float
    actual_cost: float
    cost_variance: float
    
    # Notes and tracking
    notes: str
    constraints: str
    risks: str
    
    # Workflow
    created_by: str
    last_updated_by: str
    created_at: str
    updated_at: str
    
    def calculate_schedule_variance(self) -> int:
        """Calculate schedule variance in days"""
        if self.status == TaskStatus.COMPLETED and self.actual_end_date:
            planned_end = datetime.strptime(self.planned_end_date, '%Y-%m-%d')
            actual_end = datetime.strptime(self.actual_end_date, '%Y-%m-%d')
            return (actual_end - planned_end).days
        return 0
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.status == TaskStatus.COMPLETED:
            return False
        
        planned_end = datetime.strptime(self.planned_end_date, '%Y-%m-%d').date()
        return date.today() > planned_end

class SchedulingManager:
    """Enterprise scheduling management system"""
    
    def __init__(self):
        self.tasks: Dict[str, ScheduleTask] = {}
        self.next_task_number = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample scheduling data"""
        
        # Sample task 1 - Completed foundation work
        sample_task_1 = ScheduleTask(
            task_id="task-001",
            task_number="HTD-T-001",
            task_name="Foundation Excavation and Preparation",
            description="Site excavation and foundation preparation work",
            task_type=TaskType.CONSTRUCTION,
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.HIGH,
            project_name="Highland Tower Development",
            phase="Foundation",
            work_package="Site Preparation",
            location="Building Footprint",
            planned_start_date="2024-02-15",
            planned_end_date="2024-03-15",
            actual_start_date="2024-02-15",
            actual_end_date="2024-03-12",
            duration_days=28,
            percent_complete=100.0,
            work_completed=100.0,
            work_remaining=0.0,
            assigned_to="Highland Construction Crew A",
            resources=[
                TaskResource(
                    resource_id="res-001",
                    resource_name="Excavator Operator",
                    resource_type="Labor",
                    allocation_percentage=100.0,
                    cost_per_unit=65.0,
                    units_required=224.0  # 28 days * 8 hours
                ),
                TaskResource(
                    resource_id="res-002",
                    resource_name="CAT 320 Excavator",
                    resource_type="Equipment",
                    allocation_percentage=100.0,
                    cost_per_unit=450.0,
                    units_required=28.0  # 28 days
                )
            ],
            dependencies=[],
            budgeted_cost=125000.0,
            actual_cost=121500.0,
            cost_variance=-3500.0,
            notes="Completed 3 days ahead of schedule due to favorable weather",
            constraints="Weather dependent activity",
            risks="Weather delays, underground utilities",
            created_by="John Smith - Project Manager",
            last_updated_by="Mike Johnson - Site Supervisor",
            created_at="2024-01-15 09:00:00",
            updated_at="2024-03-12 16:30:00"
        )
        
        # Sample task 2 - In progress structural work
        sample_task_2 = ScheduleTask(
            task_id="task-002",
            task_number="HTD-T-002", 
            task_name="Structural Steel Installation - Levels 11-15",
            description="Install structural steel frame for upper levels",
            task_type=TaskType.CONSTRUCTION,
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.CRITICAL,
            project_name="Highland Tower Development",
            phase="Structure",
            work_package="Steel Frame",
            location="Levels 11-15",
            planned_start_date="2024-10-01",
            planned_end_date="2024-12-15",
            actual_start_date="2024-10-03",
            actual_end_date=None,
            duration_days=75,
            percent_complete=85.0,
            work_completed=63.75,
            work_remaining=11.25,
            assigned_to="Steel Fabricators Inc.",
            resources=[
                TaskResource(
                    resource_id="res-003",
                    resource_name="Certified Welder",
                    resource_type="Labor",
                    allocation_percentage=100.0,
                    cost_per_unit=78.0,
                    units_required=600.0  # 75 days * 8 hours
                ),
                TaskResource(
                    resource_id="res-004",
                    resource_name="Tower Crane",
                    resource_type="Equipment",
                    allocation_percentage=80.0,
                    cost_per_unit=1200.0,
                    units_required=75.0  # 75 days
                ),
                TaskResource(
                    resource_id="res-005",
                    resource_name="Structural Steel",
                    resource_type="Material",
                    allocation_percentage=100.0,
                    cost_per_unit=850.0,
                    units_required=245.0  # tons
                )
            ],
            dependencies=[
                TaskDependency(
                    dependency_id="dep-001",
                    predecessor_task_id="task-001",
                    dependency_type="Finish-to-Start",
                    lag_days=5
                )
            ],
            budgeted_cost=485000.0,
            actual_cost=412750.0,
            cost_variance=-72250.0,
            notes="On track for early completion, excellent crew performance",
            constraints="Tower crane availability, weather conditions",
            risks="Steel delivery delays, weather impacts",
            created_by="John Smith - Project Manager",
            last_updated_by="Lisa Chen - Steel Supervisor",
            created_at="2024-09-01 10:00:00",
            updated_at="2025-05-27 14:00:00"
        )
        
        # Sample task 3 - Upcoming MEP work
        sample_task_3 = ScheduleTask(
            task_id="task-003",
            task_number="HTD-T-003",
            task_name="MEP Systems Installation - Levels 12-15",
            description="Install HVAC, electrical, and plumbing systems",
            task_type=TaskType.CONSTRUCTION,
            status=TaskStatus.NOT_STARTED,
            priority=TaskPriority.HIGH,
            project_name="Highland Tower Development",
            phase="MEP Systems",
            work_package="Mechanical/Electrical/Plumbing",
            location="Levels 12-15",
            planned_start_date="2025-06-01",
            planned_end_date="2025-08-15",
            actual_start_date=None,
            actual_end_date=None,
            duration_days=75,
            percent_complete=0.0,
            work_completed=0.0,
            work_remaining=75.0,
            assigned_to="Highland MEP Contractors",
            resources=[
                TaskResource(
                    resource_id="res-006",
                    resource_name="HVAC Technician",
                    resource_type="Labor",
                    allocation_percentage=100.0,
                    cost_per_unit=72.0,
                    units_required=600.0
                ),
                TaskResource(
                    resource_id="res-007",
                    resource_name="Electrician",
                    resource_type="Labor",
                    allocation_percentage=100.0,
                    cost_per_unit=85.0,
                    units_required=600.0
                )
            ],
            dependencies=[
                TaskDependency(
                    dependency_id="dep-002",
                    predecessor_task_id="task-002",
                    dependency_type="Finish-to-Start",
                    lag_days=10
                )
            ],
            budgeted_cost=325000.0,
            actual_cost=0.0,
            cost_variance=0.0,
            notes="Waiting for structural completion, materials on order",
            constraints="Structural steel completion, permit approvals",
            risks="Equipment delivery delays, coordination issues",
            created_by="Tom Brown - MEP Manager",
            last_updated_by="Tom Brown - MEP Manager",
            created_at="2025-04-15 11:00:00",
            updated_at="2025-04-15 11:00:00"
        )
        
        self.tasks[sample_task_1.task_id] = sample_task_1
        self.tasks[sample_task_2.task_id] = sample_task_2
        self.tasks[sample_task_3.task_id] = sample_task_3
        self.next_task_number = 4
    
    def create_task(self, task_data: Dict[str, Any]) -> str:
        """Create a new schedule task"""
        task_id = f"task-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        task_number = f"HTD-T-{self.next_task_number:03d}"
        
        task_data.update({
            "task_id": task_id,
            "task_number": task_number,
            "status": TaskStatus.NOT_STARTED,
            "percent_complete": 0.0,
            "work_completed": 0.0,
            "work_remaining": task_data.get("duration_days", 1),
            "actual_cost": 0.0,
            "cost_variance": 0.0,
            "resources": [],
            "dependencies": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        task_data["task_type"] = TaskType(task_data["task_type"])
        task_data["status"] = TaskStatus(task_data["status"])
        task_data["priority"] = TaskPriority(task_data["priority"])
        
        task = ScheduleTask(**task_data)
        self.tasks[task_id] = task
        self.next_task_number += 1
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[ScheduleTask]:
        """Get a specific task"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[ScheduleTask]:
        """Get all tasks sorted by planned start date"""
        return sorted(self.tasks.values(),
                     key=lambda t: t.planned_start_date)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[ScheduleTask]:
        """Get tasks by status"""
        return [task for task in self.tasks.values() if task.status == status]
    
    def get_tasks_by_phase(self, phase: str) -> List[ScheduleTask]:
        """Get tasks by project phase"""
        return [task for task in self.tasks.values() if task.phase == phase]
    
    def update_task_progress(self, task_id: str, percent_complete: float) -> bool:
        """Update task progress"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.percent_complete = min(100.0, max(0.0, percent_complete))
        task.work_completed = (task.percent_complete / 100.0) * task.duration_days
        task.work_remaining = task.duration_days - task.work_completed
        
        # Update status based on progress
        if task.percent_complete == 0:
            task.status = TaskStatus.NOT_STARTED
        elif task.percent_complete == 100:
            task.status = TaskStatus.COMPLETED
            if not task.actual_end_date:
                task.actual_end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            task.status = TaskStatus.IN_PROGRESS
            if not task.actual_start_date:
                task.actual_start_date = datetime.now().strftime('%Y-%m-%d')
        
        task.updated_at = datetime.now().isoformat()
        return True
    
    def generate_schedule_metrics(self) -> Dict[str, Any]:
        """Generate schedule performance metrics"""
        tasks = list(self.tasks.values())
        
        if not tasks:
            return {}
        
        total_tasks = len(tasks)
        
        # Status counts
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = len([t for t in tasks if t.status == status])
        
        # Priority counts
        priority_counts = {}
        for priority in TaskPriority:
            priority_counts[priority.value] = len([t for t in tasks if t.priority == priority])
        
        # Progress metrics
        avg_progress = sum(t.percent_complete for t in tasks) / total_tasks if total_tasks > 0 else 0
        
        # Schedule performance
        overdue_tasks = len([t for t in tasks if t.is_overdue()])
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
        
        # Cost metrics
        total_budgeted = sum(t.budgeted_cost for t in tasks)
        total_actual = sum(t.actual_cost for t in tasks)
        cost_variance = total_actual - total_budgeted
        
        return {
            "total_tasks": total_tasks,
            "status_breakdown": status_counts,
            "priority_breakdown": priority_counts,
            "average_progress": round(avg_progress, 1),
            "overdue_tasks": overdue_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0,
            "total_budgeted_cost": total_budgeted,
            "total_actual_cost": total_actual,
            "cost_variance": cost_variance,
            "on_time_performance": round(((total_tasks - overdue_tasks) / total_tasks * 100), 1) if total_tasks > 0 else 100
        }

# Global instance for use across the application
scheduling_manager = SchedulingManager()