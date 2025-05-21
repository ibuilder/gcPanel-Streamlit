"""
Integrated Contracts Module with Digital Signature Support.

This module provides comprehensive contract management with embedded
digital signature capabilities directly in the forms.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from modules.contracts.components.signature_enabled_forms import (
    change_order_with_signatures,
    subcontract_with_signatures,
    invoice_with_signatures
)

def render_integrated_contracts():
    """
    Render the contracts module with integrated digital signature capabilities.
    """
    st.title("Contracts Management")
    
    # Create tabs for different contract types
    tabs = st.tabs(["Change Orders", "Subcontracts", "Invoices", "Contract Log"])
    
    # Change Orders tab
    with tabs[0]:
        change_order_with_signatures()
    
    # Subcontracts tab
    with tabs[1]:
        subcontract_with_signatures()
    
    # Invoices tab
    with tabs[2]:
        invoice_with_signatures()
    
    # Contract Log tab - for displaying all contracts
    with tabs[3]:
        render_contract_log()

def render_contract_log():
    """Render a log of all contracts with their signature status."""
    st.header("Contract Log")
    
    # Sample contract data
    contracts_data = {
        "Number": ["SC-2025-001", "SC-2025-038", "CO-2025-015", "INV-2025-087", "CO-2025-042"],
        "Type": ["Subcontract", "Subcontract", "Change Order", "Invoice", "Change Order"],
        "Date": ["2025-01-15", "2025-03-22", "2025-04-05", "2025-04-15", "2025-05-10"],
        "Description": ["Excavation", "Concrete", "Added Roof Drains", "March Progress", "Added Security"],
        "Amount": [1250000.00, 3750000.00, 28500.00, 450000.00, 36750.00],
        "Status": ["Executed", "Executed", "Approved", "Paid", "Pending"],
        "Signatures": ["Complete", "Complete", "Complete", "Complete", "Incomplete"]
    }
    
    # Convert to DataFrame
    contracts_df = pd.DataFrame(contracts_data)
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        type_filter = st.multiselect(
            "Contract Type",
            options=["All Types"] + list(contracts_df["Type"].unique()),
            default="All Types"
        )
    with col2:
        status_filter = st.multiselect(
            "Status",
            options=["All Statuses"] + list(contracts_df["Status"].unique()),
            default="All Statuses"
        )
    with col3:
        signature_filter = st.multiselect(
            "Signature Status",
            options=["All", "Complete", "Incomplete"],
            default="All"
        )
    
    # Apply filters
    filtered_df = contracts_df.copy()
    
    if type_filter and "All Types" not in type_filter:
        filtered_df = filtered_df[filtered_df["Type"].isin(type_filter)]
        
    if status_filter and "All Statuses" not in status_filter:
        filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]
        
    if signature_filter and "All" not in signature_filter:
        filtered_df = filtered_df[filtered_df["Signatures"].isin(signature_filter)]
    
    # Display the filtered contracts
    st.dataframe(
        filtered_df,
        use_container_width=True,
        column_config={
            "Amount": st.column_config.NumberColumn(format="$%.2f"),
            "Status": st.column_config.Column(
                width="medium",
                help="Current status of the contract"
            ),
            "Signatures": st.column_config.Column(
                width="medium",
                help="Status of required signatures"
            )
        }
    )
    
    # Add a button to create a new contract
    st.button("+ Add New Contract")
    
    # Summary metrics
    st.subheader("Contract Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_contracts = len(contracts_df)
        st.metric("Total Contracts", total_contracts)
    with col2:
        total_value = contracts_df["Amount"].sum()
        st.metric("Total Contract Value", f"${total_value:,.2f}")
    with col3:
        executed_contracts = len(contracts_df[contracts_df["Signatures"] == "Complete"])
        st.metric("Signed Contracts", f"{executed_contracts} ({executed_contracts/total_contracts*100:.0f}%)")
    with col4:
        pending_signatures = len(contracts_df[contracts_df["Signatures"] == "Incomplete"])
        st.metric("Pending Signatures", pending_signatures)