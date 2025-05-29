"""
Base Module Class for gcPanel Construction Management Platform
Provides standardized database operations and workflow integration
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import streamlit as st
from core.database_schema import WorkflowEngine, DataValidator

class BaseModule:
    """Base class for all gcPanel modules with standardized operations"""
    
    def __init__(self, module_name: str, data_path: str):
        self.module_name = module_name
        self.data_path = data_path
        self.workflow_engine = WorkflowEngine()
        self.validator = DataValidator()
        self._ensure_data_directory()
        self._initialize_module_data()
    
    def _ensure_data_directory(self):
        """Ensure module data directory exists"""
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
    
    def _initialize_module_data(self):
        """Initialize module data file if it doesn't exist"""
        if not os.path.exists(self.data_path):
            initial_data = {
                "module": self.module_name,
                "version": "1.0.0",
                "created": datetime.now().isoformat(),
                "items": []
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> Dict:
        """Load module data from file"""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # Ensure proper structure
                if isinstance(data, list):
                    return {"items": data}
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {"items": []}
    
    def _save_data(self, data: Dict):
        """Save module data to file"""
        try:
            with open(self.data_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            st.error(f"Failed to save data: {str(e)}")
    
    def get_items(self) -> List[Dict]:
        """Get all items for this module"""
        data = self._load_data()
        return data.get("items", [])
    
    def get_item_by_id(self, item_id: str) -> Optional[Dict]:
        """Get specific item by ID"""
        items = self.get_items()
        return next((item for item in items if item.get("id") == item_id), None)
    
    def add_item(self, item: Dict) -> bool:
        """Add new item to module"""
        try:
            data = self._load_data()
            items = data.get("items", [])
            
            # Generate ID if not provided
            if "id" not in item:
                item["id"] = f"{self.module_name}_{len(items) + 1}_{int(datetime.now().timestamp())}"
            
            # Add timestamps
            item["created_date"] = datetime.now().isoformat()
            item["modified_date"] = datetime.now().isoformat()
            
            items.append(item)
            data["items"] = items
            self._save_data(data)
            
            # Trigger workflow if applicable
            self._trigger_creation_workflow(item)
            
            return True
        except Exception as e:
            st.error(f"Failed to add item: {str(e)}")
            return False
    
    def update_item(self, item_id: str, updates: Dict) -> bool:
        """Update existing item"""
        try:
            data = self._load_data()
            items = data.get("items", [])
            
            for i, item in enumerate(items):
                if item.get("id") == item_id:
                    # Preserve original creation date
                    updates["created_date"] = item.get("created_date")
                    updates["modified_date"] = datetime.now().isoformat()
                    updates["id"] = item_id
                    
                    items[i] = updates
                    data["items"] = items
                    self._save_data(data)
                    
                    # Trigger workflow if applicable
                    self._trigger_update_workflow(updates)
                    
                    return True
            
            return False
        except Exception as e:
            st.error(f"Failed to update item: {str(e)}")
            return False
    
    def delete_item(self, item_id: str) -> bool:
        """Delete item by ID"""
        try:
            data = self._load_data()
            items = data.get("items", [])
            
            original_count = len(items)
            items = [item for item in items if item.get("id") != item_id]
            
            if len(items) < original_count:
                data["items"] = items
                self._save_data(data)
                
                # Trigger workflow if applicable
                self._trigger_deletion_workflow(item_id)
                
                return True
            
            return False
        except Exception as e:
            st.error(f"Failed to delete item: {str(e)}")
            return False
    
    def get_related_items(self, item_id: str, related_module: str) -> List[Dict]:
        """Get items related to this item from another module"""
        try:
            related_path = f"data/{related_module}/{related_module}.json"
            if os.path.exists(related_path):
                with open(related_path, 'r') as f:
                    related_data = json.load(f)
                    
                # Find items that reference this item
                related_items = []
                items = related_data.get("items", [])
                
                for item in items:
                    # Check various relationship fields
                    if (item.get("project_id") == item_id or
                        item.get("contract_id") == item_id or
                        item.get("parent_id") == item_id):
                        related_items.append(item)
                
                return related_items
            
            return []
        except Exception:
            return []
    
    def _trigger_creation_workflow(self, item: Dict):
        """Trigger workflow when item is created"""
        workflow_data = {
            "module": self.module_name,
            "action": "create",
            "item_id": item.get("id"),
            "item_data": item
        }
        
        # Module-specific workflow triggers
        if self.module_name == "contracts" and item.get("type") == "owner":
            self.workflow_engine.trigger_workflow("contract_creation", workflow_data)
        elif self.module_name == "change_orders":
            self.workflow_engine.trigger_workflow("change_order_approval", workflow_data)
        elif self.module_name == "safety":
            self.workflow_engine.trigger_workflow("safety_incident", workflow_data)
    
    def _trigger_update_workflow(self, item: Dict):
        """Trigger workflow when item is updated"""
        workflow_data = {
            "module": self.module_name,
            "action": "update",
            "item_id": item.get("id"),
            "item_data": item
        }
        
        # Module-specific workflow triggers
        if self.module_name == "sov_items":
            self.workflow_engine.trigger_workflow("sov_update", workflow_data)
        elif self.module_name == "payment_applications":
            self.workflow_engine.trigger_workflow("payment_application", workflow_data)
    
    def _trigger_deletion_workflow(self, item_id: str):
        """Trigger workflow when item is deleted"""
        workflow_data = {
            "module": self.module_name,
            "action": "delete",
            "item_id": item_id
        }
        
        # Module-specific cleanup workflows could be added here
        pass
    
    def get_module_metrics(self) -> Dict:
        """Get basic metrics for this module"""
        items = self.get_items()
        return {
            "total_items": len(items),
            "created_today": len([
                item for item in items 
                if item.get("created_date", "").startswith(datetime.now().strftime("%Y-%m-%d"))
            ]),
            "last_modified": max([
                item.get("modified_date", "") for item in items
            ], default="")
        }
    
    def search_items(self, query: str, fields: List[str] = None) -> List[Dict]:
        """Search items by query in specified fields"""
        items = self.get_items()
        if not query:
            return items
        
        query = query.lower()
        search_fields = fields or ["title", "name", "description"]
        
        results = []
        for item in items:
            for field in search_fields:
                if field in item and query in str(item[field]).lower():
                    results.append(item)
                    break
        
        return results
    
    def filter_items(self, filters: Dict) -> List[Dict]:
        """Filter items by field values"""
        items = self.get_items()
        
        for field, value in filters.items():
            if value:  # Only apply non-empty filters
                items = [
                    item for item in items 
                    if item.get(field) == value
                ]
        
        return items
    
    def export_data(self, format: str = "json") -> str:
        """Export module data in specified format"""
        data = self._load_data()
        
        if format == "json":
            return json.dumps(data, indent=2)
        elif format == "csv":
            # Basic CSV export implementation
            items = data.get("items", [])
            if not items:
                return ""
            
            headers = list(items[0].keys())
            csv_lines = [",".join(headers)]
            
            for item in items:
                row = [str(item.get(header, "")) for header in headers]
                csv_lines.append(",".join(row))
            
            return "\n".join(csv_lines)
        
        return str(data)
    
    def get_workflow_status(self, item_id: str) -> List[Dict]:
        """Get workflow status for a specific item"""
        try:
            with open("data/relationships/workflow_log.json", 'r') as f:
                log_data = json.load(f)
            
            workflows = log_data.get("workflows", [])
            item_workflows = [
                workflow for workflow in workflows
                if workflow.get("data", {}).get("item_id") == item_id
            ]
            
            return item_workflows
        except Exception:
            return []

def create_module_instance(module_name: str, data_path: str) -> BaseModule:
    """Factory function to create module instances"""
    return BaseModule(module_name, data_path)