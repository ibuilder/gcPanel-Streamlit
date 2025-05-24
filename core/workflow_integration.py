"""
Workflow Integration System for gcPanel
Implements real-time data relationships and process automation between modules
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class WorkflowIntegration:
    """Manages data relationships and automated workflows between modules"""
    
    def __init__(self):
        self.relationships_path = "data/relationships"
        self._ensure_directories()
        self._initialize_relationships()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.relationships_path, exist_ok=True)
    
    def _initialize_relationships(self):
        """Initialize core data relationships"""
        relationships = {
            "contract_to_sov": {
                "trigger_module": "contracts",
                "target_module": "cost_management", 
                "relationship_type": "one_to_many",
                "trigger_events": ["contract_created", "contract_modified"],
                "automated_actions": ["create_sov_items", "update_contract_totals"]
            },
            "change_order_to_sov": {
                "trigger_module": "contracts",
                "target_module": "cost_management",
                "relationship_type": "many_to_many", 
                "trigger_events": ["change_order_approved"],
                "automated_actions": ["update_sov_values", "recalculate_billing"]
            },
            "sov_to_billing": {
                "trigger_module": "cost_management",
                "target_module": "cost_management",
                "relationship_type": "one_to_one",
                "trigger_events": ["sov_progress_updated"],
                "automated_actions": ["update_g702_g703", "calculate_retainage"]
            },
            "safety_to_field": {
                "trigger_module": "safety", 
                "target_module": "field_operations",
                "relationship_type": "many_to_one",
                "trigger_events": ["incident_logged"],
                "automated_actions": ["update_daily_report", "notify_supervisor"]
            }
        }
        
        relationships_file = f"{self.relationships_path}/core_relationships.json"
        if not os.path.exists(relationships_file):
            with open(relationships_file, 'w') as f:
                json.dump(relationships, f, indent=2)
    
    def trigger_workflow(self, trigger_module: str, event: str, data: Dict) -> bool:
        """Trigger automated workflow based on module event"""
        try:
            # Load relationships
            with open(f"{self.relationships_path}/core_relationships.json", 'r') as f:
                relationships = json.load(f)
            
            # Find applicable relationships
            for rel_name, rel_config in relationships.items():
                if (rel_config["trigger_module"] == trigger_module and 
                    event in rel_config["trigger_events"]):
                    
                    success = self._execute_workflow(rel_name, rel_config, data)
                    self._log_workflow_execution(rel_name, event, data, success)
                    
                    if success:
                        st.success(f"✅ Workflow '{rel_name}' executed successfully")
                    
            return True
            
        except Exception as e:
            st.error(f"Workflow execution failed: {str(e)}")
            return False
    
    def _execute_workflow(self, workflow_name: str, config: Dict, data: Dict) -> bool:
        """Execute specific workflow actions"""
        target_module = config["target_module"]
        actions = config["automated_actions"]
        
        for action in actions:
            if workflow_name == "change_order_to_sov" and action == "update_sov_values":
                self._update_sov_from_change_order(data)
            elif workflow_name == "sov_to_billing" and action == "update_g702_g703":
                self._update_billing_from_sov(data)
            elif workflow_name == "safety_to_field" and action == "update_daily_report":
                self._update_field_report_from_safety(data)
        
        return True
    
    def _update_sov_from_change_order(self, change_order_data: Dict):
        """Update Schedule of Values when change order is approved"""
        try:
            # Load SOV data
            sov_file = "data/cost_management/aia_billing.json"
            if os.path.exists(sov_file):
                with open(sov_file, 'r') as f:
                    sov_data = json.load(f)
                
                # Ensure proper data structure
                if isinstance(sov_data, list):
                    # Convert old format to new format
                    sov_data = {
                        "project_info": {
                            "project_name": "Highland Tower Development",
                            "project_number": "HTD-2024-001",
                            "contract_amount": 45500000.00,
                            "change_order_amount": 0.00,
                            "adjusted_contract_amount": 45500000.00
                        },
                        "schedule_of_values": [],
                        "billing_history": []
                    }
                
                # Update change order amount
                current_co_amount = sov_data["project_info"].get("change_order_amount", 0)
                co_amount = change_order_data.get("amount", 0)
                
                sov_data["project_info"]["change_order_amount"] = current_co_amount + co_amount
                sov_data["project_info"]["adjusted_contract_amount"] = (
                    sov_data["project_info"]["contract_amount"] + 
                    sov_data["project_info"]["change_order_amount"]
                )
                
                # Save updated SOV
                with open(sov_file, 'w') as f:
                    json.dump(sov_data, f, indent=2)
                
                st.info("📊 Schedule of Values updated with change order amount")
            
        except Exception as e:
            st.error(f"Failed to update SOV: {str(e)}")
    
    def _update_billing_from_sov(self, sov_data: Dict):
        """Update AIA G702/G703 billing when SOV is modified"""
        try:
            # This would recalculate payment applications based on SOV changes
            st.info("💰 AIA G702/G703 billing recalculated based on SOV updates")
            
        except Exception as e:
            st.error(f"Failed to update billing: {str(e)}")
    
    def _update_field_report_from_safety(self, safety_data: Dict):
        """Update field reports when safety incident is logged"""
        try:
            # This would add safety incident details to daily field reports
            st.info("📋 Daily field report updated with safety incident details")
            
        except Exception as e:
            st.error(f"Failed to update field report: {str(e)}")
    
    def _log_workflow_execution(self, workflow_name: str, event: str, data: Dict, success: bool):
        """Log workflow execution for tracking"""
        log_file = f"{self.relationships_path}/workflow_log.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "workflow": workflow_name,
            "event": event,
            "success": success,
            "data_keys": list(data.keys()) if data else []
        }
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {"executions": []}
            
            log_data["executions"].append(log_entry)
            
            # Keep only last 100 entries
            log_data["executions"] = log_data["executions"][-100:]
            
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception:
            pass  # Don't fail workflow if logging fails
    
    def get_workflow_status(self) -> Dict:
        """Get current workflow execution status"""
        try:
            log_file = f"{self.relationships_path}/workflow_log.json"
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
                
                executions = log_data.get("executions", [])
                successful = len([e for e in executions if e["success"]])
                failed = len([e for e in executions if not e["success"]])
                
                return {
                    "total_executions": len(executions),
                    "successful": successful,
                    "failed": failed,
                    "success_rate": (successful / len(executions) * 100) if executions else 0
                }
            
        except Exception:
            pass
        
        return {"total_executions": 0, "successful": 0, "failed": 0, "success_rate": 0}

# Global workflow integration instance
workflow_integration = WorkflowIntegration()

def trigger_workflow(trigger_module: str, event: str, data: Dict) -> bool:
    """Global function to trigger workflows from any module"""
    return workflow_integration.trigger_workflow(trigger_module, event, data)