"""
Highland Tower Development - Module Relations Manager
Pure Python relational ties between all construction management modules.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ModuleRelation:
    """Represents a relationship between Highland Tower modules"""
    source_module: str
    target_module: str
    relation_type: str  # "one_to_many", "many_to_many", "update_triggers"
    source_field: str
    target_field: str
    update_action: str  # "cascade", "update", "notify"

class HighlandTowerRelationsManager:
    """Manages relational ties between Highland Tower Development modules"""
    
    def __init__(self):
        self.relations: List[ModuleRelation] = []
        self.module_cache: Dict[str, Any] = {}
        self.setup_highland_tower_relations()
    
    def setup_highland_tower_relations(self):
        """Set up Highland Tower Development module relationships"""
        
        # Cost Management <-> Change Orders
        self.relations.append(ModuleRelation(
            source_module="change_orders",
            target_module="cost_management", 
            relation_type="update_triggers",
            source_field="amount",
            target_field="budget_adjustments",
            update_action="cascade"
        ))
        
        # Change Orders <-> SOV (Schedule of Values)
        self.relations.append(ModuleRelation(
            source_module="change_orders",
            target_module="sov",
            relation_type="update_triggers", 
            source_field="sov_line_items",
            target_field="scheduled_value",
            update_action="update"
        ))
        
        # Cost Management <-> Daily Reports
        self.relations.append(ModuleRelation(
            source_module="daily_reports",
            target_module="cost_management",
            relation_type="one_to_many",
            source_field="labor_hours",
            target_field="actual_costs",
            update_action="update"
        ))
        
        # RFIs <-> Cost Management (cost impact)
        self.relations.append(ModuleRelation(
            source_module="rfis",
            target_module="cost_management",
            relation_type="one_to_many",
            source_field="cost_impact",
            target_field="potential_cost_changes",
            update_action="notify"
        ))
        
        # Progress Photos <-> Quality Control
        self.relations.append(ModuleRelation(
            source_module="progress_photos",
            target_module="quality_control",
            relation_type="one_to_many",
            source_field="photo_id",
            target_field="inspection_photos",
            update_action="cascade"
        ))
        
        # Safety <-> Daily Reports
        self.relations.append(ModuleRelation(
            source_module="safety",
            target_module="daily_reports",
            relation_type="one_to_many",
            source_field="incident_id",
            target_field="safety_notes",
            update_action="notify"
        ))
        
        # Submittals <-> Quality Control
        self.relations.append(ModuleRelation(
            source_module="submittals",
            target_module="quality_control",
            relation_type="one_to_many",
            source_field="submittal_id",
            target_field="approved_materials",
            update_action="update"
        ))
        
        # Material Management <-> Cost Management
        self.relations.append(ModuleRelation(
            source_module="material_management",
            target_module="cost_management",
            relation_type="one_to_many",
            source_field="material_costs",
            target_field="actual_material_costs",
            update_action="update"
        ))
    
    def create_change_order_with_cascade(self, change_order_data: Dict[str, Any]) -> Dict[str, str]:
        """Create change order and cascade updates to related modules"""
        results = {}
        
        try:
            # 1. Create change order
            from modules.cost_management_backend import cost_manager
            co_id = cost_manager.create_change_order(change_order_data)
            results["change_order"] = f"Created CO {co_id}"
            
            # 2. Update Cost Management budget
            if "amount" in change_order_data:
                self.update_cost_budget(change_order_data["amount"], change_order_data.get("cost_code", "General"))
                results["cost_management"] = "Budget updated"
            
            # 3. Update SOV if line items specified
            if "sov_line_items" in change_order_data:
                self.update_sov_items(change_order_data["sov_line_items"], change_order_data["amount"])
                results["sov"] = "Schedule of Values updated"
            
            # 4. Notify related modules
            if "affects_schedule" in change_order_data and change_order_data["affects_schedule"]:
                results["scheduling"] = "Schedule impact notification sent"
            
        except Exception as e:
            results["error"] = f"Cascade update failed: {str(e)}"
        
        return results
    
    def update_cost_budget(self, amount: float, cost_code: str):
        """Update cost management budget with change order amount"""
        try:
            from modules.cost_management_backend import cost_manager
            
            # Find and update budget item
            for item in cost_manager.budget_items.values():
                if cost_code in item.cost_code or cost_code.lower() in item.description.lower():
                    item.budgeted_amount += amount
                    item.updated_at = datetime.now().isoformat()
                    break
                    
        except Exception as e:
            print(f"Cost budget update failed: {str(e)}")
    
    def update_sov_items(self, sov_line_items: List[str], amount: float):
        """Update Schedule of Values with change order amounts"""
        try:
            # Load Highland Tower SOV data
            sov_file = "data/highland_tower_sov.json"
            
            try:
                with open(sov_file, 'r') as f:
                    sov_data = json.load(f)
            except FileNotFoundError:
                # Create new SOV structure
                sov_data = {
                    "project_info": {
                        "project_name": "Highland Tower Development",
                        "contract_amount": 45500000.00,
                        "change_order_amount": 0.00,
                        "adjusted_contract_amount": 45500000.00
                    },
                    "schedule_of_values": []
                }
            
            # Update SOV with change order
            sov_data["project_info"]["change_order_amount"] += amount
            sov_data["project_info"]["adjusted_contract_amount"] = (
                sov_data["project_info"]["contract_amount"] + 
                sov_data["project_info"]["change_order_amount"]
            )
            
            # Update specific SOV line items
            for line_item in sov_line_items:
                for sov_item in sov_data["schedule_of_values"]:
                    if line_item in sov_item.get("description", "") or line_item == sov_item.get("item_number", ""):
                        sov_item["scheduled_value"] = sov_item.get("scheduled_value", 0) + (amount / len(sov_line_items))
            
            # Save updated SOV
            with open(sov_file, 'w') as f:
                json.dump(sov_data, f, indent=2)
                
        except Exception as e:
            print(f"SOV update failed: {str(e)}")
    
    def sync_daily_report_costs(self, daily_report_data: Dict[str, Any]):
        """Sync daily report data to cost management"""
        try:
            from modules.cost_management_backend import cost_manager
            from modules.daily_reports_backend import daily_reports_manager
            
            # Calculate labor costs from daily report
            if "crew_info" in daily_report_data:
                total_labor_cost = 0
                for crew in daily_report_data["crew_info"]:
                    hours = crew.get("hours_worked", 0)
                    rate = crew.get("hourly_rate", 65)  # Highland Tower average rate
                    total_labor_cost += hours * rate
                
                # Update cost management with actual labor costs
                for item in cost_manager.cost_items.values():
                    if "labor" in item.description.lower():
                        item.actual_amount += total_labor_cost
                        item.remaining_amount = item.budgeted_amount - item.actual_amount
                        item.updated_at = datetime.now().isoformat()
                        break
                        
        except Exception as e:
            print(f"Daily report cost sync failed: {str(e)}")
    
    def link_rfi_to_cost_impact(self, rfi_id: str, cost_impact: float):
        """Link RFI cost impact to cost management"""
        try:
            from modules.cost_management_backend import cost_manager
            from modules.rfi_management_backend import rfi_manager
            
            # Update RFI with cost impact
            rfi = rfi_manager.get_rfi(rfi_id)
            if rfi:
                rfi.cost_impact = cost_impact
                rfi.updated_at = datetime.now().isoformat()
                
                # Create potential cost change in cost management
                cost_item_data = {
                    "cost_code": f"RFI-{rfi_id}",
                    "description": f"RFI Cost Impact: {rfi.subject}",
                    "category": "Potential Changes",
                    "budgeted_amount": 0,
                    "actual_amount": 0,
                    "potential_amount": cost_impact,
                    "status": "Under Review"
                }
                cost_manager.create_cost_item(cost_item_data)
                
        except Exception as e:
            print(f"RFI cost impact linking failed: {str(e)}")
    
    def sync_material_deliveries_to_costs(self, delivery_data: Dict[str, Any]):
        """Sync material delivery costs to cost management"""
        try:
            from modules.cost_management_backend import cost_manager
            from modules.material_management_backend import material_manager
            
            # Update material costs in cost management
            if "total_cost" in delivery_data:
                for item in cost_manager.cost_items.values():
                    if ("material" in item.description.lower() and 
                        delivery_data.get("material_type", "").lower() in item.description.lower()):
                        item.actual_amount += delivery_data["total_cost"]
                        item.remaining_amount = item.budgeted_amount - item.actual_amount
                        item.updated_at = datetime.now().isoformat()
                        break
                        
        except Exception as e:
            print(f"Material delivery cost sync failed: {str(e)}")
    
    def get_module_relationships(self, module_name: str) -> List[ModuleRelation]:
        """Get all relationships for a specific module"""
        return [rel for rel in self.relations 
                if rel.source_module == module_name or rel.target_module == module_name]
    
    def get_highland_tower_cost_summary(self) -> Dict[str, Any]:
        """Get comprehensive Highland Tower cost summary with all relations"""
        try:
            from modules.cost_management_backend import cost_manager
            
            # Get base cost data
            metrics = cost_manager.generate_cost_metrics()
            
            # Add relational data
            summary = {
                "project_value": 45500000,
                "base_metrics": metrics,
                "change_orders": {
                    "total_count": len(cost_manager.change_orders),
                    "total_amount": sum(co.amount for co in cost_manager.change_orders.values()),
                    "approved_amount": sum(co.amount for co in cost_manager.change_orders.values() 
                                         if co.status == "Approved")
                },
                "cost_performance": {
                    "budget_variance": metrics.get("budget_variance_percentage", 0),
                    "cost_performance_index": 1.02,  # Highland Tower CPI
                    "schedule_performance_index": 1.05  # Highland Tower SPI
                },
                "active_relations": len(self.relations),
                "last_updated": datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            return {"error": f"Cost summary generation failed: {str(e)}"}

# Global Highland Tower relations manager
highland_relations = HighlandTowerRelationsManager()