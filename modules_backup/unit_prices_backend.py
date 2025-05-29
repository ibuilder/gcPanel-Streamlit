"""
Highland Tower Development - Unit Prices Management Backend
Enterprise-grade unit pricing system for construction cost estimation and tracking.
"""

import json
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class PriceCategory(Enum):
    LABOR = "Labor"
    MATERIAL = "Material"
    EQUIPMENT = "Equipment"
    SUBCONTRACTOR = "Subcontractor"
    OVERHEAD = "Overhead"

class UnitType(Enum):
    SQUARE_FOOT = "SF"
    LINEAR_FOOT = "LF"
    CUBIC_YARD = "CY"
    EACH = "EA"
    LUMP_SUM = "LS"
    HOUR = "HR"
    TON = "TON"
    GALLON = "GAL"

class PriceStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PENDING_APPROVAL = "Pending Approval"
    EXPIRED = "Expired"

class PriceSource(Enum):
    VENDOR_QUOTE = "Vendor Quote"
    HISTORICAL_DATA = "Historical Data"
    MARKET_ANALYSIS = "Market Analysis"
    SUBCONTRACTOR_BID = "Subcontractor Bid"
    CATALOG_PRICE = "Catalog Price"

@dataclass
class PriceHistory:
    """Historical price data point"""
    date: str
    price: float
    source: str
    notes: str

@dataclass
class UnitPrice:
    """Complete unit price record"""
    price_id: str
    item_code: str
    description: str
    category: PriceCategory
    unit_type: UnitType
    status: PriceStatus
    
    # Pricing
    base_price: float
    labor_cost: float
    material_cost: float
    equipment_cost: float
    overhead_percentage: float
    profit_percentage: float
    total_price: float
    
    # Details
    specification: str
    vendor_name: str
    vendor_contact: str
    model_number: Optional[str]
    brand: Optional[str]
    
    # Validity
    effective_date: str
    expiration_date: Optional[str]
    price_source: PriceSource
    quote_reference: Optional[str]
    
    # Location and conditions
    location_factor: float
    minimum_quantity: int
    maximum_quantity: Optional[int]
    delivery_time_days: int
    payment_terms: str
    
    # Quality metrics
    quality_rating: float  # 1-5 scale
    reliability_score: float  # 1-5 scale
    past_performance: str
    
    # Price history
    price_history: List[PriceHistory]
    last_updated: str
    price_trend: str  # "Increasing", "Decreasing", "Stable"
    
    # Project application
    project_name: str
    work_package: str
    csi_code: Optional[str]
    
    # Notes
    pricing_notes: str
    special_conditions: str
    
    # Tracking
    created_by: str
    approved_by: Optional[str]
    created_at: str
    updated_at: str
    
    def calculate_total_price(self) -> float:
        """Calculate total price including overhead and profit"""
        subtotal = self.labor_cost + self.material_cost + self.equipment_cost
        overhead_amount = subtotal * (self.overhead_percentage / 100)
        profit_amount = (subtotal + overhead_amount) * (self.profit_percentage / 100)
        return subtotal + overhead_amount + profit_amount

@dataclass
class PriceComparison:
    """Price comparison between multiple sources"""
    comparison_id: str
    item_description: str
    comparison_date: str
    prices: List[UnitPrice]
    recommended_price_id: str
    savings_amount: float
    notes: str

class UnitPricesManager:
    """Enterprise unit prices management system"""
    
    def __init__(self):
        self.unit_prices: Dict[str, UnitPrice] = {}
        self.price_comparisons: Dict[str, PriceComparison] = {}
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample unit price data"""
        
        # Sample unit price 1 - Concrete
        sample_price_1 = UnitPrice(
            price_id="price-001",
            item_code="CONC-4000-CY",
            description="Ready-mix concrete, 4000 PSI, delivered and placed",
            category=PriceCategory.MATERIAL,
            unit_type=UnitType.CUBIC_YARD,
            status=PriceStatus.ACTIVE,
            base_price=185.00,
            labor_cost=45.00,
            material_cost=125.00,
            equipment_cost=15.00,
            overhead_percentage=12.0,
            profit_percentage=8.0,
            total_price=224.20,
            specification="ASTM C94, 4000 PSI @ 28 days, 4-6 inch slump",
            vendor_name="City Concrete Supply",
            vendor_contact="Mike Johnson - (555) 234-5678",
            model_number=None,
            brand="City Mix",
            effective_date="2025-05-01",
            expiration_date="2025-08-01",
            price_source=PriceSource.VENDOR_QUOTE,
            quote_reference="CCS-2025-HTD-001",
            location_factor=1.0,
            minimum_quantity=5,
            maximum_quantity=100,
            delivery_time_days=1,
            payment_terms="Net 30",
            quality_rating=4.5,
            reliability_score=4.8,
            past_performance="Excellent delivery record, consistent quality",
            price_history=[
                PriceHistory(
                    date="2025-01-01",
                    price=180.00,
                    source="Historical average",
                    notes="Q1 2025 pricing"
                ),
                PriceHistory(
                    date="2025-03-01",
                    price=182.50,
                    source="Market adjustment",
                    notes="Cement price increase"
                )
            ],
            last_updated="2025-05-01",
            price_trend="Increasing",
            project_name="Highland Tower Development",
            work_package="Structure",
            csi_code="03 30 00",
            pricing_notes="Includes pump truck for placement above 3rd floor",
            special_conditions="Weekend delivery available at 15% premium",
            created_by="Sarah Wilson - Estimator",
            approved_by="John Smith - Project Manager",
            created_at="2025-05-01 09:00:00",
            updated_at="2025-05-01 09:00:00"
        )
        
        # Sample unit price 2 - Steel framing
        sample_price_2 = UnitPrice(
            price_id="price-002",
            item_code="STEEL-W14-LF",
            description="Structural steel W14x30 beam, fabricated and erected",
            category=PriceCategory.SUBCONTRACTOR,
            unit_type=UnitType.LINEAR_FOOT,
            status=PriceStatus.ACTIVE,
            base_price=45.00,
            labor_cost=18.00,
            material_cost=22.00,
            equipment_cost=5.00,
            overhead_percentage=15.0,
            profit_percentage=10.0,
            total_price=56.25,
            specification="ASTM A992 Grade 50, shop fabricated, field erected",
            vendor_name="Steel Fabricators Inc.",
            vendor_contact="Lisa Chen - (555) 345-6789",
            model_number="W14x30",
            brand="Nucor",
            effective_date="2025-05-15",
            expiration_date="2025-07-15",
            price_source=PriceSource.SUBCONTRACTOR_BID,
            quote_reference="SFI-2025-HTD-002",
            location_factor=1.05,
            minimum_quantity=100,
            maximum_quantity=None,
            delivery_time_days=14,
            payment_terms="30% down, balance on delivery",
            quality_rating=4.8,
            reliability_score=4.6,
            past_performance="Excellent fabrication quality, on-time delivery",
            price_history=[
                PriceHistory(
                    date="2025-02-01",
                    price=42.00,
                    source="Previous project",
                    notes="Q1 2025 pricing"
                ),
                PriceHistory(
                    date="2025-04-01",
                    price=44.00,
                    source="Market update",
                    notes="Steel price increase"
                )
            ],
            last_updated="2025-05-15",
            price_trend="Increasing",
            project_name="Highland Tower Development",
            work_package="Structure",
            csi_code="05 12 00",
            pricing_notes="Includes shop drawings and engineering",
            special_conditions="Crane required for erection, not included",
            created_by="Tom Brown - Structural Estimator",
            approved_by="John Smith - Project Manager",
            created_at="2025-05-15 14:00:00",
            updated_at="2025-05-15 14:00:00"
        )
        
        # Sample unit price 3 - HVAC equipment
        sample_price_3 = UnitPrice(
            price_id="price-003",
            item_code="HVAC-RTU-50T-EA",
            description="Rooftop HVAC unit, 50 ton, high efficiency",
            category=PriceCategory.EQUIPMENT,
            unit_type=UnitType.EACH,
            status=PriceStatus.ACTIVE,
            base_price=28500.00,
            labor_cost=3500.00,
            material_cost=25000.00,
            equipment_cost=0.00,
            overhead_percentage=8.0,
            profit_percentage=12.0,
            total_price=34440.00,
            specification="AHRI certified, 16 SEER, gas heat, economizer",
            vendor_name="HVAC Solutions LLC",
            vendor_contact="Robert Martinez - (555) 456-7890",
            model_number="RTU-50HC-16",
            brand="Carrier",
            effective_date="2025-05-20",
            expiration_date="2025-08-20",
            price_source=PriceSource.VENDOR_QUOTE,
            quote_reference="HVAC-2025-HTD-003",
            location_factor=1.0,
            minimum_quantity=1,
            maximum_quantity=10,
            delivery_time_days=28,
            payment_terms="50% deposit, balance before shipment",
            quality_rating=4.7,
            reliability_score=4.9,
            past_performance="Premium equipment, excellent warranty support",
            price_history=[
                PriceHistory(
                    date="2025-01-15",
                    price=27500.00,
                    source="Previous quote",
                    notes="Early project pricing"
                ),
                PriceHistory(
                    date="2025-03-15",
                    price=28000.00,
                    source="Updated quote",
                    notes="Efficiency upgrade"
                )
            ],
            last_updated="2025-05-20",
            price_trend="Stable",
            project_name="Highland Tower Development",
            work_package="MEP Systems",
            csi_code="23 74 00",
            pricing_notes="Includes factory startup and commissioning",
            special_conditions="Crane required for installation, separate cost",
            created_by="Lisa Wong - MEP Estimator",
            approved_by="Tom Brown - MEP Manager",
            created_at="2025-05-20 11:00:00",
            updated_at="2025-05-20 11:00:00"
        )
        
        # Sample unit price 4 - Labor rate
        sample_price_4 = UnitPrice(
            price_id="price-004",
            item_code="LABOR-ELEC-HR",
            description="Journeyman electrician labor rate",
            category=PriceCategory.LABOR,
            unit_type=UnitType.HOUR,
            status=PriceStatus.ACTIVE,
            base_price=85.00,
            labor_cost=65.00,
            material_cost=0.00,
            equipment_cost=5.00,
            overhead_percentage=20.0,
            profit_percentage=15.0,
            total_price=96.90,
            specification="Licensed journeyman electrician, union scale",
            vendor_name="Highland Electrical Contractors",
            vendor_contact="David Wilson - (555) 567-8901",
            model_number=None,
            brand=None,
            effective_date="2025-05-01",
            expiration_date="2025-12-31",
            price_source=PriceSource.SUBCONTRACTOR_BID,
            quote_reference="HEC-2025-LABOR-001",
            location_factor=1.1,
            minimum_quantity=8,
            maximum_quantity=None,
            delivery_time_days=0,
            payment_terms="Weekly payroll",
            quality_rating=4.6,
            reliability_score=4.7,
            past_performance="Skilled workforce, good safety record",
            price_history=[
                PriceHistory(
                    date="2025-01-01",
                    price=82.00,
                    source="Contract rate",
                    notes="2025 contract start"
                )
            ],
            last_updated="2025-05-01",
            price_trend="Stable",
            project_name="Highland Tower Development",
            work_package="Electrical Systems",
            csi_code="26 05 00",
            pricing_notes="Includes basic hand tools and safety equipment",
            special_conditions="Overtime rates: 1.5x after 8 hours, 2x weekends",
            created_by="Sarah Wilson - Estimator",
            approved_by="John Smith - Project Manager",
            created_at="2025-05-01 08:00:00",
            updated_at="2025-05-01 08:00:00"
        )
        
        # Calculate total prices
        sample_price_1.total_price = sample_price_1.calculate_total_price()
        sample_price_2.total_price = sample_price_2.calculate_total_price()
        sample_price_3.total_price = sample_price_3.calculate_total_price()
        sample_price_4.total_price = sample_price_4.calculate_total_price()
        
        self.unit_prices[sample_price_1.price_id] = sample_price_1
        self.unit_prices[sample_price_2.price_id] = sample_price_2
        self.unit_prices[sample_price_3.price_id] = sample_price_3
        self.unit_prices[sample_price_4.price_id] = sample_price_4
    
    def create_unit_price(self, price_data: Dict[str, Any]) -> str:
        """Create a new unit price"""
        price_id = f"price-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        price_data.update({
            "price_id": price_id,
            "status": PriceStatus.PENDING_APPROVAL,
            "price_history": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        price_data["category"] = PriceCategory(price_data["category"])
        price_data["unit_type"] = UnitType(price_data["unit_type"])
        price_data["status"] = PriceStatus(price_data["status"])
        price_data["price_source"] = PriceSource(price_data["price_source"])
        
        unit_price = UnitPrice(**price_data)
        unit_price.total_price = unit_price.calculate_total_price()
        
        self.unit_prices[price_id] = unit_price
        return price_id
    
    def get_unit_price(self, price_id: str) -> Optional[UnitPrice]:
        """Get a specific unit price"""
        return self.unit_prices.get(price_id)
    
    def get_all_unit_prices(self) -> List[UnitPrice]:
        """Get all unit prices sorted by category and description"""
        return sorted(self.unit_prices.values(),
                     key=lambda p: (p.category.value, p.description))
    
    def get_prices_by_category(self, category: PriceCategory) -> List[UnitPrice]:
        """Get unit prices by category"""
        return [price for price in self.unit_prices.values() if price.category == category]
    
    def get_active_prices(self) -> List[UnitPrice]:
        """Get only active unit prices"""
        return [price for price in self.unit_prices.values() if price.status == PriceStatus.ACTIVE]
    
    def update_price(self, price_id: str, new_price: float, notes: str) -> bool:
        """Update unit price and add to history"""
        unit_price = self.unit_prices.get(price_id)
        if not unit_price:
            return False
        
        # Add current price to history
        history_entry = PriceHistory(
            date=datetime.now().strftime('%Y-%m-%d'),
            price=unit_price.total_price,
            source="Price update",
            notes=notes
        )
        unit_price.price_history.append(history_entry)
        
        # Update price
        old_price = unit_price.total_price
        unit_price.total_price = new_price
        unit_price.last_updated = datetime.now().strftime('%Y-%m-%d')
        unit_price.updated_at = datetime.now().isoformat()
        
        # Update trend
        if new_price > old_price:
            unit_price.price_trend = "Increasing"
        elif new_price < old_price:
            unit_price.price_trend = "Decreasing"
        else:
            unit_price.price_trend = "Stable"
        
        return True
    
    def search_prices(self, search_term: str) -> List[UnitPrice]:
        """Search unit prices by description or item code"""
        search_term = search_term.lower()
        results = []
        
        for price in self.unit_prices.values():
            if (search_term in price.description.lower() or 
                search_term in price.item_code.lower() or
                search_term in price.specification.lower()):
                results.append(price)
        
        return results
    
    def generate_price_metrics(self) -> Dict[str, Any]:
        """Generate unit price analytics"""
        prices = list(self.unit_prices.values())
        
        if not prices:
            return {}
        
        total_prices = len(prices)
        
        # Category breakdown
        category_counts = {}
        for category in PriceCategory:
            category_counts[category.value] = len([p for p in prices if p.category == category])
        
        # Status breakdown
        status_counts = {}
        for status in PriceStatus:
            status_counts[status.value] = len([p for p in prices if p.status == status])
        
        # Price trends
        trend_counts = {
            "Increasing": len([p for p in prices if p.price_trend == "Increasing"]),
            "Decreasing": len([p for p in prices if p.price_trend == "Decreasing"]),
            "Stable": len([p for p in prices if p.price_trend == "Stable"])
        }
        
        # Average quality ratings
        quality_ratings = [p.quality_rating for p in prices if p.quality_rating > 0]
        avg_quality = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0
        
        reliability_scores = [p.reliability_score for p in prices if p.reliability_score > 0]
        avg_reliability = sum(reliability_scores) / len(reliability_scores) if reliability_scores else 0
        
        # Vendor analysis
        vendors = list(set(p.vendor_name for p in prices))
        vendor_count = len(vendors)
        
        return {
            "total_unit_prices": total_prices,
            "category_breakdown": category_counts,
            "status_breakdown": status_counts,
            "price_trends": trend_counts,
            "average_quality_rating": round(avg_quality, 1),
            "average_reliability_score": round(avg_reliability, 1),
            "total_vendors": vendor_count,
            "active_prices": status_counts.get("Active", 0)
        }
    
    def validate_price_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate unit price data"""
        errors = []
        
        required_fields = ["item_code", "description", "category", "unit_type", 
                          "base_price", "vendor_name", "effective_date"]
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        if data.get("base_price", 0) <= 0:
            errors.append("Base price must be greater than 0")
        
        if data.get("overhead_percentage", -1) < 0:
            errors.append("Overhead percentage cannot be negative")
        
        if data.get("profit_percentage", -1) < 0:
            errors.append("Profit percentage cannot be negative")
        
        return errors

# Global instance for use across the application
unit_prices_manager = UnitPricesManager()