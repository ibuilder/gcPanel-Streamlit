"""
Highland Tower Development - Material Management Backend
Enterprise-grade material inventory tracking with procurement and delivery management.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class MaterialStatus(Enum):
    PLANNED = "Planned"
    ORDERED = "Ordered"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    INSTALLED = "Installed"
    RETURNED = "Returned"

class MaterialCategory(Enum):
    CONCRETE = "Concrete & Masonry"
    STEEL = "Structural Steel"
    LUMBER = "Lumber & Wood"
    INSULATION = "Insulation"
    ROOFING = "Roofing Materials"
    ELECTRICAL = "Electrical"
    PLUMBING = "Plumbing"
    HVAC = "HVAC Materials"
    FINISHES = "Finishes"
    HARDWARE = "Hardware & Fasteners"

class UnitType(Enum):
    CUBIC_YARD = "CY"
    TON = "TON"
    LINEAR_FOOT = "LF"
    SQUARE_FOOT = "SF"
    EACH = "EA"
    GALLON = "GAL"
    POUND = "LB"
    BUNDLE = "BDL"

@dataclass
class MaterialDelivery:
    """Material delivery record"""
    delivery_id: str
    delivery_date: str
    quantity_delivered: float
    delivery_ticket: str
    received_by: str
    condition_notes: str
    photos_attached: List[str]

@dataclass
class MaterialUsage:
    """Material usage/consumption record"""
    usage_id: str
    usage_date: str
    quantity_used: float
    location_used: str
    used_by: str
    work_order: str
    notes: str

@dataclass
class Material:
    """Complete material record"""
    material_id: str
    material_code: str
    name: str
    description: str
    category: MaterialCategory
    status: MaterialStatus
    
    # Specifications
    specification: str
    grade_quality: str
    size_dimensions: str
    color_finish: str
    manufacturer: str
    model_part_number: str
    
    # Quantities
    unit_type: UnitType
    quantity_ordered: float
    quantity_delivered: float
    quantity_used: float
    quantity_remaining: float
    minimum_stock_level: float
    
    # Location tracking
    storage_location: str
    delivery_location: str
    current_location: str
    
    # Procurement
    supplier_name: str
    supplier_contact: str
    purchase_order: str
    unit_cost: float
    total_cost: float
    
    # Schedule
    required_date: str
    order_date: Optional[str]
    expected_delivery: Optional[str]
    actual_delivery: Optional[str]
    
    # Quality & compliance
    certifications_required: List[str]
    certifications_received: List[str]
    test_reports: List[str]
    compliance_notes: str
    
    # Project details
    project_name: str
    work_package: str
    phase: str
    drawing_reference: str
    
    # Deliveries and usage
    deliveries: List[MaterialDelivery]
    usage_records: List[MaterialUsage]
    
    # Notes and tracking
    procurement_notes: str
    quality_notes: str
    storage_requirements: str
    
    # Workflow
    requested_by: str
    approved_by: Optional[str]
    created_by: str
    created_at: str
    updated_at: str
    
    def calculate_usage_rate(self) -> float:
        """Calculate material usage rate"""
        if self.quantity_delivered > 0:
            return (self.quantity_used / self.quantity_delivered) * 100
        return 0.0
    
    def is_low_stock(self) -> bool:
        """Check if material is below minimum stock level"""
        return self.quantity_remaining <= self.minimum_stock_level
    
    def calculate_waste_percentage(self) -> float:
        """Calculate waste percentage"""
        if self.quantity_delivered > 0:
            waste = self.quantity_delivered - self.quantity_used
            return (waste / self.quantity_delivered) * 100
        return 0.0

class MaterialManager:
    """Enterprise material management system"""
    
    def __init__(self):
        self.materials: Dict[str, Material] = {}
        self.next_material_code = 1
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample material data"""
        
        # Sample material 1 - Concrete
        sample_material_1 = Material(
            material_id="mat-001",
            material_code="HTD-MAT-001",
            name="Ready-Mix Concrete 4000 PSI",
            description="High-strength concrete for structural elements",
            category=MaterialCategory.CONCRETE,
            status=MaterialStatus.DELIVERED,
            specification="ASTM C94, 4000 PSI @ 28 days",
            grade_quality="4000 PSI",
            size_dimensions="N/A",
            color_finish="Standard Gray",
            manufacturer="City Concrete Supply",
            model_part_number="4000-STD",
            unit_type=UnitType.CUBIC_YARD,
            quantity_ordered=450.0,
            quantity_delivered=445.0,
            quantity_used=380.0,
            quantity_remaining=65.0,
            minimum_stock_level=20.0,
            storage_location="On-site batch plant",
            delivery_location="Level 15 pour location",
            current_location="Ready for use",
            supplier_name="City Concrete Supply",
            supplier_contact="Mike Johnson - (555) 234-5678",
            purchase_order="PO-HTD-2024-158",
            unit_cost=185.0,
            total_cost=83250.0,
            required_date="2025-05-20",
            order_date="2025-05-15",
            expected_delivery="2025-05-20",
            actual_delivery="2025-05-20",
            certifications_required=["ASTM C94 Compliance", "DOT Approval"],
            certifications_received=["ASTM C94 Compliance", "DOT Approval"],
            test_reports=["28-day strength test - Pass"],
            compliance_notes="All certifications current and valid",
            project_name="Highland Tower Development",
            work_package="Structure",
            phase="Level 15 Construction",
            drawing_reference="S-301, S-302",
            deliveries=[
                MaterialDelivery(
                    delivery_id="del-001",
                    delivery_date="2025-05-20",
                    quantity_delivered=445.0,
                    delivery_ticket="CC-20250520-001",
                    received_by="Site Supervisor",
                    condition_notes="Good condition, no issues",
                    photos_attached=["delivery_001.jpg"]
                )
            ],
            usage_records=[
                MaterialUsage(
                    usage_id="use-001",
                    usage_date="2025-05-25",
                    quantity_used=380.0,
                    location_used="Level 15 slab",
                    used_by="Highland Construction Crew",
                    work_order="WO-L15-SLAB",
                    notes="Pour completed successfully"
                )
            ],
            procurement_notes="Reliable supplier with good quality control",
            quality_notes="Consistent mix quality, meets all specifications",
            storage_requirements="Use within 90 minutes of batching",
            requested_by="John Smith - Project Manager",
            approved_by="Sarah Wilson - Site Engineer",
            created_by="Tom Brown - Materials Coordinator",
            created_at="2025-05-10 09:00:00",
            updated_at="2025-05-25 16:30:00"
        )
        
        # Sample material 2 - Structural Steel
        sample_material_2 = Material(
            material_id="mat-002",
            material_code="HTD-MAT-002",
            name="Structural Steel W14x30 Beams",
            description="Wide flange steel beams for structural frame",
            category=MaterialCategory.STEEL,
            status=MaterialStatus.INSTALLED,
            specification="ASTM A992 Grade 50",
            grade_quality="Grade 50",
            size_dimensions="W14x30",
            color_finish="Mill finish",
            manufacturer="Nucor Steel",
            model_part_number="W14x30-A992",
            unit_type=UnitType.LINEAR_FOOT,
            quantity_ordered=2400.0,
            quantity_delivered=2400.0,
            quantity_used=2280.0,
            quantity_remaining=120.0,
            minimum_stock_level=50.0,
            storage_location="Laydown Yard A",
            delivery_location="Tower crane staging",
            current_location="Levels 11-15",
            supplier_name="Steel Fabricators Inc.",
            supplier_contact="Lisa Chen - (555) 345-6789",
            purchase_order="PO-HTD-2024-142",
            unit_cost=45.0,
            total_cost=108000.0,
            required_date="2025-04-15",
            order_date="2025-03-01",
            expected_delivery="2025-04-15",
            actual_delivery="2025-04-12",
            certifications_required=["Mill Test Certificate", "AWS Welding Certification"],
            certifications_received=["Mill Test Certificate", "AWS Welding Certification"],
            test_reports=["Tensile strength test - Pass", "Chemical analysis - Pass"],
            compliance_notes="All AISC requirements met",
            project_name="Highland Tower Development",
            work_package="Structure",
            phase="Steel Frame Installation",
            drawing_reference="S-201, S-202, S-203",
            deliveries=[
                MaterialDelivery(
                    delivery_id="del-002",
                    delivery_date="2025-04-12",
                    quantity_delivered=2400.0,
                    delivery_ticket="SF-20250412-001",
                    received_by="Steel Crew Foreman",
                    condition_notes="Excellent condition, properly marked",
                    photos_attached=["steel_delivery_001.jpg", "steel_delivery_002.jpg"]
                )
            ],
            usage_records=[
                MaterialUsage(
                    usage_id="use-002",
                    usage_date="2025-05-15",
                    quantity_used=2280.0,
                    location_used="Levels 11-15 frame",
                    used_by="Steel Fabricators Inc.",
                    work_order="WO-STEEL-L11-15",
                    notes="Installation 95% complete"
                )
            ],
            procurement_notes="Premium supplier with excellent fabrication quality",
            quality_notes="Perfect dimensional accuracy, superior welds",
            storage_requirements="Keep dry, protect from corrosion",
            requested_by="John Smith - Project Manager",
            approved_by="Sarah Wilson - Structural Engineer",
            created_by="Tom Brown - Materials Coordinator",
            created_at="2025-02-15 10:00:00",
            updated_at="2025-05-15 14:00:00"
        )
        
        # Sample material 3 - HVAC Equipment (Pending)
        sample_material_3 = Material(
            material_id="mat-003",
            material_code="HTD-MAT-003",
            name="Rooftop HVAC Units 50-Ton",
            description="High-efficiency rooftop HVAC units for building climate control",
            category=MaterialCategory.HVAC,
            status=MaterialStatus.ORDERED,
            specification="AHRI certified, 16 SEER, gas heat",
            grade_quality="Premium efficiency",
            size_dimensions="120\" x 60\" x 48\"",
            color_finish="Weathered steel",
            manufacturer="Carrier",
            model_part_number="RTU-50HC-16",
            unit_type=UnitType.EACH,
            quantity_ordered=8.0,
            quantity_delivered=0.0,
            quantity_used=0.0,
            quantity_remaining=0.0,
            minimum_stock_level=1.0,
            storage_location="TBD - Rooftop staging",
            delivery_location="Rooftop crane access",
            current_location="Manufacturer facility",
            supplier_name="HVAC Solutions LLC",
            supplier_contact="Robert Martinez - (555) 456-7890",
            purchase_order="PO-HTD-2024-189",
            unit_cost=28500.0,
            total_cost=228000.0,
            required_date="2025-07-01",
            order_date="2025-05-20",
            expected_delivery="2025-06-15",
            actual_delivery=None,
            certifications_required=["AHRI Certification", "Energy Star Rating"],
            certifications_received=["AHRI Certification"],
            test_reports=["Factory performance test - Scheduled"],
            compliance_notes="Energy Star certification pending",
            project_name="Highland Tower Development",
            work_package="MEP Systems",
            phase="HVAC Installation",
            drawing_reference="M-401, M-402",
            deliveries=[],
            usage_records=[],
            procurement_notes="Lead time extended due to high efficiency requirements",
            quality_notes="Top-tier manufacturer with excellent warranty",
            storage_requirements="Protect from weather, crane access required",
            requested_by="Tom Brown - MEP Manager",
            approved_by="John Smith - Project Manager",
            created_by="Lisa Wong - Procurement",
            created_at="2025-05-20 11:00:00",
            updated_at="2025-05-20 11:00:00"
        )
        
        self.materials[sample_material_1.material_id] = sample_material_1
        self.materials[sample_material_2.material_id] = sample_material_2
        self.materials[sample_material_3.material_id] = sample_material_3
        self.next_material_code = 4
    
    def create_material(self, material_data: Dict[str, Any]) -> str:
        """Create a new material record"""
        material_id = f"mat-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        material_code = f"HTD-MAT-{self.next_material_code:03d}"
        
        material_data.update({
            "material_id": material_id,
            "material_code": material_code,
            "status": MaterialStatus.PLANNED,
            "quantity_delivered": 0.0,
            "quantity_used": 0.0,
            "quantity_remaining": material_data.get("quantity_ordered", 0.0),
            "certifications_received": [],
            "test_reports": [],
            "deliveries": [],
            "usage_records": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        material_data["category"] = MaterialCategory(material_data["category"])
        material_data["status"] = MaterialStatus(material_data["status"])
        material_data["unit_type"] = UnitType(material_data["unit_type"])
        
        material = Material(**material_data)
        self.materials[material_id] = material
        self.next_material_code += 1
        
        return material_id
    
    def get_material(self, material_id: str) -> Optional[Material]:
        """Get a specific material"""
        return self.materials.get(material_id)
    
    def get_all_materials(self) -> List[Material]:
        """Get all materials sorted by category and name"""
        return sorted(self.materials.values(),
                     key=lambda m: (m.category.value, m.name))
    
    def get_materials_by_status(self, status: MaterialStatus) -> List[Material]:
        """Get materials by status"""
        return [material for material in self.materials.values() if material.status == status]
    
    def get_materials_by_category(self, category: MaterialCategory) -> List[Material]:
        """Get materials by category"""
        return [material for material in self.materials.values() if material.category == category]
    
    def get_low_stock_materials(self) -> List[Material]:
        """Get materials below minimum stock level"""
        return [material for material in self.materials.values() if material.is_low_stock()]
    
    def update_material_status(self, material_id: str, status: MaterialStatus) -> bool:
        """Update material status"""
        material = self.materials.get(material_id)
        if not material:
            return False
        
        material.status = status
        material.updated_at = datetime.now().isoformat()
        return True
    
    def add_delivery(self, material_id: str, delivery_data: Dict[str, Any]) -> bool:
        """Add a delivery record to material"""
        material = self.materials.get(material_id)
        if not material:
            return False
        
        delivery_id = f"del-{len(material.deliveries) + 1:03d}"
        delivery_data.update({"delivery_id": delivery_id})
        
        delivery = MaterialDelivery(**delivery_data)
        material.deliveries.append(delivery)
        
        # Update quantities
        material.quantity_delivered += delivery.quantity_delivered
        material.quantity_remaining = material.quantity_delivered - material.quantity_used
        
        # Update status
        if material.status == MaterialStatus.ORDERED:
            material.status = MaterialStatus.DELIVERED
        
        material.updated_at = datetime.now().isoformat()
        return True
    
    def add_usage(self, material_id: str, usage_data: Dict[str, Any]) -> bool:
        """Add a usage record to material"""
        material = self.materials.get(material_id)
        if not material:
            return False
        
        usage_id = f"use-{len(material.usage_records) + 1:03d}"
        usage_data.update({"usage_id": usage_id})
        
        usage = MaterialUsage(**usage_data)
        material.usage_records.append(usage)
        
        # Update quantities
        material.quantity_used += usage.quantity_used
        material.quantity_remaining = material.quantity_delivered - material.quantity_used
        
        material.updated_at = datetime.now().isoformat()
        return True
    
    def generate_material_metrics(self) -> Dict[str, Any]:
        """Generate material management metrics"""
        materials = list(self.materials.values())
        
        if not materials:
            return {}
        
        total_materials = len(materials)
        
        # Status counts
        status_counts = {}
        for status in MaterialStatus:
            status_counts[status.value] = len([m for m in materials if m.status == status])
        
        # Category counts
        category_counts = {}
        for category in MaterialCategory:
            category_counts[category.value] = len([m for m in materials if m.category == category])
        
        # Cost metrics
        total_cost = sum(m.total_cost for m in materials)
        
        # Stock metrics
        low_stock_count = len(self.get_low_stock_materials())
        
        # Usage metrics
        materials_with_usage = [m for m in materials if m.quantity_used > 0]
        avg_usage_rate = sum(m.calculate_usage_rate() for m in materials_with_usage) / len(materials_with_usage) if materials_with_usage else 0
        
        # Waste analysis
        materials_with_deliveries = [m for m in materials if m.quantity_delivered > 0]
        avg_waste = sum(m.calculate_waste_percentage() for m in materials_with_deliveries) / len(materials_with_deliveries) if materials_with_deliveries else 0
        
        return {
            "total_materials": total_materials,
            "status_breakdown": status_counts,
            "category_breakdown": category_counts,
            "total_project_cost": total_cost,
            "low_stock_materials": low_stock_count,
            "average_usage_rate": round(avg_usage_rate, 1),
            "average_waste_percentage": round(avg_waste, 1),
            "delivered_materials": status_counts.get("Delivered", 0),
            "pending_deliveries": status_counts.get("Ordered", 0) + status_counts.get("In Transit", 0)
        }

# Global instance for use across the application
material_manager = MaterialManager()