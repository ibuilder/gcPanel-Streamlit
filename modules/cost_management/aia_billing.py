"""
AIA G702/G703 Billing Module for gcPanel
Standard AIA Application and Certificate for Payment forms
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

class AIABillingModule:
    def __init__(self):
        """Initialize AIA G702/G703 billing module"""
        self.data_file_path = "data/cost_management/aia_billing.json"
        self._ensure_data_directory()
        self._initialize_demo_data()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
    
    def _initialize_demo_data(self):
        """Initialize AIA billing data if it doesn't exist"""
        # Always reinitialize to ensure proper format
        demo_data = {
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
                "schedule_of_values": [
                    {
                        "item": "01 00 00",
                        "description": "General Requirements",
                        "scheduled_value": 2275000.00,
                        "work_completed_previous": 2275000.00,
                        "work_completed_this_period": 0.00,
                        "materials_stored": 0.00,
                        "total_completed_stored": 2275000.00,
                        "percentage": 100.0,
                        "balance_to_finish": 0.00,
                        "retainage": 0.00
                    },
                    {
                        "item": "02 00 00",
                        "description": "Existing Conditions",
                        "scheduled_value": 1850000.00,
                        "work_completed_previous": 1850000.00,
                        "work_completed_this_period": 0.00,
                        "materials_stored": 0.00,
                        "total_completed_stored": 1850000.00,
                        "percentage": 100.0,
                        "balance_to_finish": 0.00,
                        "retainage": 0.00
                    },
                    {
                        "item": "03 00 00",
                        "description": "Concrete",
                        "scheduled_value": 4635000.00,
                        "work_completed_previous": 3945750.00,
                        "work_completed_this_period": 231750.00,
                        "materials_stored": 92700.00,
                        "total_completed_stored": 4270200.00,
                        "percentage": 92.1,
                        "balance_to_finish": 364800.00,
                        "retainage": 213510.00
                    },
                    {
                        "item": "04 00 00",
                        "description": "Masonry",
                        "scheduled_value": 1390500.00,
                        "work_completed_previous": 973350.00,
                        "work_completed_this_period": 208575.00,
                        "materials_stored": 41715.00,
                        "total_completed_stored": 1223640.00,
                        "percentage": 88.0,
                        "balance_to_finish": 166860.00,
                        "retainage": 61182.00
                    },
                    {
                        "item": "05 00 00",
                        "description": "Metals",
                        "scheduled_value": 3245000.00,
                        "work_completed_previous": 2271500.00,
                        "work_completed_this_period": 324500.00,
                        "materials_stored": 129800.00,
                        "total_completed_stored": 2725800.00,
                        "percentage": 84.0,
                        "balance_to_finish": 519200.00,
                        "retainage": 136290.00
                    },
                    {
                        "item": "06 00 00",
                        "description": "Wood, Plastics, and Composites",
                        "scheduled_value": 925000.00,
                        "work_completed_previous": 555000.00,
                        "work_completed_this_period": 185000.00,
                        "materials_stored": 37000.00,
                        "total_completed_stored": 777000.00,
                        "percentage": 84.0,
                        "balance_to_finish": 148000.00,
                        "retainage": 38850.00
                    },
                    {
                        "item": "07 00 00",
                        "description": "Thermal and Moisture Protection",
                        "scheduled_value": 2775000.00,
                        "work_completed_previous": 1665000.00,
                        "work_completed_this_period": 277500.00,
                        "materials_stored": 111000.00,
                        "total_completed_stored": 2053500.00,
                        "percentage": 74.0,
                        "balance_to_finish": 721500.00,
                        "retainage": 102675.00
                    },
                    {
                        "item": "08 00 00",
                        "description": "Openings",
                        "scheduled_value": 3700000.00,
                        "work_completed_previous": 2220000.00,
                        "work_completed_this_period": 555000.00,
                        "materials_stored": 148000.00,
                        "total_completed_stored": 2923000.00,
                        "percentage": 79.0,
                        "balance_to_finish": 777000.00,
                        "retainage": 146150.00
                    },
                    {
                        "item": "09 00 00",
                        "description": "Finishes",
                        "scheduled_value": 5550000.00,
                        "work_completed_previous": 1665000.00,
                        "work_completed_this_period": 832500.00,
                        "materials_stored": 222000.00,
                        "total_completed_stored": 2719500.00,
                        "percentage": 49.0,
                        "balance_to_finish": 2830500.00,
                        "retainage": 135975.00
                    },
                    {
                        "item": "10 00 00",
                        "description": "Specialties",
                        "scheduled_value": 1387500.00,
                        "work_completed_previous": 416250.00,
                        "work_completed_this_period": 277500.00,
                        "materials_stored": 55500.00,
                        "total_completed_stored": 749250.00,
                        "percentage": 54.0,
                        "balance_to_finish": 638250.00,
                        "retainage": 37462.50
                    },
                    {
                        "item": "11 00 00",
                        "description": "Equipment",
                        "scheduled_value": 925000.00,
                        "work_completed_previous": 185000.00,
                        "work_completed_this_period": 185000.00,
                        "materials_stored": 92500.00,
                        "total_completed_stored": 462500.00,
                        "percentage": 50.0,
                        "balance_to_finish": 462500.00,
                        "retainage": 23125.00
                    },
                    {
                        "item": "12 00 00",
                        "description": "Furnishings",
                        "scheduled_value": 462500.00,
                        "work_completed_previous": 0.00,
                        "work_completed_this_period": 46250.00,
                        "materials_stored": 23125.00,
                        "total_completed_stored": 69375.00,
                        "percentage": 15.0,
                        "balance_to_finish": 393125.00,
                        "retainage": 3468.75
                    },
                    {
                        "item": "13 00 00",
                        "description": "Special Construction",
                        "scheduled_value": 1850000.00,
                        "work_completed_previous": 370000.00,
                        "work_completed_this_period": 277500.00,
                        "materials_stored": 74000.00,
                        "total_completed_stored": 721500.00,
                        "percentage": 39.0,
                        "balance_to_finish": 1128500.00,
                        "retainage": 36075.00
                    },
                    {
                        "item": "14 00 00",
                        "description": "Conveying Equipment",
                        "scheduled_value": 1387500.00,
                        "work_completed_previous": 277500.00,
                        "work_completed_this_period": 277500.00,
                        "materials_stored": 69375.00,
                        "total_completed_stored": 624375.00,
                        "percentage": 45.0,
                        "balance_to_finish": 763125.00,
                        "retainage": 31218.75
                    },
                    {
                        "item": "15 00 00",
                        "description": "Mechanical",
                        "scheduled_value": 6937500.00,
                        "work_completed_previous": 2775000.00,
                        "work_completed_this_period": 1387500.00,
                        "materials_stored": 346875.00,
                        "total_completed_stored": 4509375.00,
                        "percentage": 65.0,
                        "balance_to_finish": 2428125.00,
                        "retainage": 225468.75
                    },
                    {
                        "item": "16 00 00",
                        "description": "Electrical",
                        "scheduled_value": 5550000.00,
                        "work_completed_previous": 1887750.00,
                        "work_completed_this_period": 1110000.00,
                        "materials_stored": 222000.00,
                        "total_completed_stored": 3219750.00,
                        "percentage": 58.0,
                        "balance_to_finish": 2330250.00,
                        "retainage": 160987.50
                    }
                ],
                "billing_history": [
                    {
                        "application_number": 8,
                        "period_ending": "2024-05-31",
                        "total_completed_stored": 31524480.00,
                        "total_retainage": 1576224.00,
                        "total_earned_less_retainage": 29948256.00,
                        "less_previous_payments": 27235430.40,
                        "current_payment_due": 2712825.60,
                        "status": "Approved",
                        "approved_date": "2024-06-05"
                    }
                ]
            }
            
        with open(self.data_file_path, 'w') as f:
            json.dump(demo_data, f, indent=2)
    
    def _load_data(self):
        """Load AIA billing data"""
        try:
            with open(self.data_file_path, 'r') as f:
                data = json.load(f)
                # Ensure data is properly structured
                if isinstance(data, list):
                    # If data is a list, return default structure
                    return self._get_default_data()
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return self._get_default_data()
    
    def _get_default_data(self):
        """Get default data structure"""
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
            "schedule_of_values": [
                {
                    "item": "01 00 00",
                    "description": "General Requirements",
                    "scheduled_value": 2275000.00,
                    "work_completed_previous": 2275000.00,
                    "work_completed_this_period": 0.00,
                    "materials_stored": 0.00,
                    "total_completed_stored": 2275000.00,
                    "percentage": 100.0,
                    "balance_to_finish": 0.00,
                    "retainage": 0.00
                }
            ],
            "billing_history": []
        }
    
    def render_g702_application(self):
        """Render AIA G702 Application for Payment"""
        st.markdown("### 📋 AIA G702 - Application for Payment")
        
        data = self._load_data()
        project_info = data["project_info"]
        
        # Application Header
        st.markdown("#### Application Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.text_input("Application Number", value="9", key="app_number")
            st.date_input("Application Date", value=datetime.now(), key="app_date")
        
        with col2:
            st.date_input("Period Ending", value=datetime.now().replace(day=31), key="period_ending")
            st.text_input("Project Number", value=project_info["project_number"], key="proj_number")
        
        with col3:
            st.selectbox("Application Status", ["Draft", "Submitted", "Under Review", "Approved"], key="app_status")
        
        # Project Information
        st.markdown("#### Project Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Project Name", value=project_info["project_name"], key="proj_name")
            st.text_input("Location", value=project_info["location"], key="location")
            st.text_input("Architect", value=project_info["architect"], key="architect")
        
        with col2:
            st.text_input("Owner", value=project_info["owner"], key="owner")
            st.text_input("Contractor", value=project_info["contractor"], key="contractor")
            st.date_input("Contract Date", value=datetime.strptime(project_info["contract_date"], "%Y-%m-%d"), key="contract_date")
        
        # Contract Summary
        st.markdown("#### Contract Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Original Contract Amount", f"${project_info['contract_amount']:,.2f}")
        
        with col2:
            st.metric("Change Orders", f"${project_info['change_order_amount']:,.2f}")
        
        with col3:
            st.metric("Adjusted Contract Amount", f"${project_info['adjusted_contract_amount']:,.2f}")
        
        with col4:
            # Calculate totals from schedule of values
            schedule_df = pd.DataFrame(data["schedule_of_values"])
            total_completed = schedule_df['total_completed_stored'].sum()
            completion_percentage = (total_completed / project_info['adjusted_contract_amount']) * 100
            st.metric("Overall Completion", f"{completion_percentage:.1f}%")
    
    def render_g703_schedule(self):
        """Render AIA G703 Schedule of Values"""
        st.markdown("### 📊 AIA G703 - Schedule of Values")
        
        data = self._load_data()
        schedule_df = pd.DataFrame(data["schedule_of_values"])
        
        # Calculate summary totals
        total_scheduled = schedule_df['scheduled_value'].sum()
        total_previous = schedule_df['work_completed_previous'].sum()
        total_this_period = schedule_df['work_completed_this_period'].sum()
        total_materials = schedule_df['materials_stored'].sum()
        total_completed_stored = schedule_df['total_completed_stored'].sum()
        total_retainage = schedule_df['retainage'].sum()
        total_earned_less_retainage = total_completed_stored - total_retainage
        
        # Summary metrics
        st.markdown("#### Summary Totals")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Scheduled Value", f"${total_scheduled:,.2f}")
            st.metric("Total This Period", f"${total_this_period:,.2f}")
        
        with col2:
            st.metric("Total Previous", f"${total_previous:,.2f}")
            st.metric("Materials Stored", f"${total_materials:,.2f}")
        
        with col3:
            st.metric("Total Completed & Stored", f"${total_completed_stored:,.2f}")
            st.metric("Total Retainage", f"${total_retainage:,.2f}")
        
        with col4:
            completion_pct = (total_completed_stored / total_scheduled) * 100
            st.metric("Overall Completion", f"{completion_pct:.1f}%")
            st.metric("Earned Less Retainage", f"${total_earned_less_retainage:,.2f}")
        
        # Schedule of Values Table
        st.markdown("#### Schedule of Values Detail")
        
        # Format the dataframe for display
        display_df = schedule_df.copy()
        
        # Format monetary columns
        money_columns = ['scheduled_value', 'work_completed_previous', 'work_completed_this_period', 
                        'materials_stored', 'total_completed_stored', 'balance_to_finish', 'retainage']
        
        for col in money_columns:
            display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
        
        display_df['percentage'] = display_df['percentage'].apply(lambda x: f"{x:.1f}%")
        
        # Rename columns for display
        display_df = display_df.rename(columns={
            'item': 'Item #',
            'description': 'Description',
            'scheduled_value': 'Scheduled Value',
            'work_completed_previous': 'Work Completed (Previous)',
            'work_completed_this_period': 'Work Completed (This Period)',
            'materials_stored': 'Materials Stored',
            'total_completed_stored': 'Total Completed & Stored',
            'percentage': '% Complete',
            'balance_to_finish': 'Balance to Finish',
            'retainage': 'Retainage'
        })
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Payment calculation
        st.markdown("#### Payment Calculation")
        
        # Get previous payments from billing history
        billing_history = data.get("billing_history", [])
        previous_payments = sum([bill["current_payment_due"] for bill in billing_history])
        
        current_payment_due = total_earned_less_retainage - previous_payments
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Payment Summary:**")
            st.text(f"Total Earned Less Retainage: ${total_earned_less_retainage:,.2f}")
            st.text(f"Less Previous Payments: ${previous_payments:,.2f}")
            st.text(f"Current Payment Due: ${current_payment_due:,.2f}")
        
        with col2:
            st.markdown("**Retainage Information:**")
            retainage_rate = 5.0  # 5% retainage rate
            st.text(f"Retainage Rate: {retainage_rate}%")
            st.text(f"Total Retainage Held: ${total_retainage:,.2f}")
            st.text(f"Balance to Complete: ${total_scheduled - total_completed_stored:,.2f}")
    
    def render_billing_history(self):
        """Render billing history and previous applications"""
        st.markdown("### 📈 Billing History")
        
        data = self._load_data()
        billing_history = data.get("billing_history", [])
        
        if billing_history:
            # Convert to DataFrame for display
            history_df = pd.DataFrame(billing_history)
            
            # Format monetary columns
            money_columns = ['total_completed_stored', 'total_retainage', 'total_earned_less_retainage', 
                            'less_previous_payments', 'current_payment_due']
            
            for col in money_columns:
                history_df[col] = history_df[col].apply(lambda x: f"${x:,.2f}")
            
            # Rename columns for display
            history_df = history_df.rename(columns={
                'application_number': 'App #',
                'period_ending': 'Period Ending',
                'total_completed_stored': 'Total Completed & Stored',
                'total_retainage': 'Total Retainage',
                'total_earned_less_retainage': 'Earned Less Retainage',
                'less_previous_payments': 'Less Previous Payments',
                'current_payment_due': 'Current Payment Due',
                'status': 'Status',
                'approved_date': 'Approved Date'
            })
            
            st.dataframe(history_df, use_container_width=True, hide_index=True)
        else:
            st.info("No billing history available yet.")
    
    def render_export_options(self):
        """Render export options for PDF and Excel"""
        st.markdown("### 📥 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export PDF", type="primary", use_container_width=True):
                st.success("AIA G702/G703 PDF generated successfully!")
                st.info("In production, this would generate a properly formatted AIA PDF document.")
        
        with col2:
            if st.button("📊 Export Excel", type="secondary", use_container_width=True):
                st.success("Excel workbook exported successfully!")
                st.info("In production, this would export a comprehensive Excel workbook with all data.")
        
        with col3:
            if st.button("📧 Email Application", type="secondary", use_container_width=True):
                st.success("Application emailed to stakeholders!")
                st.info("In production, this would email the application to the owner and architect.")

def render_aia_billing():
    """Main render function for AIA G702/G703 billing module"""
    aia_billing = AIABillingModule()
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["G702 Application", "G703 Schedule", "Billing History", "Export"])
    
    with tab1:
        aia_billing.render_g702_application()
    
    with tab2:
        aia_billing.render_g703_schedule()
    
    with tab3:
        aia_billing.render_billing_history()
    
    with tab4:
        aia_billing.render_export_options()