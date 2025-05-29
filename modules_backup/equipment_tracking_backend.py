"""
Highland Tower Development - Equipment Tracking Backend
Enterprise-grade equipment and asset management with maintenance tracking.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class EquipmentStatus(Enum):
    ACTIVE = "Active"
    MAINTENANCE = "Under Maintenance"
    IDLE = "Idle"
    OUT_OF_SERVICE = "Out of Service"
    RENTED = "Rented Out"
    RETURNED = "Returned"

class EquipmentCategory(Enum):
    HEAVY_MACHINERY = "Heavy Machinery"
    CONSTRUCTION_TOOLS = "Construction Tools"
    SAFETY_EQUIPMENT = "Safety Equipment"
    MEASURING_INSTRUMENTS = "Measuring Instruments"
    LIFTING_EQUIPMENT = "Lifting Equipment"
    VEHICLES = "Vehicles"
    GENERATORS = "Generators & Power"
    SCAFFOLDING = "Scaffolding"

class MaintenanceType(Enum):
    PREVENTIVE = "Preventive"
    CORRECTIVE = "Corrective"
    EMERGENCY = "Emergency"
    INSPECTION = "Inspection"

@dataclass
class MaintenanceRecord:
    """Equipment maintenance record"""
    maintenance_id: str
    maintenance_date: str
    maintenance_type: MaintenanceType
    description: str
    performed_by: str
    cost: float
    parts_replaced: List[str]
    next_service_date: Optional[str]
    notes: str

@dataclass
class UsageRecord:
    """Equipment usage tracking record"""
    usage_id: str
    start_date: str
    end_date: Optional[str]
    operator: str
    location: str
    project_phase: str
    hours_used: float
    fuel_consumed: float
    notes: str

@dataclass
class Equipment:
    """Complete equipment record"""
    equipment_id: str
    equipment_code: str
    name: str
    description: str
    category: EquipmentCategory
    status: EquipmentStatus
    
    # Equipment details
    manufacturer: str
    model: str
    serial_number: str
    year_manufactured: int
    
    # Specifications
    capacity: str
    weight: str
    dimensions: str
    power_rating: str
    fuel_type: str
    
    # Financial
    purchase_cost: float
    current_value: float
    rental_rate_daily: float
    depreciation_rate: float
    
    # Location and assignment
    current_location: str
    assigned_to: str
    project_assignment: str
    
    # Operational
    total_hours: float
    hours_this_month: float
    fuel_efficiency: float
    
    # Maintenance
    last_service_date: Optional[str]
    next_service_date: Optional[str]
    service_interval_hours: int
    maintenance_records: List[MaintenanceRecord]
    
    # Usage tracking
    usage_records: List[UsageRecord]
    
    # Certification and compliance
    certifications_required: List[str]
    certifications_current: List[str]
    inspection_due_date: Optional[str]
    
    # Documentation
    manual_location: str
    warranty_expiry: Optional[str]
    insurance_policy: str
    
    # Notes and tracking
    procurement_notes: str
    operational_notes: str
    safety_notes: str
    
    # Workflow
    owned_rented: str  # "Owned" or "Rented"
    acquisition_date: str
    disposal_date: Optional[str]
    created_by: str
    updated_by: str
    created_at: str
    updated_at: str
    
    def calculate_utilization_rate(self) -> float:
        """Calculate equipment utilization rate"""
        if self.total_hours > 0:
            days_in_service = (datetime.now() - datetime.strptime(self.acquisition_date, '%Y-%m-%d')).days
            if days_in_service > 0:
                theoretical_max_hours = days_in_service * 8  # 8 hours per day theoretical max
                return min(100.0, (self.total_hours / theoretical_max_hours) * 100)
        return 0.0
    
    def needs_maintenance(self) -> bool:
        """Check if equipment needs maintenance"""
        if self.next_service_date:
            return datetime.strptime(self.next_service_date, '%Y-%m-%d').date() <= date.today()
        return False
    
    def is_overdue_inspection(self) -> bool:
        """Check if equipment inspection is overdue"""
        if self.inspection_due_date:
            return datetime.strptime(self.inspection_due_date, '%Y-%m-%d').date() < date.today()
        return False

class EquipmentManager:
    """Enterprise equipment tracking and management system"""
    
    def __init__(self):
        self.equipment: Dict[str, Equipment] = {}
        self.next_equipment_code = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample equipment data"""
        
        # Sample equipment 1 - Tower Crane
        sample_equipment_1 = Equipment(
            equipment_id="eq-001",
            equipment_code="HTD-EQ-001",
            name="Liebherr Tower Crane 280 EC-H",
            description="High-capacity tower crane for high-rise construction",
            category=EquipmentCategory.LIFTING_EQUIPMENT,
            status=EquipmentStatus.ACTIVE,
            manufacturer="Liebherr",
            model="280 EC-H",
            serial_number="LTM-2024-7829",
            year_manufactured=2023,
            capacity="12 tons at 50m radius",
            weight="65 tons",
            dimensions="Height: 180m, Jib: 65m",
            power_rating="132 kW",
            fuel_type="Electric",
            purchase_cost=0.0,  # Rented
            current_value=0.0,
            rental_rate_daily=2500.0,
            depreciation_rate=0.0,
            current_location="Highland Tower - Center Position",
            assigned_to="Highland Construction Crew",
            project_assignment="Highland Tower Development",
            total_hours=2840.5,
            hours_this_month=185.0,
            fuel_efficiency=0.0,  # Electric
            last_service_date="2025-05-01",
            next_service_date="2025-06-01",
            service_interval_hours=200,
            maintenance_records=[
                MaintenanceRecord(
                    maintenance_id="maint-001",
                    maintenance_date="2025-05-01",
                    maintenance_type=MaintenanceType.PREVENTIVE,
                    description="Monthly preventive maintenance and safety inspection",
                    performed_by="Liebherr Service Team",
                    cost=3500.0,
                    parts_replaced=["Wire rope inspection", "Hydraulic fluid change"],
                    next_service_date="2025-06-01",
                    notes="All systems operating within specifications"
                )
            ],
            usage_records=[
                UsageRecord(
                    usage_id="use-001",
                    start_date="2025-05-25",
                    end_date="2025-05-25",
                    operator="Mike Rodriguez - Certified Crane Operator",
                    location="Level 15 - Steel Installation",
                    project_phase="Structural Steel",
                    hours_used=8.5,
                    fuel_consumed=0.0,
                    notes="Steel beam installation - excellent performance"
                )
            ],
            certifications_required=["Annual Crane Inspection", "Monthly Safety Check", "Operator Certification"],
            certifications_current=["Annual Crane Inspection", "Monthly Safety Check"],
            inspection_due_date="2025-06-15",
            manual_location="Site Office - Equipment Folder",
            warranty_expiry="2026-12-31",
            insurance_policy="INS-LIFT-2024-001",
            procurement_notes="Rented from Liebherr - excellent reliability record",
            operational_notes="Primary crane for structural work - high utilization",
            safety_notes="Daily pre-operation inspection required",
            owned_rented="Rented",
            acquisition_date="2024-08-15",
            disposal_date=None,
            created_by="John Smith - Project Manager",
            updated_by="Mike Johnson - Equipment Manager",
            created_at="2024-08-15 09:00:00",
            updated_at="2025-05-25 17:30:00"
        )
        
        # Sample equipment 2 - Excavator
        sample_equipment_2 = Equipment(
            equipment_id="eq-002",
            equipment_code="HTD-EQ-002",
            name="CAT 320D Hydraulic Excavator",
            description="Mid-size excavator for general construction work",
            category=EquipmentCategory.HEAVY_MACHINERY,
            status=EquipmentStatus.ACTIVE,
            manufacturer="Caterpillar",
            model="320D",
            serial_number="CAT320D-2023-4567",
            year_manufactured=2023,
            capacity="20 tons operating weight",
            weight="20.2 tons",
            dimensions="Length: 9.5m, Width: 2.55m, Height: 3.1m",
            power_rating="105 kW (141 hp)",
            fuel_type="Diesel",
            purchase_cost=485000.0,
            current_value=425000.0,
            rental_rate_daily=850.0,
            depreciation_rate=12.0,  # 12% per year
            current_location="Site Perimeter - Equipment Yard",
            assigned_to="Site Excavation Crew",
            project_assignment="Highland Tower Development",
            total_hours=1450.2,
            hours_this_month=120.5,
            fuel_efficiency=15.2,  # L/hour
            last_service_date="2025-05-10",
            next_service_date="2025-07-10",
            service_interval_hours=250,
            maintenance_records=[
                MaintenanceRecord(
                    maintenance_id="maint-002",
                    maintenance_date="2025-05-10",
                    maintenance_type=MaintenanceType.PREVENTIVE,
                    description="500-hour service - engine oil, filters, hydraulic system check",
                    performed_by="CAT Service Center",
                    cost=2800.0,
                    parts_replaced=["Engine oil", "Oil filter", "Air filter", "Hydraulic filter"],
                    next_service_date="2025-07-10",
                    notes="Hydraulic system pressure tested - all systems normal"
                )
            ],
            usage_records=[
                UsageRecord(
                    usage_id="use-002",
                    start_date="2025-05-27",
                    end_date="2025-05-27",
                    operator="Carlos Martinez - Equipment Operator",
                    location="Building Perimeter - Utility Trenching",
                    project_phase="Site Utilities",
                    hours_used=7.5,
                    fuel_consumed=114.0,  # 7.5 * 15.2
                    notes="Utility trench excavation - good progress"
                )
            ],
            certifications_required=["Annual DOT Inspection", "Operator Certification"],
            certifications_current=["Annual DOT Inspection", "Operator Certification"],
            inspection_due_date="2026-02-15",
            manual_location="Site Office - Equipment Folder",
            warranty_expiry="2025-12-31",
            insurance_policy="INS-HVY-2024-002",
            procurement_notes="Purchased new - excellent condition and reliability",
            operational_notes="Versatile machine - used for various excavation tasks",
            safety_notes="Daily walk-around inspection required",
            owned_rented="Owned",
            acquisition_date="2023-09-01",
            disposal_date=None,
            created_by="Tom Brown - Equipment Manager",
            updated_by="Mike Johnson - Equipment Manager",
            created_at="2023-09-01 10:00:00",
            updated_at="2025-05-27 16:45:00"
        )
        
        # Sample equipment 3 - Safety Equipment (Needing Maintenance)
        sample_equipment_3 = Equipment(
            equipment_id="eq-003",
            equipment_code="HTD-EQ-003",
            name="Miller Fall Protection System",
            description="Comprehensive fall protection harnesses and lanyards",
            category=EquipmentCategory.SAFETY_EQUIPMENT,
            status=EquipmentStatus.MAINTENANCE,
            manufacturer="Miller Safety",
            model="Titan II",
            serial_number="MST-2024-FPS-15",
            year_manufactured=2024,
            capacity="140 kg per harness",
            weight="2.1 kg per set",
            dimensions="Adjustable sizing",
            power_rating="N/A",
            fuel_type="N/A",
            purchase_cost=15600.0,  # 12 complete sets
            current_value=14200.0,
            rental_rate_daily=0.0,
            depreciation_rate=20.0,  # Higher for safety equipment
            current_location="Safety Equipment Storage",
            assigned_to="Highland Safety Team",
            project_assignment="Highland Tower Development",
            total_hours=0.0,  # Safety equipment tracked differently
            hours_this_month=0.0,
            fuel_efficiency=0.0,
            last_service_date="2025-03-15",
            next_service_date="2025-05-28",  # Overdue
            service_interval_hours=0,  # Time-based maintenance
            maintenance_records=[
                MaintenanceRecord(
                    maintenance_id="maint-003",
                    maintenance_date="2025-03-15",
                    maintenance_type=MaintenanceType.INSPECTION,
                    description="Quarterly safety equipment inspection",
                    performed_by="Highland Safety Officer",
                    cost=450.0,
                    parts_replaced=["2 damaged D-rings", "1 worn lanyard"],
                    next_service_date="2025-05-28",
                    notes="2 harnesses need replacement - showing wear"
                )
            ],
            usage_records=[],
            certifications_required=["ANSI Z359 Compliance", "Monthly Inspection"],
            certifications_current=["ANSI Z359 Compliance"],
            inspection_due_date="2025-05-28",
            manual_location="Safety Office",
            warranty_expiry="2027-01-31",
            insurance_policy="INS-SAF-2024-003",
            procurement_notes="Critical safety equipment - no compromise on quality",
            operational_notes="12 complete fall protection systems for high-rise work",
            safety_notes="CRITICAL: Inspect before each use - zero tolerance for defects",
            owned_rented="Owned",
            acquisition_date="2024-01-15",
            disposal_date=None,
            created_by="Sarah Wilson - Safety Manager",
            updated_by="Sarah Wilson - Safety Manager",
            created_at="2024-01-15 08:00:00",
            updated_at="2025-05-25 14:00:00"
        )
        
        self.equipment[sample_equipment_1.equipment_id] = sample_equipment_1
        self.equipment[sample_equipment_2.equipment_id] = sample_equipment_2
        self.equipment[sample_equipment_3.equipment_id] = sample_equipment_3
        self.next_equipment_code = 4
    
    def create_equipment(self, equipment_data: Dict[str, Any]) -> str:
        """Create a new equipment record"""
        equipment_id = f"eq-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        equipment_code = f"HTD-EQ-{self.next_equipment_code:03d}"
        
        equipment_data.update({
            "equipment_id": equipment_id,
            "equipment_code": equipment_code,
            "status": EquipmentStatus.IDLE,
            "total_hours": 0.0,
            "hours_this_month": 0.0,
            "maintenance_records": [],
            "usage_records": [],
            "certifications_current": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        equipment_data["category"] = EquipmentCategory(equipment_data["category"])
        equipment_data["status"] = EquipmentStatus(equipment_data["status"])
        
        equipment = Equipment(**equipment_data)
        self.equipment[equipment_id] = equipment
        self.next_equipment_code += 1
        
        return equipment_id
    
    def get_equipment(self, equipment_id: str) -> Optional[Equipment]:
        """Get a specific equipment"""
        return self.equipment.get(equipment_id)
    
    def get_all_equipment(self) -> List[Equipment]:
        """Get all equipment sorted by category and name"""
        return sorted(self.equipment.values(),
                     key=lambda e: (e.category.value, e.name))
    
    def get_equipment_by_status(self, status: EquipmentStatus) -> List[Equipment]:
        """Get equipment by status"""
        return [eq for eq in self.equipment.values() if eq.status == status]
    
    def get_equipment_by_category(self, category: EquipmentCategory) -> List[Equipment]:
        """Get equipment by category"""
        return [eq for eq in self.equipment.values() if eq.category == category]
    
    def get_equipment_needing_maintenance(self) -> List[Equipment]:
        """Get equipment that needs maintenance"""
        return [eq for eq in self.equipment.values() if eq.needs_maintenance()]
    
    def get_overdue_inspections(self) -> List[Equipment]:
        """Get equipment with overdue inspections"""
        return [eq for eq in self.equipment.values() if eq.is_overdue_inspection()]
    
    def update_equipment_status(self, equipment_id: str, status: EquipmentStatus) -> bool:
        """Update equipment status"""
        equipment = self.equipment.get(equipment_id)
        if not equipment:
            return False
        
        equipment.status = status
        equipment.updated_at = datetime.now().isoformat()
        return True
    
    def add_maintenance_record(self, equipment_id: str, maintenance_data: Dict[str, Any]) -> bool:
        """Add a maintenance record to equipment"""
        equipment = self.equipment.get(equipment_id)
        if not equipment:
            return False
        
        maintenance_id = f"maint-{len(equipment.maintenance_records) + 1:03d}"
        maintenance_data.update({"maintenance_id": maintenance_id})
        
        # Convert enum
        maintenance_data["maintenance_type"] = MaintenanceType(maintenance_data["maintenance_type"])
        
        maintenance = MaintenanceRecord(**maintenance_data)
        equipment.maintenance_records.append(maintenance)
        
        # Update service dates
        equipment.last_service_date = maintenance.maintenance_date
        if maintenance.next_service_date:
            equipment.next_service_date = maintenance.next_service_date
        
        equipment.updated_at = datetime.now().isoformat()
        return True
    
    def add_usage_record(self, equipment_id: str, usage_data: Dict[str, Any]) -> bool:
        """Add a usage record to equipment"""
        equipment = self.equipment.get(equipment_id)
        if not equipment:
            return False
        
        usage_id = f"use-{len(equipment.usage_records) + 1:03d}"
        usage_data.update({"usage_id": usage_id})
        
        usage = UsageRecord(**usage_data)
        equipment.usage_records.append(usage)
        
        # Update total hours
        equipment.total_hours += usage.hours_used
        equipment.hours_this_month += usage.hours_used
        
        equipment.updated_at = datetime.now().isoformat()
        return True
    
    def generate_equipment_metrics(self) -> Dict[str, Any]:
        """Generate equipment management metrics"""
        equipment_list = list(self.equipment.values())
        
        if not equipment_list:
            return {}
        
        total_equipment = len(equipment_list)
        
        # Status counts
        status_counts = {}
        for status in EquipmentStatus:
            status_counts[status.value] = len([eq for eq in equipment_list if eq.status == status])
        
        # Category counts
        category_counts = {}
        for category in EquipmentCategory:
            category_counts[category.value] = len([eq for eq in equipment_list if eq.category == category])
        
        # Financial metrics
        total_asset_value = sum(eq.current_value for eq in equipment_list)
        monthly_rental_cost = sum(eq.rental_rate_daily * 30 for eq in equipment_list if eq.owned_rented == "Rented")
        
        # Utilization metrics
        equipment_with_hours = [eq for eq in equipment_list if eq.total_hours > 0]
        avg_utilization = sum(eq.calculate_utilization_rate() for eq in equipment_with_hours) / len(equipment_with_hours) if equipment_with_hours else 0
        
        # Maintenance metrics
        maintenance_needed = len(self.get_equipment_needing_maintenance())
        overdue_inspections = len(self.get_overdue_inspections())
        
        # Usage metrics
        total_hours_this_month = sum(eq.hours_this_month for eq in equipment_list)
        
        return {
            "total_equipment": total_equipment,
            "status_breakdown": status_counts,
            "category_breakdown": category_counts,
            "total_asset_value": total_asset_value,
            "monthly_rental_cost": monthly_rental_cost,
            "average_utilization": round(avg_utilization, 1),
            "maintenance_needed": maintenance_needed,
            "overdue_inspections": overdue_inspections,
            "total_hours_this_month": total_hours_this_month,
            "active_equipment": status_counts.get("Active", 0),
            "equipment_in_maintenance": status_counts.get("Under Maintenance", 0)
        }

# Global instance for use across the application
equipment_manager = EquipmentManager()