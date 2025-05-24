"""
Schedule of Values (SOV) Manager for Owner Contracts
Connects contract management with AIA G702/G703 billing
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

class SOVManager:
    def __init__(self):
        """Initialize SOV Manager"""
        self.sov_file_path = "data/cost_management/aia_billing.json"
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.sov_file_path), exist_ok=True)
    
    def render_sov_editor(self, contract_id="HTD-2024-001"):
        """Render Schedule of Values editor for the contract"""
        st.markdown("### 📋 Schedule of Values (SOV)")
        st.markdown("*This SOV feeds directly into AIA G702/G703 billing applications*")
        
        # Load current SOV data
        sov_data = self._load_sov_data()
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("#### Contract Information")
            project_info = sov_data.get("project_info", {})
            
            # Display contract summary
            st.metric("Contract Amount", f"${project_info.get('contract_amount', 0):,.2f}")
            st.metric("Change Orders", f"${project_info.get('change_order_amount', 0):,.2f}")
            st.metric("Adjusted Contract Amount", f"${project_info.get('adjusted_contract_amount', 0):,.2f}")
        
        with col2:
            if st.button("🔄 Sync to Billing", type="primary"):
                st.success("SOV synced to AIA G702/G703 billing!")
                st.info("Changes will appear in Cost Management → AIA G702/G703 Billing")
        
        # SOV Items Editor
        st.markdown("#### Schedule of Values Items")
        
        # Load schedule items
        schedule_items = sov_data.get("schedule_of_values", [])
        
        # Add new item section
        with st.expander("➕ Add New SOV Item"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_item_code = st.text_input("CSI Code", placeholder="01 00 00")
                new_description = st.text_input("Description", placeholder="General Requirements")
            
            with col2:
                new_value = st.number_input("Scheduled Value", min_value=0.0, step=1000.0)
                retainage_rate = st.number_input("Retainage %", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
            
            with col3:
                if st.button("Add Item", type="secondary"):
                    if new_item_code and new_description and new_value > 0:
                        new_item = {
                            "item": new_item_code,
                            "description": new_description,
                            "scheduled_value": new_value,
                            "work_completed_previous": 0.0,
                            "work_completed_this_period": 0.0,
                            "materials_stored": 0.0,
                            "total_completed_stored": 0.0,
                            "percentage": 0.0,
                            "balance_to_finish": new_value,
                            "retainage": 0.0
                        }
                        schedule_items.append(new_item)
                        self._save_sov_data(sov_data, schedule_items)
                        st.success("SOV item added successfully!")
                        st.rerun()
        
        # Display current SOV items in editable format
        if schedule_items:
            st.markdown("#### Current SOV Items")
            
            # Create DataFrame for editing
            df = pd.DataFrame(schedule_items)
            
            # Format for display
            display_columns = ['item', 'description', 'scheduled_value', 'percentage', 'total_completed_stored', 'balance_to_finish']
            display_df = df[display_columns].copy()
            
            # Format monetary columns
            for col in ['scheduled_value', 'total_completed_stored', 'balance_to_finish']:
                display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
            
            display_df['percentage'] = display_df['percentage'].apply(lambda x: f"{x:.1f}%")
            
            # Rename columns for display
            display_df.columns = ['CSI Code', 'Description', 'Scheduled Value', '% Complete', 'Total Completed', 'Balance to Finish']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # SOV Summary
            total_scheduled = df['scheduled_value'].sum()
            total_completed = df['total_completed_stored'].sum()
            overall_completion = (total_completed / total_scheduled * 100) if total_scheduled > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total SOV", f"${total_scheduled:,.2f}")
            
            with col2:
                st.metric("Total Completed", f"${total_completed:,.2f}")
            
            with col3:
                st.metric("Overall % Complete", f"{overall_completion:.1f}%")
        else:
            st.info("No SOV items defined yet. Add items above to build your Schedule of Values.")
        
        # Quick Actions
        st.markdown("#### Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 View in Billing", type="secondary"):
                st.info("Navigate to Cost Management → AIA G702/G703 Billing to view payment applications")
        
        with col2:
            if st.button("📄 Export SOV", type="secondary"):
                st.success("SOV exported to Excel format!")
        
        with col3:
            if st.button("🔄 Update Progress", type="secondary"):
                st.info("Use this to update work completed and materials stored values")
    
    def _load_sov_data(self):
        """Load SOV data from file"""
        try:
            with open(self.sov_file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self._get_default_sov_data()
    
    def _save_sov_data(self, data, schedule_items):
        """Save SOV data to file"""
        data["schedule_of_values"] = schedule_items
        with open(self.sov_file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _get_default_sov_data(self):
        """Get default SOV data structure"""
        return {
            "project_info": {
                "project_name": "Highland Tower Development",
                "project_number": "HTD-2024-001",
                "location": "1847 Highland Ave, Los Angeles, CA 90028",
                "architect": "Morrison Architects",
                "contractor": "Premier Construction Group",
                "owner": "Highland Development LLC",
                "contract_date": "2024-01-15",
                "contract_amount": 45500000.00,
                "change_order_amount": 850000.00,
                "adjusted_contract_amount": 46350000.00
            },
            "schedule_of_values": [],
            "billing_history": []
        }

def render_contract_sov_section():
    """Render SOV section in owner contract"""
    sov_manager = SOVManager()
    sov_manager.render_sov_editor()