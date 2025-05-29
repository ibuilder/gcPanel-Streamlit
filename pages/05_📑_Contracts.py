"""
Contracts Management Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

st.set_page_config(
    page_title="Contracts - gcPanel",
    page_icon="📑",
    layout="wide"
)

# Initialize session state
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📑 Contracts Management")
st.markdown("Highland Tower Development - Contract Administration")
st.markdown("---")

# Initialize contracts in session state if not exists
if 'contracts' not in st.session_state:
    st.session_state.contracts = [
        {
            "id": "CNT-001",
            "title": "Prime Construction Contract",
            "contractor": "Highland Construction LLC",
            "contract_value": 45500000,
            "start_date": "2024-01-15",
            "end_date": "2025-12-15",
            "status": "Active",
            "type": "Prime Contract",
            "project_manager": "Sarah Johnson"
        },
        {
            "id": "CNT-002",
            "title": "Structural Steel Subcontract",
            "contractor": "Steel Works Inc.",
            "contract_value": 3200000,
            "start_date": "2024-06-01",
            "end_date": "2024-12-31",
            "status": "Active",
            "type": "Subcontract",
            "project_manager": "Mike Chen"
        }
    ]

# Main content
tab1, tab2 = st.tabs(["📊 Contracts Database", "📝 Create New Contract"])

with tab1:
    st.subheader("📝 Create New Contract")
    
    with st.form("contract_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            contract_title = st.text_input("Contract Title*", placeholder="Description of contract")
            contractor = st.text_input("Contractor/Vendor*", placeholder="Company name")
            contract_value = st.number_input("Contract Value ($)*", min_value=0.0, format="%.2f")
            contract_type = st.selectbox("Contract Type", 
                ["Prime Contract", "Subcontract", "Purchase Order", "Service Agreement", "Change Order"])
        
        with col2:
            start_date = st.date_input("Start Date*")
            end_date = st.date_input("End Date*")
            project_manager = st.text_input("Project Manager", placeholder="Assigned project manager")
            payment_terms = st.selectbox("Payment Terms", 
                ["Net 30", "Net 15", "Progress Payments", "Upon Completion", "Other"])
        
        scope_of_work = st.text_area("Scope of Work", height=100,
            placeholder="Detailed description of work to be performed...")
        
        special_conditions = st.text_area("Special Conditions", height=80,
            placeholder="Any special terms or conditions...")
        
        submitted = st.form_submit_button("📄 Create Contract", type="primary", use_container_width=True)
        
        if submitted and contract_title and contractor and contract_value > 0:
            new_contract = {
                "id": f"CNT-{len(st.session_state.contracts) + 1:03d}",
                "title": contract_title,
                "contractor": contractor,
                "contract_value": contract_value,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "status": "Draft",
                "type": contract_type,
                "project_manager": project_manager,
                "payment_terms": payment_terms,
                "scope_of_work": scope_of_work,
                "special_conditions": special_conditions,
                "created_date": str(date.today()),
                "created_by": st.session_state.get('user_name', 'User')
            }
            st.session_state.contracts.insert(0, new_contract)
            st.success(f"Contract {new_contract['id']} created successfully!")
            st.rerun()
        elif submitted:
            st.error("Please fill in all required fields (*)")

with tab2:
    st.subheader("📊 Contracts Database")
    
    if st.session_state.contracts:
        df = pd.DataFrame(st.session_state.contracts)
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search contracts...", placeholder="Search by title, contractor, or ID")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Draft", "Active", "Completed", "Terminated"])
        with col3:
            type_filter = st.selectbox("Type", ["All", "Prime Contract", "Subcontract", "Purchase Order", "Service Agreement"])
        
        # Filter data
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[
                filtered_df.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)
            ]
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
        
        # Display results
        st.write(f"**Total Contracts:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            # Format contract values for display
            display_df = filtered_df.copy()
            display_df['Contract Value'] = display_df['contract_value'].apply(lambda x: f"${x:,.2f}")
            
            # Display with column configuration
            st.dataframe(
                clean_dataframe_for_display(display_df),
                column_config={
                    "id": st.column_config.TextColumn("Contract ID"),
                    "title": st.column_config.TextColumn("Title"),
                    "contractor": st.column_config.TextColumn("Contractor"),
                    "Contract Value": st.column_config.TextColumn("Contract Value"),
                    "start_date": st.column_config.DateColumn("Start Date"),
                    "end_date": st.column_config.DateColumn("End Date"),
                    "status": st.column_config.SelectboxColumn("Status", 
                        options=["Draft", "Active", "Completed", "Terminated"]),
                    "type": st.column_config.TextColumn("Type")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No contracts found matching your criteria.")
    else:
        st.info("No contracts available. Create your first contract above!")

# Contract summary statistics
st.markdown("---")
st.subheader("📈 Contract Summary")

if st.session_state.contracts:
    df = pd.DataFrame(st.session_state.contracts)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_contracts = len(df)
        st.metric("Total Contracts", total_contracts)
    
    with col2:
        active_contracts = len(df[df['status'] == 'Active'])
        st.metric("Active Contracts", active_contracts)
    
    with col3:
        total_value = df['contract_value'].sum()
        st.metric("Total Contract Value", f"${total_value:,.0f}")
    
    with col4:
        avg_value = df['contract_value'].mean()
        st.metric("Average Contract Value", f"${avg_value:,.0f}")
    
    # Contract value by type chart
    if len(df) > 0:
        st.markdown("**Contract Value by Type**")
        type_summary = df.groupby('type')['contract_value'].sum().reset_index()
        
        import plotly.express as px
        fig = px.pie(type_summary, values='contract_value', names='type', 
                    title="Contract Value Distribution")
        st.plotly_chart(fig, use_container_width=True)