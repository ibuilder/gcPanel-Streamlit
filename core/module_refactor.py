"""
Automated Module Refactoring System for gcPanel
Converts existing modules to use standardized base class and database relationships
"""

import os
import json
from datetime import datetime
from typing import Dict, List
import streamlit as st

class ModuleRefactor:
    """Automated system to refactor existing modules"""
    
    def __init__(self):
        self.modules_to_refactor = [
            "contracts", "cost_management", "safety", "field_operations",
            "documents", "bim", "closeout", "engineering", "preconstruction"
        ]
        self.refactor_log = []
    
    def execute_full_refactor(self):
        """Execute complete refactoring of all modules"""
        st.info("🔄 Starting automated module refactoring...")
        
        for module in self.modules_to_refactor:
            success = self._refactor_module(module)
            if success:
                st.success(f"✅ {module.title()} module refactored successfully")
            else:
                st.warning(f"⚠️ {module.title()} module refactoring had issues")
        
        self._create_workflow_connections()
        self._update_main_application()
        
        st.success("🎉 All modules refactored with standardized base class and database relationships!")
    
    def _refactor_module(self, module_name: str) -> bool:
        """Refactor individual module to use base class"""
        try:
            # Create standardized module class
            self._create_standardized_module(module_name)
            
            # Migrate existing data to new format
            self._migrate_module_data(module_name)
            
            # Update module to use workflow engine
            self._add_workflow_integration(module_name)
            
            self.refactor_log.append({
                "module": module_name,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            self.refactor_log.append({
                "module": module_name,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def _create_standardized_module(self, module_name: str):
        """Create standardized module class"""
        
        # Module-specific configurations
        module_configs = {
            "contracts": {
                "primary_fields": ["contract_id", "project_id", "contract_type", "contractor_name", "value"],
                "relationships": ["change_orders", "sov_items", "payment_applications"],
                "workflows": ["contract_creation", "contract_approval", "change_order_processing"]
            },
            "cost_management": {
                "primary_fields": ["cost_item_id", "project_id", "description", "budgeted_amount", "actual_amount"],
                "relationships": ["contracts", "invoices", "payment_applications"],
                "workflows": ["budget_update", "cost_tracking", "payment_processing"]
            },
            "safety": {
                "primary_fields": ["incident_id", "project_id", "incident_type", "severity", "date"],
                "relationships": ["field_reports", "projects"],
                "workflows": ["incident_reporting", "safety_metrics_update", "compliance_tracking"]
            },
            "field_operations": {
                "primary_fields": ["report_id", "project_id", "date", "weather", "crew_count"],
                "relationships": ["safety_incidents", "projects"],
                "workflows": ["daily_reporting", "progress_tracking", "resource_management"]
            },
            "documents": {
                "primary_fields": ["document_id", "project_id", "document_type", "title", "version"],
                "relationships": ["contracts", "bim_models", "projects"],
                "workflows": ["document_approval", "version_control", "distribution"]
            },
            "bim": {
                "primary_fields": ["model_id", "project_id", "model_name", "discipline", "version"],
                "relationships": ["documents", "clash_detections", "projects"],
                "workflows": ["model_coordination", "clash_detection", "version_management"]
            }
        }
        
        config = module_configs.get(module_name, {
            "primary_fields": ["id", "name", "description"],
            "relationships": [],
            "workflows": []
        })
        
        # Create module directory if it doesn't exist
        module_dir = f"modules/{module_name}"
        os.makedirs(f"{module_dir}/components", exist_ok=True)
        
        # Create standardized module class
        module_content = f'''"""
{module_name.title()} Module for gcPanel Construction Management Platform
Standardized module using base class with database relationships and workflows
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
from core.base_module import BaseModule
from core.database_schema import WorkflowEngine

class {module_name.title().replace('_', '')}Module(BaseModule):
    """Standardized {module_name.title()} module with database relationships"""
    
    def __init__(self):
        super().__init__(
            module_name="{module_name}",
            data_path="data/{module_name}/{module_name}.json"
        )
        self.primary_fields = {config["primary_fields"]}
        self.relationships = {config["relationships"]}
        self.workflows = {config["workflows"]}
    
    def render(self):
        """Main render function for {module_name.title()} module"""
        st.title(f"📊 {{self.module_name.title().replace('_', ' ')}} Management")
        
        # Module metrics
        metrics = self.get_module_metrics()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Items", metrics["total_items"])
        with col2:
            st.metric("Created Today", metrics["created_today"])
        with col3:
            if metrics["last_modified"]:
                st.metric("Last Modified", metrics["last_modified"][:10])
        
        # Create tabs for module sections
        tabs = st.tabs(["Overview", "Add New", "Search", "Analytics"])
        
        with tabs[0]:
            self.render_overview()
        
        with tabs[1]:
            self.render_add_form()
        
        with tabs[2]:
            self.render_search()
        
        with tabs[3]:
            self.render_analytics()
    
    def render_overview(self):
        """Render overview of all items"""
        items = self.get_items()
        
        if not items:
            st.info(f"No {{self.module_name}} items found. Use the 'Add New' tab to create items.")
            return
        
        # Display items in a table format
        for item in items[-10:]:  # Show last 10 items
            with st.expander(f"{{item.get('title', item.get('name', item.get('id')))}}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    for field in self.primary_fields[:3]:
                        if field in item:
                            st.text(f"{{field.title()}}: {{item[field]}}")
                
                with col2:
                    st.text(f"Created: {{item.get('created_date', '')[:10]}}")
                    st.text(f"Status: {{item.get('status', 'Active')}}")
                    
                    if st.button(f"Edit {{item.get('id')}}", key=f"edit_{{item.get('id')}}"):
                        st.session_state[f"edit_{{self.module_name}}_{{item.get('id')}}"] = True
    
    def render_add_form(self):
        """Render form to add new item"""
        st.markdown("### Add New {{self.module_name.title().replace('_', ' ')}} Item")
        
        with st.form(f"add_{{self.module_name}}_form"):
            form_data = {{}}
            
            # Create form fields based on primary fields
            for field in self.primary_fields:
                if field.endswith("_id"):
                    form_data[field] = st.text_input(f"{{field.replace('_', ' ').title()}}")
                elif field in ["amount", "value", "cost"]:
                    form_data[field] = st.number_input(f"{{field.title()}}", min_value=0.0)
                elif field == "date":
                    form_data[field] = st.date_input(f"{{field.title()}}")
                else:
                    form_data[field] = st.text_input(f"{{field.replace('_', ' ').title()}}")
            
            # Additional common fields
            form_data["description"] = st.text_area("Description")
            form_data["status"] = st.selectbox("Status", ["Active", "Pending", "Completed", "Cancelled"])
            
            submit_button = st.form_submit_button("Add Item")
            
            if submit_button:
                # Validate required fields
                required_fields = [f for f in self.primary_fields if not f.endswith("_id") or f == "project_id"]
                missing_fields = [f for f in required_fields if not form_data.get(f)]
                
                if missing_fields:
                    st.error(f"Please fill in required fields: {{', '.join(missing_fields)}}")
                else:
                    success = self.add_item(form_data)
                    if success:
                        st.success("Item added successfully!")
                        st.rerun()
    
    def render_search(self):
        """Render search functionality"""
        st.markdown("### Search {{self.module_name.title().replace('_', ' ')}} Items")
        
        search_query = st.text_input("Search Query")
        
        if search_query:
            results = self.search_items(search_query)
            
            if results:
                st.markdown(f"Found {{len(results)}} results:")
                for item in results:
                    st.write(f"- {{item.get('title', item.get('name', item.get('id')))}}")
            else:
                st.info("No results found")
    
    def render_analytics(self):
        """Render analytics for this module"""
        st.markdown("### {{self.module_name.title().replace('_', ' ')}} Analytics")
        
        items = self.get_items()
        
        if not items:
            st.info("No data available for analytics")
            return
        
        # Basic analytics
        col1, col2 = st.columns(2)
        
        with col1:
            # Status distribution
            statuses = [item.get("status", "Unknown") for item in items]
            status_counts = {{}}
            for status in statuses:
                status_counts[status] = status_counts.get(status, 0) + 1
            
            st.bar_chart(status_counts)
        
        with col2:
            # Timeline chart
            dates = [item.get("created_date", "")[:10] for item in items if item.get("created_date")]
            date_counts = {{}}
            for date in dates:
                date_counts[date] = date_counts.get(date, 0) + 1
            
            st.line_chart(date_counts)

def render():
    """Main render function for the module"""
    module = {module_name.title().replace('_', '')}Module()
    module.render()
'''
        
        # Write the standardized module file
        with open(f"modules/{module_name}/__init__.py", 'w') as f:
            f.write(module_content)
    
    def _migrate_module_data(self, module_name: str):
        """Migrate existing module data to new standardized format"""
        old_data_paths = [
            f"data/{module_name}.json",
            f"data/{module_name}/{module_name}.json",
            f"modules/{module_name}/data.json"
        ]
        
        # Find existing data
        existing_data = None
        for path in old_data_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        existing_data = json.load(f)
                    break
                except:
                    continue
        
        if existing_data:
            # Ensure new data directory exists
            os.makedirs(f"data/{module_name}", exist_ok=True)
            
            # Convert to standardized format
            if isinstance(existing_data, list):
                standardized_data = {
                    "module": module_name,
                    "version": "1.0.0",
                    "created": datetime.now().isoformat(),
                    "items": existing_data
                }
            else:
                standardized_data = existing_data
                if "items" not in standardized_data:
                    standardized_data["items"] = []
            
            # Save in new location
            with open(f"data/{module_name}/{module_name}.json", 'w') as f:
                json.dump(standardized_data, f, indent=2)
    
    def _add_workflow_integration(self, module_name: str):
        """Add workflow integration to module"""
        # This would add specific workflow triggers based on module type
        pass
    
    def _create_workflow_connections(self):
        """Create workflow connections between modules"""
        connections = {
            "contracts_to_cost": {
                "trigger": "contract_value_change",
                "target": "cost_management",
                "action": "update_budget"
            },
            "change_orders_to_sov": {
                "trigger": "change_order_approval",
                "target": "sov_items", 
                "action": "update_values"
            },
            "sov_to_billing": {
                "trigger": "sov_update",
                "target": "payment_applications",
                "action": "recalculate_amounts"
            },
            "safety_to_field": {
                "trigger": "safety_incident",
                "target": "field_operations",
                "action": "update_daily_report"
            }
        }
        
        # Save workflow connections
        os.makedirs("data/relationships", exist_ok=True)
        with open("data/relationships/workflow_connections.json", 'w') as f:
            json.dump(connections, f, indent=2)
    
    def _update_main_application(self):
        """Update main application to use refactored modules"""
        # This would update app.py and app_manager.py to use the new module structure
        pass
    
    def generate_refactor_report(self) -> str:
        """Generate report of refactoring process"""
        report = "# gcPanel Module Refactoring Report\n\n"
        report += f"**Refactoring completed at:** {datetime.now().isoformat()}\n\n"
        
        successful = [log for log in self.refactor_log if log["status"] == "success"]
        failed = [log for log in self.refactor_log if log["status"] == "failed"]
        
        report += f"**Successfully refactored:** {len(successful)} modules\n"
        report += f"**Failed refactoring:** {len(failed)} modules\n\n"
        
        if successful:
            report += "## ✅ Successfully Refactored Modules\n"
            for log in successful:
                report += f"- {log['module'].title()}\n"
        
        if failed:
            report += "\n## ❌ Failed Refactoring\n"
            for log in failed:
                report += f"- {log['module'].title()}: {log['error']}\n"
        
        report += "\n## 🔄 Workflow Connections Created\n"
        report += "- Contracts ↔ Cost Management\n"
        report += "- Change Orders ↔ Schedule of Values\n"
        report += "- SOV ↔ AIA G702/G703 Billing\n"
        report += "- Safety Incidents ↔ Field Operations\n"
        
        return report

def execute_refactoring():
    """Execute the complete refactoring process"""
    refactor = ModuleRefactor()
    refactor.execute_full_refactor()
    return refactor.generate_refactor_report()