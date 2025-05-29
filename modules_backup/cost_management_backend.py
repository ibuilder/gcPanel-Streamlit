"""
Highland Tower Development - Cost Management Backend
Enterprise-grade cost tracking, budget management, and financial analytics.
"""

import json
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from decimal import Decimal

class CostCategory(Enum):
    LABOR = "Labor"
    MATERIALS = "Materials"
    EQUIPMENT = "Equipment"
    SUBCONTRACTOR = "Subcontractor"
    OVERHEAD = "Overhead"
    CONTINGENCY = "Contingency"

class BudgetStatus(Enum):
    ON_BUDGET = "On Budget"
    OVER_BUDGET = "Over Budget"
    UNDER_BUDGET = "Under Budget"
    AT_RISK = "At Risk"

class CostItemStatus(Enum):
    PLANNED = "Planned"
    COMMITTED = "Committed"
    INVOICED = "Invoiced"
    PAID = "Paid"

@dataclass
class CostItem:
    """Individual cost item tracking"""
    item_id: str
    description: str
    category: CostCategory
    status: CostItemStatus
    
    # Financial data
    budgeted_amount: float
    committed_amount: float
    actual_amount: float
    remaining_amount: float
    
    # Project details
    work_package: str
    location: str
    vendor_supplier: str
    
    # Dates
    planned_date: str
    actual_date: Optional[str]
    
    # References
    purchase_order: Optional[str]
    invoice_number: Optional[str]
    
    # Tracking
    created_by: str
    created_at: str
    updated_at: str
    
    def calculate_variance(self) -> float:
        """Calculate budget variance"""
        return self.actual_amount - self.budgeted_amount
    
    def calculate_variance_percentage(self) -> float:
        """Calculate variance as percentage"""
        if self.budgeted_amount == 0:
            return 0.0
        return (self.calculate_variance() / self.budgeted_amount) * 100

@dataclass
class BudgetCategory:
    """Budget category with allocated amounts"""
    category_id: str
    name: str
    category_type: CostCategory
    budgeted_amount: float
    committed_amount: float
    actual_amount: float
    
    def get_remaining_budget(self) -> float:
        """Get remaining budget amount"""
        return self.budgeted_amount - self.actual_amount
    
    def get_status(self) -> BudgetStatus:
        """Determine budget status"""
        variance = self.actual_amount - self.budgeted_amount
        variance_percentage = (variance / self.budgeted_amount) * 100 if self.budgeted_amount > 0 else 0
        
        if variance_percentage > 10:
            return BudgetStatus.OVER_BUDGET
        elif variance_percentage < -10:
            return BudgetStatus.UNDER_BUDGET
        elif variance_percentage > 5:
            return BudgetStatus.AT_RISK
        else:
            return BudgetStatus.ON_BUDGET

@dataclass
class ChangeOrder:
    """Change order tracking"""
    co_id: str
    co_number: str
    description: str
    amount: float
    status: str  # "Pending", "Approved", "Rejected"
    submitted_date: str
    approved_date: Optional[str]
    reason: str
    impact_description: str

class CostManager:
    """Enterprise cost management system"""
    
    def __init__(self):
        self.cost_items: Dict[str, CostItem] = {}
        self.budget_categories: Dict[str, BudgetCategory] = {}
        self.change_orders: Dict[str, ChangeOrder] = {}
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load Highland Tower Development sample cost data"""
        
        # Sample budget categories
        categories = [
            ("Structure", CostCategory.MATERIALS, 8500000, 7200000, 6850000),
            ("MEP Systems", CostCategory.SUBCONTRACTOR, 5200000, 4800000, 4650000),
            ("Labor - General", CostCategory.LABOR, 6800000, 6200000, 5950000),
            ("Facades", CostCategory.MATERIALS, 3400000, 3100000, 3250000),
            ("Site Work", CostCategory.SUBCONTRACTOR, 1800000, 1650000, 1580000),
            ("Equipment Rental", CostCategory.EQUIPMENT, 950000, 850000, 820000)
        ]
        
        for i, (name, cat_type, budgeted, committed, actual) in enumerate(categories):
            category = BudgetCategory(
                category_id=f"cat-{i+1:03d}",
                name=name,
                category_type=cat_type,
                budgeted_amount=budgeted,
                committed_amount=committed,
                actual_amount=actual
            )
            self.budget_categories[category.category_id] = category
        
        # Sample cost items
        sample_items = [
            {
                "description": "Level 15 Concrete Pour",
                "category": CostCategory.MATERIALS,
                "status": CostItemStatus.PAID,
                "budgeted_amount": 85000.0,
                "committed_amount": 87500.0,
                "actual_amount": 87500.0,
                "work_package": "Structure - Level 15",
                "location": "Level 15",
                "vendor_supplier": "ABC Concrete Supply",
                "planned_date": "2025-05-25",
                "actual_date": "2025-05-25",
                "purchase_order": "PO-2025-0234",
                "invoice_number": "INV-ABC-5671"
            },
            {
                "description": "MEP Rough-in - Levels 12-14",
                "category": CostCategory.SUBCONTRACTOR,
                "status": CostItemStatus.COMMITTED,
                "budgeted_amount": 245000.0,
                "committed_amount": 245000.0,
                "actual_amount": 0.0,
                "work_package": "MEP Systems",
                "location": "Levels 12-14",
                "vendor_supplier": "Highland MEP Contractors",
                "planned_date": "2025-06-01",
                "actual_date": None,
                "purchase_order": "PO-2025-0245",
                "invoice_number": None
            },
            {
                "description": "Tower Crane Rental - Month 8",
                "category": CostCategory.EQUIPMENT,
                "status": CostItemStatus.INVOICED,
                "budgeted_amount": 28000.0,
                "committed_amount": 28000.0,
                "actual_amount": 28000.0,
                "work_package": "Equipment",
                "location": "Site",
                "vendor_supplier": "Metro Crane Services",
                "planned_date": "2025-05-01",
                "actual_date": "2025-05-01",
                "purchase_order": "PO-2025-0198",
                "invoice_number": "INV-MCS-8821"
            }
        ]
        
        for i, item_data in enumerate(sample_items):
            item_id = f"cost-{i+1:03d}"
            item_data.update({
                "item_id": item_id,
                "remaining_amount": item_data["budgeted_amount"] - item_data["actual_amount"],
                "created_by": "Project Manager",
                "created_at": "2025-05-20 09:00:00",
                "updated_at": "2025-05-27 10:00:00"
            })
            
            cost_item = CostItem(**item_data)
            self.cost_items[item_id] = cost_item
        
        # Sample change orders
        sample_co = ChangeOrder(
            co_id="co-001",
            co_number="CO-2025-001",
            description="Additional structural reinforcement for Level 15",
            amount=125000.0,
            status="Approved",
            submitted_date="2025-05-15",
            approved_date="2025-05-22",
            reason="Engineering requirement for increased load capacity",
            impact_description="Structural enhancement for future equipment installation"
        )
        
        self.change_orders[sample_co.co_id] = sample_co
    
    def create_cost_item(self, item_data: Dict[str, Any]) -> str:
        """Create a new cost item"""
        item_id = f"cost-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        item_data.update({
            "item_id": item_id,
            "remaining_amount": item_data["budgeted_amount"] - item_data.get("actual_amount", 0),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Convert enums
        item_data["category"] = CostCategory(item_data["category"])
        item_data["status"] = CostItemStatus(item_data["status"])
        
        cost_item = CostItem(**item_data)
        self.cost_items[item_id] = cost_item
        
        return item_id
    
    def get_cost_item(self, item_id: str) -> Optional[CostItem]:
        """Get a specific cost item"""
        return self.cost_items.get(item_id)
    
    def get_all_cost_items(self) -> List[CostItem]:
        """Get all cost items"""
        return list(self.cost_items.values())
    
    def update_cost_item(self, item_id: str, updates: Dict[str, Any]) -> bool:
        """Update a cost item"""
        if item_id not in self.cost_items:
            return False
        
        item = self.cost_items[item_id]
        
        for key, value in updates.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        # Recalculate remaining amount
        item.remaining_amount = item.budgeted_amount - item.actual_amount
        item.updated_at = datetime.now().isoformat()
        
        return True
    
    def get_items_by_category(self, category: CostCategory) -> List[CostItem]:
        """Get cost items by category"""
        return [item for item in self.cost_items.values() if item.category == category]
    
    def get_items_by_status(self, status: CostItemStatus) -> List[CostItem]:
        """Get cost items by status"""
        return [item for item in self.cost_items.values() if item.status == status]
    
    def calculate_project_totals(self) -> Dict[str, float]:
        """Calculate project-wide financial totals"""
        total_budget = sum(cat.budgeted_amount for cat in self.budget_categories.values())
        total_committed = sum(cat.committed_amount for cat in self.budget_categories.values())
        total_actual = sum(cat.actual_amount for cat in self.budget_categories.values())
        total_remaining = total_budget - total_actual
        
        # Add change orders
        approved_cos = [co for co in self.change_orders.values() if co.status == "Approved"]
        total_change_orders = sum(co.amount for co in approved_cos)
        
        return {
            "total_budget": total_budget,
            "total_committed": total_committed,
            "total_actual": total_actual,
            "total_remaining": total_remaining,
            "total_change_orders": total_change_orders,
            "revised_budget": total_budget + total_change_orders,
            "budget_variance": total_actual - total_budget,
            "variance_percentage": ((total_actual - total_budget) / total_budget * 100) if total_budget > 0 else 0
        }
    
    def get_category_performance(self) -> List[Dict[str, Any]]:
        """Get performance data for each budget category"""
        performance_data = []
        
        for category in self.budget_categories.values():
            variance = category.actual_amount - category.budgeted_amount
            variance_pct = (variance / category.budgeted_amount * 100) if category.budgeted_amount > 0 else 0
            
            performance_data.append({
                "Category": category.name,
                "Type": category.category_type.value,
                "Budgeted": category.budgeted_amount,
                "Committed": category.committed_amount,
                "Actual": category.actual_amount,
                "Remaining": category.get_remaining_budget(),
                "Variance": variance,
                "Variance_Pct": round(variance_pct, 1),
                "Status": category.get_status().value
            })
        
        return performance_data
    
    def get_cash_flow_data(self) -> List[Dict[str, Any]]:
        """Generate cash flow analysis data"""
        # This would typically pull from actual payment schedules
        # For now, return sample monthly data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        cash_flow_data = []
        cumulative_actual = 0
        cumulative_planned = 0
        
        # Sample monthly spending (this would come from actual data)
        monthly_planned = [2100000, 2800000, 3200000, 3800000, 4200000, 4600000, 
                          5000000, 5400000, 5800000, 6200000, 6500000, 6800000]
        monthly_actual = [2050000, 2750000, 3150000, 3900000, 4100000, 0, 0, 0, 0, 0, 0, 0]
        
        for i, month in enumerate(months):
            if i < len(monthly_actual) and monthly_actual[i] > 0:
                cumulative_actual += monthly_actual[i] - (monthly_actual[i-1] if i > 0 else 0)
            
            cumulative_planned = monthly_planned[i]
            
            cash_flow_data.append({
                "Month": month,
                "Planned_Cumulative": cumulative_planned,
                "Actual_Cumulative": cumulative_actual,
                "Variance": cumulative_actual - cumulative_planned
            })
        
        return cash_flow_data
    
    def validate_cost_item_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate cost item data"""
        errors = []
        
        required_fields = ["description", "category", "status", "budgeted_amount", "work_package", "created_by"]
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing")
        
        if data.get("budgeted_amount", 0) <= 0:
            errors.append("Budgeted amount must be greater than 0")
        
        if data.get("actual_amount", 0) < 0:
            errors.append("Actual amount cannot be negative")
        
        return errors

# Global instance for use across the application
cost_manager = CostManager()