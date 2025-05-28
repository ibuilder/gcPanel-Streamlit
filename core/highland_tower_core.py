"""
Highland Tower Development - Core System Architecture
Unified constructor classes and relational framework for all 25 modules.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, date
from abc import ABC, abstractmethod
import json
import uuid

# Highland Tower Project Information - Core Data
@dataclass
class HighlandTowerProject:
    """Core Highland Tower Development project information"""
    project_id: str = "HTD-2024-001"
    project_name: str = "Highland Tower Development"
    project_value: float = 45500000.0
    project_location: str = "Downtown Highland District"
    project_size: str = "168,500 sq ft"
    floors: str = "15 stories above ground, 2 below"
    units: str = "120 residential + 8 retail"
    client: str = "Highland Properties LLC"
    project_manager: str = "John Smith"
    start_date: str = "2024-01-15"
    planned_completion: str = "2025-11-23"
    current_progress: float = 78.5
    schedule_performance_index: float = 1.05
    cost_performance_index: float = 1.02
    safety_rating: float = 97.2
    
    def get_project_context(self) -> Dict[str, Any]:
        """Get complete project context for module integration"""
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "project_value": self.project_value,
            "current_progress": self.current_progress,
            "spi": self.schedule_performance_index,
            "cpi": self.cost_performance_index,
            "safety_rating": self.safety_rating
        }

# Base Module Class for all Highland Tower modules
class HighlandTowerModule(ABC):
    """Base class for all Highland Tower Development modules"""
    
    def __init__(self, module_name: str, project: HighlandTowerProject):
        self.module_name = module_name
        self.project = project
        self.module_id = f"HTD-{module_name.upper()}-{str(uuid.uuid4())[:8]}"
        self.created_at = datetime.now().isoformat()
        self.data_store: Dict[str, Any] = {}
        self.related_modules: List[str] = []
        self.validation_rules: Dict[str, Any] = {}
        
    @abstractmethod
    def initialize_module_data(self):
        """Initialize module-specific data"""
        pass
    
    @abstractmethod
    def get_module_metrics(self) -> Dict[str, Any]:
        """Get module performance metrics"""
        pass
    
    def add_module_relation(self, target_module: str, relation_type: str):
        """Add relationship to another module"""
        if target_module not in self.related_modules:
            self.related_modules.append(target_module)
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate data against module rules"""
        for field, rules in self.validation_rules.items():
            if field in data:
                value = data[field]
                if "required" in rules and rules["required"] and not value:
                    return False
                if "type" in rules and not isinstance(value, rules["type"]):
                    return False
        return True

# Highland Tower Data Manager - Central data coordination
class HighlandTowerDataManager:
    """Central data manager for Highland Tower Development platform"""
    
    def __init__(self):
        self.project = HighlandTowerProject()
        self.modules: Dict[str, HighlandTowerModule] = {}
        self.module_registry: Dict[str, type] = {}
        self.data_relationships: Dict[str, List[str]] = {}
        self.global_cache: Dict[str, Any] = {}
        
    def register_module(self, module_name: str, module_class: type):
        """Register a module class"""
        self.module_registry[module_name] = module_class
        
    def create_module(self, module_name: str) -> Optional[HighlandTowerModule]:
        """Create and initialize a module instance"""
        if module_name in self.module_registry:
            module_class = self.module_registry[module_name]
            module = module_class(module_name, self.project)
            module.initialize_module_data()
            self.modules[module_name] = module
            return module
        return None
    
    def get_module(self, module_name: str) -> Optional[HighlandTowerModule]:
        """Get a module instance"""
        if module_name not in self.modules:
            self.create_module(module_name)
        return self.modules.get(module_name)
    
    def sync_module_data(self, source_module: str, target_module: str, data_key: str, data_value: Any):
        """Sync data between modules"""
        source = self.get_module(source_module)
        target = self.get_module(target_module)
        
        if source and target:
            target.data_store[f"{source_module}_{data_key}"] = data_value
            
    def get_cross_module_data(self, requesting_module: str, data_keys: List[str]) -> Dict[str, Any]:
        """Get data from multiple modules for cross-module operations"""
        result = {}
        result["project_context"] = self.project.get_project_context()
        
        for module_name, module in self.modules.items():
            if module_name != requesting_module:
                for key in data_keys:
                    if key in module.data_store:
                        result[f"{module_name}_{key}"] = module.data_store[key]
        
        return result

# Specific Highland Tower Module Classes
class HighlandTowerCostManagement(HighlandTowerModule):
    """Cost Management module for Highland Tower Development"""
    
    def __init__(self, module_name: str, project: HighlandTowerProject):
        super().__init__(module_name, project)
        self.add_module_relation("change_orders", "bidirectional")
        self.add_module_relation("daily_reports", "receives_updates")
        self.add_module_relation("material_management", "receives_updates")
        self.add_module_relation("rfis", "receives_cost_impacts")
        
    def initialize_module_data(self):
        """Initialize Highland Tower cost management data"""
        self.data_store = {
            "total_budget": self.project.project_value,
            "spent_to_date": 30247800.0,
            "budget_variance": -2100000.0,  # $2.1M under budget
            "change_orders_total": 585000.0,
            "cost_performance_index": self.project.cost_performance_index,
            "budget_categories": [
                {"code": "01-0000", "name": "General Requirements", "budget": 2280000, "actual": 2100000},
                {"code": "03-0000", "name": "Concrete", "budget": 8750000, "actual": 8250000},
                {"code": "05-0000", "name": "Metals", "budget": 12400000, "actual": 10230000},
                {"code": "15-0000", "name": "MEP Systems", "budget": 15200000, "actual": 8740000},
                {"code": "07-0000", "name": "Exterior Envelope", "budget": 6870000, "actual": 3572400}
            ]
        }
        
    def get_module_metrics(self) -> Dict[str, Any]:
        """Get cost management metrics"""
        return {
            "total_budget": self.data_store["total_budget"],
            "spent_percentage": (self.data_store["spent_to_date"] / self.data_store["total_budget"]) * 100,
            "variance_amount": self.data_store["budget_variance"],
            "cpi": self.data_store["cost_performance_index"],
            "change_orders_count": 3,
            "under_budget_status": self.data_store["budget_variance"] < 0
        }

class HighlandTowerDailyReports(HighlandTowerModule):
    """Daily Reports module for Highland Tower Development"""
    
    def __init__(self, module_name: str, project: HighlandTowerProject):
        super().__init__(module_name, project)
        self.add_module_relation("cost_management", "provides_updates")
        self.add_module_relation("safety", "shares_incidents")
        self.add_module_relation("progress_photos", "references_photos")
        self.add_module_relation("weather", "includes_conditions")
        
    def initialize_module_data(self):
        """Initialize Highland Tower daily reports data"""
        self.data_store = {
            "total_reports": 156,
            "current_week_reports": 5,
            "average_crew_size": 89,
            "total_labor_hours": 1247,
            "weather_delays": 2,
            "safety_incidents": 0,
            "productivity_index": 1.15,
            "recent_activities": [
                "Level 13 structural steel erection completed",
                "MEP rough-in progress on Levels 9-11", 
                "Exterior skin installation ongoing",
                "Interior finishes started on Levels 1-3"
            ]
        }
        
    def get_module_metrics(self) -> Dict[str, Any]:
        """Get daily reports metrics"""
        return {
            "total_reports": self.data_store["total_reports"],
            "crew_productivity": self.data_store["productivity_index"],
            "safety_performance": "Excellent" if self.data_store["safety_incidents"] == 0 else "Needs Attention",
            "weather_impact": self.data_store["weather_delays"],
            "labor_efficiency": "Above Average"
        }

class HighlandTowerRFI(HighlandTowerModule):
    """RFI Management module for Highland Tower Development"""
    
    def __init__(self, module_name: str, project: HighlandTowerProject):
        super().__init__(module_name, project)
        self.add_module_relation("cost_management", "provides_cost_impacts")
        self.add_module_relation("scheduling", "affects_timeline")
        self.add_module_relation("quality_control", "design_clarifications")
        
    def initialize_module_data(self):
        """Initialize Highland Tower RFI data"""
        self.data_store = {
            "total_rfis": 23,
            "open_rfis": 5,
            "closed_rfis": 18,
            "average_response_time": 3.2,
            "cost_impact_total": 125000.0,
            "schedule_impact_days": 2,
            "rfi_categories": {
                "Design Clarification": 12,
                "Product Substitution": 6,
                "Field Condition": 3,
                "Code Compliance": 2
            }
        }
        
    def get_module_metrics(self) -> Dict[str, Any]:
        """Get RFI metrics"""
        return {
            "total_rfis": self.data_store["total_rfis"],
            "response_efficiency": "Excellent" if self.data_store["average_response_time"] < 5 else "Good",
            "cost_impact": self.data_store["cost_impact_total"],
            "schedule_impact": self.data_store["schedule_impact_days"],
            "closure_rate": (self.data_store["closed_rfis"] / self.data_store["total_rfis"]) * 100
        }

class HighlandTowerSafety(HighlandTowerModule):
    """Safety Management module for Highland Tower Development"""
    
    def __init__(self, module_name: str, project: HighlandTowerProject):
        super().__init__(module_name, project)
        self.add_module_relation("daily_reports", "receives_incidents")
        self.add_module_relation("quality_control", "safety_inspections")
        self.add_module_relation("training", "safety_training")
        
    def initialize_module_data(self):
        """Initialize Highland Tower safety data"""
        self.data_store = {
            "safety_rating": self.project.safety_rating,
            "incidents_ytd": 1,
            "near_misses": 3,
            "safety_meetings": 24,
            "training_hours": 1240,
            "osha_recordable": 0,
            "days_since_incident": 45,
            "safety_inspections": 89,
            "compliance_score": 98.5
        }
        
    def get_module_metrics(self) -> Dict[str, Any]:
        """Get safety metrics"""
        return {
            "overall_rating": self.data_store["safety_rating"],
            "incident_rate": "Excellent",
            "training_completion": "100%",
            "compliance_status": "Full Compliance",
            "days_without_incident": self.data_store["days_since_incident"]
        }

class HighlandTowerQualityControl(HighlandTowerModule):
    """Quality Control module for Highland Tower Development"""
    
    def __init__(self, module_name: str, project: HighlandTowerProject):
        super().__init__(module_name, project)
        self.add_module_relation("progress_photos", "receives_photos")
        self.add_module_relation("submittals", "material_approvals")
        self.add_module_relation("safety", "quality_safety_overlap")
        
    def initialize_module_data(self):
        """Initialize Highland Tower quality control data"""
        self.data_store = {
            "quality_score": 94.2,
            "inspections_completed": 234,
            "punch_list_items": 12,
            "rework_percentage": 1.8,
            "material_approvals": 156,
            "defects_per_unit": 0.3,
            "customer_satisfaction": 96.5,
            "quality_trend": "Improving"
        }
        
    def get_module_metrics(self) -> Dict[str, Any]:
        """Get quality control metrics"""
        return {
            "quality_score": self.data_store["quality_score"],
            "inspection_efficiency": "Excellent",
            "rework_rate": self.data_store["rework_percentage"],
            "punch_list_status": "Minimal Items",
            "overall_trend": self.data_store["quality_trend"]
        }

# Highland Tower Module Factory
class HighlandTowerModuleFactory:
    """Factory for creating Highland Tower Development modules"""
    
    @staticmethod
    def create_module(module_type: str, project: HighlandTowerProject) -> Optional[HighlandTowerModule]:
        """Create a specific module instance"""
        module_classes = {
            "cost_management": HighlandTowerCostManagement,
            "daily_reports": HighlandTowerDailyReports,
            "rfi_management": HighlandTowerRFI,
            "safety": HighlandTowerSafety,
            "quality_control": HighlandTowerQualityControl
        }
        
        if module_type in module_classes:
            return module_classes[module_type](module_type, project)
        return None

# Highland Tower Integration Manager
class HighlandTowerIntegrationManager:
    """Manages integration and data flow between all Highland Tower modules"""
    
    def __init__(self):
        self.project = HighlandTowerProject()
        self.data_manager = HighlandTowerDataManager()
        self.active_modules: Dict[str, HighlandTowerModule] = {}
        
    def initialize_all_modules(self):
        """Initialize all Highland Tower Development modules"""
        module_types = [
            "cost_management", "daily_reports", "rfi_management", 
            "safety", "quality_control"
        ]
        
        for module_type in module_types:
            module = HighlandTowerModuleFactory.create_module(module_type, self.project)
            if module:
                self.active_modules[module_type] = module
                
    def sync_cross_module_data(self):
        """Synchronize data across all modules"""
        # Cost Management receives updates from multiple modules
        if "cost_management" in self.active_modules and "daily_reports" in self.active_modules:
            daily_labor = self.active_modules["daily_reports"].data_store.get("total_labor_hours", 0)
            self.data_manager.sync_module_data("daily_reports", "cost_management", "labor_hours", daily_labor)
        
        # RFI cost impacts update cost management
        if "rfi_management" in self.active_modules and "cost_management" in self.active_modules:
            rfi_costs = self.active_modules["rfi_management"].data_store.get("cost_impact_total", 0)
            self.data_manager.sync_module_data("rfi_management", "cost_management", "rfi_impacts", rfi_costs)
            
    def get_integrated_dashboard_data(self) -> Dict[str, Any]:
        """Get integrated data for Highland Tower dashboard"""
        dashboard_data = {
            "project_info": self.project.get_project_context(),
            "module_metrics": {}
        }
        
        for module_name, module in self.active_modules.items():
            dashboard_data["module_metrics"][module_name] = module.get_module_metrics()
            
        return dashboard_data
    
    def create_module_relationship_map(self) -> Dict[str, List[str]]:
        """Create a map of module relationships"""
        relationship_map = {}
        for module_name, module in self.active_modules.items():
            relationship_map[module_name] = module.related_modules
        return relationship_map

# Global Highland Tower System Instance
highland_tower_system = HighlandTowerIntegrationManager()
highland_tower_system.initialize_all_modules()
highland_tower_system.sync_cross_module_data()