"""
Contracts module for the gcPanel Construction Management Dashboard.

This module provides contract management functionality including contract tracking,
change orders, payment applications, and subcontractor management.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_contracts():
    """Render the contracts management interface."""
    st.header("Contracts")
    
    # Create tabs for different contract functions
    tabs = st.tabs(["Overview", "Subcontracts", "Change Orders", "Payment Applications"])
    
    # Contract Overview Tab
    with tabs[0]:
        render_contract_overview()
    
    # Subcontracts Tab
    with tabs[1]:
        render_subcontracts()
    
    # Change Orders Tab
    with tabs[2]:
        render_change_orders()
        
    # Payment Applications Tab
    with tabs[3]:
        render_payment_applications()

def render_contract_overview():
    """Render the contract overview with metrics and summaries."""
    st.subheader("Contract Overview")
    
    # Key Contract Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Contract Value", "$42.5M", "+$1.2M this quarter")
    with col2:
        st.metric("Open Change Orders", "$850K", "+$120K since last month")
    with col3:
        st.metric("Billed to Date", "$18.3M", "43% of contract value")
    
    # Project Contract Summary
    st.subheader("Project Contract Summary")
    
    contract_summary = [
        {"project": "Highland Tower", "original_value": "$15,500,000", "change_orders": "$320,000", "revised_value": "$15,820,000", "billed": "$6,750,000", "remaining": "$9,070,000"},
        {"project": "City Center", "original_value": "$12,200,000", "change_orders": "$450,000", "revised_value": "$12,650,000", "billed": "$8,200,000", "remaining": "$4,450,000"},
        {"project": "Riverside Apartments", "original_value": "$8,800,000", "change_orders": "$80,000", "revised_value": "$8,880,000", "billed": "$2,100,000", "remaining": "$6,780,000"},
        {"project": "Metro Office Complex", "original_value": "$6,000,000", "change_orders": "$0", "revised_value": "$6,000,000", "billed": "$1,250,000", "remaining": "$4,750,000"}
    ]
    
    st.dataframe(pd.DataFrame(contract_summary), use_container_width=True)
    
    # Billing Progress Chart
    st.subheader("Billing Progress")
    
    # Data for billing progress
    billing_data = {
        'Project': ['Highland Tower', 'City Center', 'Riverside Apartments', 'Metro Office'],
        'Billed %': [43, 65, 24, 21]
    }
    
    billing_df = pd.DataFrame(billing_data)
    st.bar_chart(billing_df.set_index('Project'), color='#1e3a8a')
    
    # Recent Contract Activities
    st.subheader("Recent Contract Activities")
    
    activities = [
        {"date": "2025-05-15", "project": "Highland Tower", "activity": "Change Order #8 Approved", "amount": "$45,000"},
        {"date": "2025-05-14", "project": "City Center", "activity": "Payment Application #12 Submitted", "amount": "$780,000"},
        {"date": "2025-05-10", "project": "Highland Tower", "activity": "Subcontract Executed - MEP Systems", "amount": "$2,200,000"},
        {"date": "2025-05-05", "project": "Riverside Apartments", "activity": "Change Order #3 Rejected", "amount": "$28,000"},
        {"date": "2025-05-01", "project": "Metro Office", "activity": "Payment Application #2 Approved", "amount": "$450,000"}
    ]
    
    activities_df = pd.DataFrame(activities)
    st.dataframe(activities_df, use_container_width=True)

def render_subcontracts():
    """Render the subcontracts interface."""
    st.subheader("Subcontracts")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("Add Subcontract", key="add_subcontract")
    with col2:
        st.button("Subcontractor Report", key="subcontractor_report")
    
    # Add filter options
    with st.expander("Filter Options"):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Project", ["All Projects", "Highland Tower", "City Center", "Riverside Apartments", "Metro Office"])
            st.selectbox("Trade", ["All Trades", "Concrete", "Steel", "Carpentry", "Electrical", "Plumbing", "HVAC", "Finishes"])
        with col2:
            st.selectbox("Status", ["All Statuses", "Pending", "Executed", "Complete", "Terminated"])
            st.text_input("Search Subcontractor")
    
    # Sample subcontract data
    subcontracts = [
        {"id": 1, "project": "Highland Tower", "subcontractor": "ABC Concrete, Inc.", "trade": "Concrete", "value": "$1,850,000", "executed_date": "2025-01-15", "status": "In Progress"},
        {"id": 2, "project": "Highland Tower", "subcontractor": "Steel Experts LLC", "trade": "Steel", "value": "$2,100,000", "executed_date": "2025-01-20", "status": "In Progress"},
        {"id": 3, "project": "City Center", "subcontractor": "Modern Electrical Co.", "trade": "Electrical", "value": "$1,750,000", "executed_date": "2024-11-10", "status": "In Progress"},
        {"id": 4, "project": "Riverside Apartments", "subcontractor": "Quality Plumbing Services", "trade": "Plumbing", "value": "$980,000", "executed_date": "2025-03-05", "status": "In Progress"},
        {"id": 5, "project": "City Center", "subcontractor": "Premier Drywall, Inc.", "trade": "Finishes", "value": "$950,000", "executed_date": "2024-12-01", "status": "Complete"}
    ]
    
    # Convert to DataFrame
    subcontracts_df = pd.DataFrame(subcontracts)
    
    # Add status styling
    def status_color(val):
        if val == "Complete":
            return 'background-color: #d1fae5; color: #064e3b'
        elif val == "In Progress":
            return 'background-color: #e0f2fe; color: #0c4a6e'
        else:
            return 'background-color: #fee2e2; color: #7f1d1d'
    
    # Apply styling
    styled_df = subcontracts_df.style.applymap(status_color, subset=['status'])
    
    # Display the dataframe
    st.dataframe(styled_df, use_container_width=True)
    
    # Sample subcontract detail
    if st.button("View Sample Subcontract Details", key="view_subcontract"):
        st.subheader("Subcontract: ABC Concrete, Inc.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Project:** Highland Tower")
            st.markdown("**Trade:** Concrete")
            st.markdown("**Value:** $1,850,000")
        with col2:
            st.markdown("**Status:** In Progress")
            st.markdown("**Executed Date:** January 15, 2025")
            st.markdown("**Completion %:** 45%")
        
        st.markdown("### Scope of Work")
        st.markdown("""
        - Foundation excavation and preparation
        - Reinforced concrete foundations and footings
        - Concrete slabs for floors 1-20
        - Concrete columns and shear walls
        - Concrete finishing for exposed surfaces
        """)
        
        st.markdown("### Payment Schedule")
        payment_schedule = {
            "Milestone": ["Mobilization", "Foundations Complete", "Floor 10 Complete", "Floor 20 Complete", "Final Completion"],
            "Percentage": ["10%", "25%", "25%", "25%", "15%"],
            "Amount": ["$185,000", "$462,500", "$462,500", "$462,500", "$277,500"],
            "Status": ["Paid", "Paid", "In Progress", "Not Started", "Not Started"]
        }
        
        st.dataframe(pd.DataFrame(payment_schedule), use_container_width=True)
        
        st.markdown("### Change Orders")
        change_orders = {
            "CO #": ["CO-001", "CO-002"],
            "Description": ["Additional foundation work due to soil conditions", "Upgrade to exposed concrete finish in lobby"],
            "Amount": ["$45,000", "$28,000"],
            "Status": ["Approved", "Pending"]
        }
        
        st.dataframe(pd.DataFrame(change_orders), use_container_width=True)

def render_change_orders():
    """Render the change orders interface."""
    st.subheader("Change Orders")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("New Change Order", key="new_change_order")
    with col2:
        st.button("Change Order Log", key="change_order_log")
    
    # Add filter options
    with st.expander("Filter Options"):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Project", ["All Projects", "Highland Tower", "City Center", "Riverside Apartments", "Metro Office"], key="co_project")
            st.selectbox("Type", ["All Types", "Owner Change", "Design Change", "Field Condition", "Value Engineering"], key="co_type")
        with col2:
            st.selectbox("Status", ["All Statuses", "Draft", "Submitted", "Approved", "Rejected"], key="co_status")
            st.date_input("Date Range", datetime.now() - timedelta(days=90), key="co_date")
    
    # Change order summary
    st.subheader("Change Order Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Change Orders", "24", "+3 this month")
    with col2:
        st.metric("Approved", "$850,000", "+$120K since last month")
    with col3:
        st.metric("Pending", "$215,000", "5 open items")
    with col4:
        st.metric("Rejected", "$95,000", "3 items")
    
    # Sample change order data
    change_orders = [
        {"id": "CO-008", "project": "Highland Tower", "description": "Additional glass facade feature", "type": "Owner Change", "amount": "$115,000", "submitted": "2025-05-10", "status": "Pending"},
        {"id": "CO-007", "project": "Highland Tower", "description": "Upgrade electrical system in penthouse", "type": "Design Change", "amount": "$45,000", "submitted": "2025-05-01", "status": "Approved"},
        {"id": "CO-012", "project": "City Center", "description": "Revise foundation due to utility conflict", "type": "Field Condition", "amount": "$78,000", "submitted": "2025-04-28", "status": "Approved"},
        {"id": "CO-004", "project": "Riverside Apartments", "description": "Add rooftop solar array", "type": "Value Engineering", "amount": "$220,000", "submitted": "2025-04-15", "status": "Approved"},
        {"id": "CO-003", "project": "Riverside Apartments", "description": "Revise landscape design", "type": "Owner Change", "amount": "$28,000", "submitted": "2025-04-10", "status": "Rejected"}
    ]
    
    # Convert to DataFrame
    change_orders_df = pd.DataFrame(change_orders)
    
    # Add status styling
    def co_status_color(val):
        if val == "Approved":
            return 'background-color: #d1fae5; color: #064e3b'
        elif val == "Pending":
            return 'background-color: #e0f2fe; color: #0c4a6e'
        else:
            return 'background-color: #fee2e2; color: #7f1d1d'
    
    # Apply styling
    styled_co_df = change_orders_df.style.applymap(co_status_color, subset=['status'])
    
    # Display the dataframe
    st.dataframe(styled_co_df, use_container_width=True)
    
    # Change order distribution chart
    st.subheader("Change Order Distribution by Type")
    
    co_types = {
        'Type': ['Owner Change', 'Design Change', 'Field Condition', 'Value Engineering'],
        'Amount': [320000, 230000, 180000, 120000]
    }
    
    co_types_df = pd.DataFrame(co_types)
    st.bar_chart(co_types_df.set_index('Type'), color='#1e3a8a')

def render_payment_applications():
    """Render the payment applications interface."""
    st.subheader("Payment Applications")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("New Payment App", key="new_payment_app")
    with col2:
        st.button("Payment Report", key="payment_report")
    
    # Add filter options
    with st.expander("Filter Options"):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Project", ["All Projects", "Highland Tower", "City Center", "Riverside Apartments", "Metro Office"], key="pa_project")
            st.selectbox("Status", ["All Statuses", "Draft", "Submitted", "Approved", "Paid"], key="pa_status")
        with col2:
            st.date_input("From Date", datetime.now() - timedelta(days=90), key="pa_from_date")
            st.date_input("To Date", datetime.now(), key="pa_to_date")
    
    # Sample payment application data
    payment_apps = [
        {"id": "PA-012", "project": "City Center", "period": "April 2025", "amount": "$780,000", "submitted": "2025-05-14", "status": "Submitted"},
        {"id": "PA-011", "project": "Highland Tower", "period": "April 2025", "amount": "$650,000", "submitted": "2025-05-10", "status": "Approved"},
        {"id": "PA-010", "project": "Riverside Apartments", "period": "April 2025", "amount": "$320,000", "submitted": "2025-05-08", "status": "Paid"},
        {"id": "PA-009", "project": "City Center", "period": "March 2025", "amount": "$720,000", "submitted": "2025-04-10", "status": "Paid"},
        {"id": "PA-008", "project": "Highland Tower", "period": "March 2025", "amount": "$680,000", "submitted": "2025-04-08", "status": "Paid"}
    ]
    
    # Convert to DataFrame
    payment_apps_df = pd.DataFrame(payment_apps)
    
    # Add status styling
    def pa_status_color(val):
        if val == "Paid":
            return 'background-color: #d1fae5; color: #064e3b'
        elif val == "Approved":
            return 'background-color: #fef3c7; color: #78350f'
        elif val == "Submitted":
            return 'background-color: #e0f2fe; color: #0c4a6e'
        else:
            return 'background-color: #f5f5f4; color: #44403c'
    
    # Apply styling
    styled_pa_df = payment_apps_df.style.applymap(pa_status_color, subset=['status'])
    
    # Display the dataframe
    st.dataframe(styled_pa_df, use_container_width=True)
    
    # Cash flow chart
    st.subheader("Project Cash Flow")
    
    # Generate sample cash flow data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cash_flow_data = pd.DataFrame({
        'Month': months,
        'Highland Tower': [450, 520, 680, 650, 700, 750, 800, 850, 900, 950, 1000, 1100],
        'City Center': [650, 690, 720, 780, 800, 750, 700, 650, 600, 550, 500, 450],
        'Riverside Apartments': [0, 0, 280, 320, 380, 450, 550, 600, 650, 700, 750, 800],
        'Metro Office': [0, 0, 0, 200, 250, 300, 350, 400, 450, 500, 550, 600]
    })
    
    # Melt the DataFrame for easier plotting
    cash_flow_melted = pd.melt(cash_flow_data, id_vars=['Month'], var_name='Project', value_name='Amount ($K)')
    
    # Create a temporary pivot table for the chart
    cash_flow_pivot = cash_flow_melted.pivot(index='Month', columns='Project', values='Amount ($K)')
    
    # Plot the cash flow chart
    st.line_chart(cash_flow_pivot)