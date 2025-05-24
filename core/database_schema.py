"""
Core Database Schema for gcPanel Construction Management Platform
Defines all database relationships and workflow processes between modules
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class DatabaseSchema:
    """Central database schema manager for gcPanel platform"""
    
    def __init__(self):
        self.base_path = "data"
        self.schema_version = "1.0.0"
        self._ensure_directories()
        self._initialize_schema()
    
    def _ensure_directories(self):
        """Ensure all required data directories exist"""
        directories = [
            "data/projects",
            "data/contracts", 
            "data/cost_management",
            "data/safety",
            "data/field_operations",
            "data/documents",
            "data/bim",
            "data/closeout",
            "data/engineering",
            "data/preconstruction",
            "data/analytics",
            "data/relationships"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _initialize_schema(self):
        """Initialize database schema with relationships"""
        schema_file = f"{self.base_path}/schema.json"
        
        if not os.path.exists(schema_file):
            schema = {
                "version": self.schema_version,
                "created": datetime.now().isoformat(),
                "entities": {
                    "project": {
                        "primary_key": "project_id",
                        "fields": ["project_name", "project_number", "location", "start_date", "end_date", "status", "budget"],
                        "relationships": {
                            "contracts": "one_to_many",
                            "cost_items": "one_to_many", 
                            "safety_incidents": "one_to_many",
                            "field_reports": "one_to_many",
                            "documents": "one_to_many",
                            "bim_models": "one_to_many"
                        }
                    },
                    "contract": {
                        "primary_key": "contract_id",
                        "fields": ["project_id", "contract_type", "contractor_name", "value", "execution_date", "status"],
                        "relationships": {
                            "project": "many_to_one",
                            "change_orders": "one_to_many",
                            "sov_items": "one_to_many",
                            "payment_applications": "one_to_many"
                        }
                    },
                    "change_order": {
                        "primary_key": "change_order_id", 
                        "fields": ["contract_id", "oco_number", "title", "amount", "status", "date_issued"],
                        "relationships": {
                            "contract": "many_to_one",
                            "sov_items": "many_to_many",
                            "cost_impacts": "one_to_many"
                        }
                    },
                    "sov_item": {
                        "primary_key": "sov_item_id",
                        "fields": ["contract_id", "csi_code", "description", "scheduled_value", "completed_value"],
                        "relationships": {
                            "contract": "many_to_one",
                            "change_orders": "many_to_many",
                            "payment_applications": "one_to_many"
                        }
                    },
                    "payment_application": {
                        "primary_key": "application_id",
                        "fields": ["contract_id", "application_number", "period_ending", "total_amount", "status"],
                        "relationships": {
                            "contract": "many_to_one",
                            "sov_items": "one_to_many"
                        }
                    },
                    "safety_incident": {
                        "primary_key": "incident_id",
                        "fields": ["project_id", "incident_type", "severity", "date", "location", "status"],
                        "relationships": {
                            "project": "many_to_one",
                            "field_reports": "many_to_many"
                        }
                    },
                    "field_report": {
                        "primary_key": "report_id", 
                        "fields": ["project_id", "date", "weather", "crew_count", "activities", "issues"],
                        "relationships": {
                            "project": "many_to_one",
                            "safety_incidents": "many_to_many"
                        }
                    },
                    "document": {
                        "primary_key": "document_id",
                        "fields": ["project_id", "document_type", "title", "file_path", "upload_date", "version"],
                        "relationships": {
                            "project": "many_to_one",
                            "contracts": "many_to_many",
                            "bim_models": "many_to_many"
                        }
                    },
                    "bim_model": {
                        "primary_key": "model_id",
                        "fields": ["project_id", "model_name", "discipline", "file_path", "version", "status"],
                        "relationships": {
                            "project": "many_to_one",
                            "documents": "many_to_many",
                            "clash_detections": "one_to_many"
                        }
                    }
                },
                "workflows": {
                    "change_order_process": {
                        "trigger": "change_order_creation",
                        "steps": [
                            "create_change_order",
                            "update_sov_items", 
                            "recalculate_contract_value",
                            "update_payment_applications",
                            "notify_stakeholders"
                        ]
                    },
                    "payment_application_process": {
                        "trigger": "payment_period_end",
                        "steps": [
                            "collect_sov_progress",
                            "calculate_retainage",
                            "generate_g702_g703",
                            "submit_for_approval",
                            "process_payment"
                        ]
                    },
                    "safety_incident_process": {
                        "trigger": "incident_report",
                        "steps": [
                            "log_incident",
                            "notify_safety_manager",
                            "investigate",
                            "update_safety_metrics",
                            "generate_corrective_actions"
                        ]
                    }
                }
            }
            
            with open(schema_file, 'w') as f:
                json.dump(schema, f, indent=2)

class WorkflowEngine:
    """Manages workflows and processes between modules"""
    
    def __init__(self):
        self.workflow_log_path = "data/relationships/workflow_log.json"
        self._ensure_workflow_log()
    
    def _ensure_workflow_log(self):
        """Ensure workflow log file exists"""
        if not os.path.exists(self.workflow_log_path):
            with open(self.workflow_log_path, 'w') as f:
                json.dump({"workflows": []}, f, indent=2)
    
    def trigger_workflow(self, workflow_name: str, trigger_data: Dict) -> bool:
        """Trigger a workflow process"""
        workflows = {
            "change_order_approval": self._process_change_order_approval,
            "sov_update": self._process_sov_update,
            "payment_application": self._process_payment_application,
            "safety_incident": self._process_safety_incident,
            "document_approval": self._process_document_approval
        }
        
        if workflow_name in workflows:
            return workflows[workflow_name](trigger_data)
        return False
    
    def _process_change_order_approval(self, data: Dict) -> bool:
        """Process change order approval workflow"""
        try:
            # Update SOV items
            self._update_related_sov_items(data["change_order_id"], data["amount"])
            
            # Update contract value
            self._update_contract_value(data["contract_id"], data["amount"])
            
            # Update payment applications
            self._update_payment_applications(data["contract_id"])
            
            # Log workflow execution
            self._log_workflow("change_order_approval", data, "completed")
            return True
        except Exception as e:
            self._log_workflow("change_order_approval", data, f"failed: {str(e)}")
            return False
    
    def _process_sov_update(self, data: Dict) -> bool:
        """Process Schedule of Values update workflow"""
        try:
            # Update related payment applications
            self._update_payment_applications(data["contract_id"])
            
            # Update project budget
            self._update_project_budget(data["project_id"])
            
            # Log workflow execution
            self._log_workflow("sov_update", data, "completed")
            return True
        except Exception as e:
            self._log_workflow("sov_update", data, f"failed: {str(e)}")
            return False
    
    def _process_payment_application(self, data: Dict) -> bool:
        """Process payment application workflow"""
        try:
            # Generate G702/G703 forms
            self._generate_payment_forms(data["application_id"])
            
            # Update contract cash flow
            self._update_cash_flow(data["contract_id"], data["amount"])
            
            # Log workflow execution
            self._log_workflow("payment_application", data, "completed")
            return True
        except Exception as e:
            self._log_workflow("payment_application", data, f"failed: {str(e)}")
            return False
    
    def _process_safety_incident(self, data: Dict) -> bool:
        """Process safety incident workflow"""
        try:
            # Update safety metrics
            self._update_safety_metrics(data["project_id"], data["incident_type"])
            
            # Generate safety alerts
            self._generate_safety_alerts(data["project_id"], data["severity"])
            
            # Log workflow execution
            self._log_workflow("safety_incident", data, "completed")
            return True
        except Exception as e:
            self._log_workflow("safety_incident", data, f"failed: {str(e)}")
            return False
    
    def _process_document_approval(self, data: Dict) -> bool:
        """Process document approval workflow"""
        try:
            # Update document status
            self._update_document_status(data["document_id"], "approved")
            
            # Notify stakeholders
            self._notify_document_stakeholders(data["document_id"])
            
            # Log workflow execution
            self._log_workflow("document_approval", data, "completed")
            return True
        except Exception as e:
            self._log_workflow("document_approval", data, f"failed: {str(e)}")
            return False
    
    def _update_related_sov_items(self, change_order_id: str, amount: float):
        """Update SOV items related to a change order"""
        # Implementation for SOV updates
        pass
    
    def _update_contract_value(self, contract_id: str, amount: float):
        """Update contract value based on change orders"""
        # Implementation for contract value updates
        pass
    
    def _update_payment_applications(self, contract_id: str):
        """Update payment applications for a contract"""
        # Implementation for payment application updates
        pass
    
    def _update_project_budget(self, project_id: str):
        """Update project budget based on SOV changes"""
        # Implementation for project budget updates
        pass
    
    def _generate_payment_forms(self, application_id: str):
        """Generate AIA G702/G703 forms"""
        # Implementation for form generation
        pass
    
    def _update_cash_flow(self, contract_id: str, amount: float):
        """Update contract cash flow"""
        # Implementation for cash flow updates
        pass
    
    def _update_safety_metrics(self, project_id: str, incident_type: str):
        """Update safety metrics for project"""
        # Implementation for safety metrics updates
        pass
    
    def _generate_safety_alerts(self, project_id: str, severity: str):
        """Generate safety alerts based on incidents"""
        # Implementation for safety alert generation
        pass
    
    def _update_document_status(self, document_id: str, status: str):
        """Update document approval status"""
        # Implementation for document status updates
        pass
    
    def _notify_document_stakeholders(self, document_id: str):
        """Notify stakeholders of document approval"""
        # Implementation for stakeholder notifications
        pass
    
    def _log_workflow(self, workflow_name: str, data: Dict, status: str):
        """Log workflow execution"""
        try:
            with open(self.workflow_log_path, 'r') as f:
                log_data = json.load(f)
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "workflow": workflow_name,
                "status": status,
                "data": data
            }
            
            log_data["workflows"].append(log_entry)
            
            with open(self.workflow_log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
        except Exception as e:
            st.error(f"Failed to log workflow: {str(e)}")

class DataValidator:
    """Validates data integrity across modules"""
    
    @staticmethod
    def validate_project_data(project_data: Dict) -> bool:
        """Validate project data structure"""
        required_fields = ["project_id", "project_name", "project_number", "location"]
        return all(field in project_data for field in required_fields)
    
    @staticmethod
    def validate_contract_data(contract_data: Dict) -> bool:
        """Validate contract data structure"""
        required_fields = ["contract_id", "project_id", "contract_type", "value"]
        return all(field in contract_data for field in required_fields)
    
    @staticmethod
    def validate_sov_data(sov_data: Dict) -> bool:
        """Validate SOV data structure"""
        required_fields = ["sov_item_id", "contract_id", "csi_code", "scheduled_value"]
        return all(field in sov_data for field in required_fields)
    
    @staticmethod
    def validate_change_order_data(co_data: Dict) -> bool:
        """Validate change order data structure"""
        required_fields = ["change_order_id", "contract_id", "amount", "status"]
        return all(field in co_data for field in required_fields)

def initialize_database_schema():
    """Initialize the database schema for gcPanel"""
    schema = DatabaseSchema()
    st.success("Database schema initialized successfully")
    return schema

def get_workflow_engine():
    """Get workflow engine instance"""
    return WorkflowEngine()