"""
Contracts Management Page - Highland Tower Development
Refactored using MVC pattern with models, controllers, and helpers
"""

import streamlit as st
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from lib.utils.helpers import check_authentication

from lib.models.contract_model import ContractModel
from lib.controllers.crud_controller import CRUDController
from lib.helpers.ui_helpers import format_currency, render_highland_header, apply_highland_tower_styling

# Page configuration
st.set_page_config(page_title="Contracts - gcPanel", page_icon="📑", layout="wide")
# Check authentication
if not check_authentication():
    st.error("🔒 Please log in to access this page")
    st.stop()


# Apply styling
apply_highland_tower_styling()

# Render header
render_highland_header("📑 Contracts Management", "Highland Tower Development - Contract Administration")

# Initialize model and controller
contract_model = ContractModel()

# Display configuration for the contracts module
display_config = {
    'title': 'Contracts',
    'item_name': 'Contract',
    'title_field': 'title',
    'key_fields': ['contract_number', 'contract_name', 'contractor', 'contract_value', 'status'],
    'detail_fields': ['start_date', 'end_date', 'contract_type'],
    'search_fields': ['contract_name', 'contractor', 'contract_number', 'contract_type'],
    'primary_filter': {
        'field': 'status',
        'label': 'Status'
    },
    'secondary_filter': {
        'field': 'status', 
        'label': 'Contract Type'
    },
    'formatters': {
        'contract_value': format_currency
    },
    'column_config': {
        "id": st.column_config.TextColumn("Contract ID"),
        "title": st.column_config.TextColumn("Title"),
        "contractor": st.column_config.TextColumn("Contractor"),
        "contract_value": st.column_config.NumberColumn("Contract Value", format="$%.2f"),
        "start_date": st.column_config.DateColumn("Start Date"),
        "end_date": st.column_config.DateColumn("End Date"),
        "status": st.column_config.SelectboxColumn("Status", 
            options=["Draft", "Active", "Completed", "Terminated"]),
        "type": st.column_config.TextColumn("Type")
    }
}

# Form configuration for creating new contracts
form_config = {
    'fields': [
        {'key': 'title', 'type': 'text', 'label': 'Contract Title', 'placeholder': 'Enter contract title'},
        {'key': 'contractor', 'type': 'text', 'label': 'Contractor', 'placeholder': 'Enter contractor name'},
        {'key': 'contract_value', 'type': 'number', 'label': 'Contract Value ($)', 'min_value': 0.0},
        {'key': 'type', 'type': 'select', 'label': 'Contract Type', 
         'options': ['Prime Contract', 'Subcontract', 'Purchase Order', 'Service Agreement']},
        {'key': 'status', 'type': 'select', 'label': 'Status',
         'options': ['Draft', 'Active', 'Completed', 'Terminated']},
        {'key': 'start_date', 'type': 'date', 'label': 'Start Date'},
        {'key': 'end_date', 'type': 'date', 'label': 'End Date'},
        {'key': 'description', 'type': 'textarea', 'label': 'Description', 'placeholder': 'Enter contract description'},
        {'key': 'project_phase', 'type': 'select', 'label': 'Project Phase',
         'options': ['Phase 1 - Structural', 'Phase 2 - MEP', 'Phase 3 - Envelope', 'Phase 4 - Finishes']},
        {'key': 'retention_percentage', 'type': 'number', 'label': 'Retention %', 'min_value': 0.0},
        {'key': 'payment_terms', 'type': 'select', 'label': 'Payment Terms',
         'options': ['Net 30', 'Net 45', 'Net 60', 'Due on Receipt']}
    ]
}

# Initialize controller
crud_controller = CRUDController(contract_model, 'contracts', display_config)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📊 Contracts Database", "📝 Create New Contract", "📈 Analytics"])

with tab1:
    crud_controller.render_data_view('contracts')

with tab2:
    crud_controller.render_create_form(form_config)

with tab3:
    st.subheader("📈 Contract Analytics")
    
    # Display key metrics using the model
    total_contracts = len(contract_model.get_all())
    active_contracts = len(contract_model.get_active_contracts())
    total_value = contract_model.get_total_contract_value()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Contracts", total_contracts)
    
    with col2:
        st.metric("Active Contracts", active_contracts)
    
    with col3:
        st.metric("Total Value", format_currency(total_value))
    
    with col4:
        completion_rate = (active_contracts / total_contracts * 100) if total_contracts > 0 else 0
        st.metric("Active Rate", f"{completion_rate:.1f}%")
    
    # Contract distribution by type
    st.subheader("Contract Distribution by Type")
    contracts_df = contract_model.to_dataframe()
    if not contracts_df.empty:
        type_distribution = contracts_df['type'].value_counts()
        st.bar_chart(type_distribution)
    
    # Contract values by phase
    st.subheader("Contract Values by Project Phase")
    if not contracts_df.empty:
        phase_values = contracts_df.groupby('project_phase')['contract_value'].sum()
        st.bar_chart(phase_values)

# Sidebar with additional contract information
with st.sidebar:
    st.header("Contract Summary")
    
    contracts = contract_model.get_all()
    if contracts:
        active_contracts = contract_model.get_active_contracts()
        
        st.metric("Highland Tower Contracts", len(contracts))
        st.metric("Currently Active", len(active_contracts))
        
        # Show recent contracts
        st.subheader("Recent Contracts")
        recent_contracts = sorted(contracts, key=lambda x: x.get('created_at', ''), reverse=True)[:3]
        
        for contract in recent_contracts:
            with st.expander(f"📋 {contract['title'][:30]}..."):
                st.write(f"**Contractor:** {contract['contractor']}")
                st.write(f"**Value:** {format_currency(contract['contract_value'])}")
                st.write(f"**Status:** {contract['status']}")
    
    st.markdown("---")
    st.write("**Highland Tower Development**")
    st.write("$45.5M Mixed-Use Project")
    st.write("Contract management powered by gcPanel")