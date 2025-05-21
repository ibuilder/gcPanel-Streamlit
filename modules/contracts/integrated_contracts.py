"""
Integrated Contracts Module with Digital Signature Support and CRUD Functionality.

This module provides comprehensive contract management with embedded
digital signature capabilities and full CRUD operations.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from modules.contracts.components.signature_enabled_forms import (
    change_order_with_signatures,
    subcontract_with_signatures,
    invoice_with_signatures
)

# Initialize directory for contract data if it doesn't exist
os.makedirs("data/contracts", exist_ok=True)

# Contract data filenames
CHANGE_ORDERS_FILE = "data/contracts/change_orders.json"
SUBCONTRACTS_FILE = "data/contracts/subcontracts.json"
INVOICES_FILE = "data/contracts/invoices.json"

def initialize_contract_data():
    """Initialize contract data files if they don't exist."""
    # Sample change orders data
    if not os.path.exists(CHANGE_ORDERS_FILE):
        sample_change_orders = [
            {
                "id": "CO-2025-001",
                "project": "Highland Tower Development",
                "date": "2025-02-10",
                "status": "Approved",
                "description": "Added Roof Drains",
                "reason": "Owner Request",
                "original_amount": 45500000.00,
                "previous_changes": 0.00,
                "this_change": 28500.00,
                "days_added": 2,
                "signatures": ["Contractor: John Doe", "Owner: Jane Smith"],
                "created_at": "2025-02-10",
                "updated_at": "2025-02-15"
            },
            {
                "id": "CO-2025-042",
                "project": "Highland Tower Development",
                "date": "2025-05-10",
                "status": "Pending Approval",
                "description": "Added Security Equipment",
                "reason": "Owner Request",
                "original_amount": 45500000.00,
                "previous_changes": 124500.00,
                "this_change": 36750.00,
                "days_added": 3,
                "signatures": ["Contractor: John Doe"],
                "created_at": "2025-05-10",
                "updated_at": "2025-05-10"
            }
        ]
        with open(CHANGE_ORDERS_FILE, 'w') as f:
            json.dump(sample_change_orders, f, indent=2)
    
    # Sample subcontracts data
    if not os.path.exists(SUBCONTRACTS_FILE):
        sample_subcontracts = [
            {
                "id": "SC-2025-001",
                "project": "Highland Tower Development",
                "date": "2025-01-15",
                "status": "Executed",
                "company": "Deep Excavation Inc.",
                "contact": "Mike Johnson",
                "email": "mike@deepexcavation.com",
                "scope": "Excavation",
                "amount": 1250000.00,
                "start_date": "2025-02-01",
                "completion_date": "2025-04-15",
                "signatures": ["Subcontractor: Mike Johnson", "General Contractor: John Doe"],
                "created_at": "2025-01-10",
                "updated_at": "2025-01-15"
            },
            {
                "id": "SC-2025-038",
                "project": "Highland Tower Development",
                "date": "2025-03-22",
                "status": "Executed",
                "company": "Superior Concrete Solutions",
                "contact": "Sarah Williams",
                "email": "sarah@superiorconcrete.com",
                "scope": "Concrete",
                "amount": 3750000.00,
                "start_date": "2025-04-01",
                "completion_date": "2025-08-15",
                "signatures": ["Subcontractor: Sarah Williams", "General Contractor: John Doe"],
                "created_at": "2025-03-15",
                "updated_at": "2025-03-22"
            }
        ]
        with open(SUBCONTRACTS_FILE, 'w') as f:
            json.dump(sample_subcontracts, f, indent=2)
    
    # Sample invoices data
    if not os.path.exists(INVOICES_FILE):
        sample_invoices = [
            {
                "id": "INV-2025-087",
                "project": "Highland Tower Development",
                "date": "2025-04-15",
                "status": "Paid",
                "description": "March Progress",
                "company": "Superior Concrete Solutions",
                "contract_amount": 3750000.00,
                "approved_changes": 0.00,
                "previously_billed": 0.00,
                "current_billed": 450000.00,
                "retainage": 45000.00,
                "amount_due": 405000.00,
                "signatures": ["Contractor: Sarah Williams", "Owner/CM: Jane Smith"],
                "created_at": "2025-04-15",
                "updated_at": "2025-04-22"
            }
        ]
        with open(INVOICES_FILE, 'w') as f:
            json.dump(sample_invoices, f, indent=2)

def load_contract_data(contract_type):
    """
    Load contract data from JSON file.
    
    Args:
        contract_type (str): Type of contract ("change_orders", "subcontracts", or "invoices")
        
    Returns:
        list: List of contract dictionaries
    """
    file_map = {
        "change_orders": CHANGE_ORDERS_FILE,
        "subcontracts": SUBCONTRACTS_FILE,
        "invoices": INVOICES_FILE
    }
    
    file_path = file_map.get(contract_type)
    if not file_path or not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading contract data: {e}")
        return []

def save_contract_data(contract_type, data):
    """
    Save contract data to JSON file.
    
    Args:
        contract_type (str): Type of contract ("change_orders", "subcontracts", or "invoices")
        data (list): List of contract dictionaries
    """
    file_map = {
        "change_orders": CHANGE_ORDERS_FILE,
        "subcontracts": SUBCONTRACTS_FILE,
        "invoices": INVOICES_FILE
    }
    
    file_path = file_map.get(contract_type)
    if not file_path:
        return
    
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving contract data: {e}")

def render_integrated_contracts():
    """
    Render the contracts module with integrated digital signature capabilities
    and CRUD operations.
    """
    # Initialize contract data files if they don't exist
    initialize_contract_data()
    
    # Initialize session state for CRUD operations if not already present
    if "contracts_view" not in st.session_state:
        st.session_state.contracts_view = "list"
    if "selected_contract_type" not in st.session_state:
        st.session_state.selected_contract_type = "change_orders"
    if "selected_contract_id" not in st.session_state:
        st.session_state.selected_contract_id = None
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False
    
    st.title("Contracts Management")
    
    # Only show tabs in list view
    if st.session_state.contracts_view == "list":
        # Create tabs for different contract types
        tab_names = ["Change Orders", "Subcontracts", "Invoices", "Contract Log"]
        tabs = st.tabs(tab_names)
        
        # Handle each tab's content
        with tabs[0]:
            render_contract_list("change_orders")
        
        with tabs[1]:
            render_contract_list("subcontracts")
        
        with tabs[2]:
            render_contract_list("invoices")
        
        with tabs[3]:
            render_contract_log()
    
    # Detail, edit, or create view for specific contract types
    else:
        # Back button for non-list views
        if st.button("← Back to List"):
            st.session_state.contracts_view = "list"
            st.session_state.selected_contract_id = None
            st.session_state.edit_mode = False
            st.rerun()
        
        # Determine which view to show based on session state
        contract_type = st.session_state.selected_contract_type
        
        if contract_type == "change_orders":
            if st.session_state.contracts_view == "create":
                change_order_with_signatures()
            elif st.session_state.contracts_view == "edit":
                # Get the selected contract data
                contracts = load_contract_data("change_orders")
                selected_contract = next((c for c in contracts if c["id"] == st.session_state.selected_contract_id), None)
                if selected_contract:
                    change_order_with_signatures(edit_mode=True, contract_data=selected_contract)
                else:
                    st.error("Selected change order not found.")
            elif st.session_state.contracts_view == "detail":
                render_change_order_detail()
        
        elif contract_type == "subcontracts":
            if st.session_state.contracts_view == "create":
                subcontract_with_signatures()
            elif st.session_state.contracts_view == "edit":
                # Get the selected contract data
                contracts = load_contract_data("subcontracts")
                selected_contract = next((c for c in contracts if c["id"] == st.session_state.selected_contract_id), None)
                if selected_contract:
                    subcontract_with_signatures(edit_mode=True, contract_data=selected_contract)
                else:
                    st.error("Selected subcontract not found.")
            elif st.session_state.contracts_view == "detail":
                render_subcontract_detail()
        
        elif contract_type == "invoices":
            if st.session_state.contracts_view == "create":
                invoice_with_signatures()
            elif st.session_state.contracts_view == "edit":
                # Get the selected contract data
                contracts = load_contract_data("invoices")
                selected_contract = next((c for c in contracts if c["id"] == st.session_state.selected_contract_id), None)
                if selected_contract:
                    invoice_with_signatures(edit_mode=True, contract_data=selected_contract)
                else:
                    st.error("Selected invoice not found.")
            elif st.session_state.contracts_view == "detail":
                render_invoice_detail()

def render_contract_list(contract_type):
    """
    Render a list of contracts with CRUD options.
    
    Args:
        contract_type (str): Type of contract ("change_orders", "subcontracts", or "invoices")
    """
    # Set heading based on contract type
    type_label = {
        "change_orders": "Change Orders",
        "subcontracts": "Subcontracts",
        "invoices": "Invoices"
    }.get(contract_type, "Contracts")
    
    st.header(type_label)
    
    # Load contract data
    contracts = load_contract_data(contract_type)
    
    # Add search and filter options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("Search", placeholder=f"Search {type_label.lower()}...", key=f"search_{contract_type}")
    
    with col2:
        status_options = ["All Statuses"] + sorted(list(set(c.get("status", "Unknown") for c in contracts)))
        status_filter = st.selectbox("Status", options=status_options, key=f"status_{contract_type}")
    
    with col3:
        # Add a create button
        if st.button(f"+ New {type_label[:-1]}", key=f"new_{contract_type}"):
            st.session_state.contracts_view = "create"
            st.session_state.selected_contract_type = contract_type
            st.session_state.selected_contract_id = None
            st.rerun()
    
    # Filter contracts based on search and status
    filtered_contracts = contracts
    
    if search_term:
        # Search in multiple fields based on contract type
        search_term = search_term.lower()
        if contract_type == "change_orders":
            filtered_contracts = [c for c in filtered_contracts if 
                                search_term in c.get("id", "").lower() or 
                                search_term in c.get("description", "").lower() or
                                search_term in c.get("reason", "").lower()]
        elif contract_type == "subcontracts":
            filtered_contracts = [c for c in filtered_contracts if 
                                search_term in c.get("id", "").lower() or 
                                search_term in c.get("company", "").lower() or
                                search_term in c.get("scope", "").lower()]
        elif contract_type == "invoices":
            filtered_contracts = [c for c in filtered_contracts if 
                                search_term in c.get("id", "").lower() or 
                                search_term in c.get("description", "").lower() or
                                search_term in c.get("company", "").lower()]
    
    if status_filter and status_filter != "All Statuses":
        filtered_contracts = [c for c in filtered_contracts if c.get("status") == status_filter]
    
    # Prepare data for display based on contract type
    if contract_type == "change_orders":
        display_data = [{
            "ID": c.get("id", ""),
            "Date": c.get("date", ""),
            "Description": c.get("description", ""),
            "Amount": c.get("this_change", 0),
            "Status": c.get("status", ""),
            "Signatures": ", ".join(c.get("signatures", [])) if c.get("signatures") else "None"
        } for c in filtered_contracts]
    elif contract_type == "subcontracts":
        display_data = [{
            "ID": c.get("id", ""),
            "Date": c.get("date", ""),
            "Company": c.get("company", ""),
            "Scope": c.get("scope", ""),
            "Amount": c.get("amount", 0),
            "Status": c.get("status", ""),
            "Signatures": len(c.get("signatures", [])) if c.get("signatures") else 0
        } for c in filtered_contracts]
    elif contract_type == "invoices":
        display_data = [{
            "ID": c.get("id", ""),
            "Date": c.get("date", ""),
            "Description": c.get("description", ""),
            "Company": c.get("company", ""),
            "Amount Due": c.get("amount_due", 0),
            "Status": c.get("status", ""),
            "Signatures": len(c.get("signatures", [])) if c.get("signatures") else 0
        } for c in filtered_contracts]
    
    # Convert to DataFrame for display
    if display_data:
        df = pd.DataFrame(display_data)
        
        # Add action buttons to each row
        df["Actions"] = None  # Placeholder column for action buttons
        
        # Display the dataframe with a callback for row selection
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Amount": st.column_config.NumberColumn(format="$%.2f") if "Amount" in df.columns else None,
                "Amount Due": st.column_config.NumberColumn(format="$%.2f") if "Amount Due" in df.columns else None,
                "Actions": st.column_config.Column(
                    width="small",
                    help="Actions"
                )
            },
            hide_index=True
        )
        
        # Action buttons in separate columns below the table
        st.write("Select an item to perform actions:")
        
        # Get a list of IDs for selection
        id_options = [c.get("id", "") for c in filtered_contracts]
        selected_id = st.selectbox("Select Item", id_options, label_visibility="collapsed")
        
        if selected_id:
            # Add action buttons for the selected item
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("View Details", key=f"view_{contract_type}_{selected_id}"):
                    st.session_state.contracts_view = "detail"
                    st.session_state.selected_contract_type = contract_type
                    st.session_state.selected_contract_id = selected_id
                    st.rerun()
            
            with col2:
                if st.button("Edit", key=f"edit_{contract_type}_{selected_id}"):
                    st.session_state.contracts_view = "edit"
                    st.session_state.selected_contract_type = contract_type
                    st.session_state.selected_contract_id = selected_id
                    st.rerun()
            
            with col3:
                if contract_type == "change_orders":
                    # Get the selected change order
                    selected_co = next((c for c in filtered_contracts if c.get("id") == selected_id), None)
                    if selected_co and selected_co.get("status") != "Approved":
                        if st.button("Approve", key=f"approve_{contract_type}_{selected_id}"):
                            # Approve the change order
                            for c in contracts:
                                if c.get("id") == selected_id:
                                    c["status"] = "Approved"
                                    c["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                            save_contract_data(contract_type, contracts)
                            st.success(f"Change Order {selected_id} approved successfully.")
                            st.rerun()
                elif contract_type == "subcontracts":
                    # Get the selected subcontract
                    selected_sc = next((c for c in filtered_contracts if c.get("id") == selected_id), None)
                    if selected_sc and selected_sc.get("status") != "Executed":
                        if st.button("Mark as Executed", key=f"execute_{contract_type}_{selected_id}"):
                            # Mark the subcontract as executed
                            for c in contracts:
                                if c.get("id") == selected_id:
                                    c["status"] = "Executed"
                                    c["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                            save_contract_data(contract_type, contracts)
                            st.success(f"Subcontract {selected_id} marked as executed successfully.")
                            st.rerun()
                elif contract_type == "invoices":
                    # Get the selected invoice
                    selected_inv = next((c for c in filtered_contracts if c.get("id") == selected_id), None)
                    if selected_inv and selected_inv.get("status") != "Paid":
                        if st.button("Mark as Paid", key=f"pay_{contract_type}_{selected_id}"):
                            # Mark the invoice as paid
                            for c in contracts:
                                if c.get("id") == selected_id:
                                    c["status"] = "Paid"
                                    c["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                            save_contract_data(contract_type, contracts)
                            st.success(f"Invoice {selected_id} marked as paid successfully.")
                            st.rerun()
            
            with col4:
                if st.button("Delete", key=f"delete_{contract_type}_{selected_id}"):
                    # Confirm deletion
                    st.warning(f"Are you sure you want to delete {selected_id}?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Yes, Delete", key=f"confirm_delete_{contract_type}_{selected_id}"):
                            # Delete the contract
                            contracts = [c for c in contracts if c.get("id") != selected_id]
                            save_contract_data(contract_type, contracts)
                            st.success(f"{selected_id} deleted successfully.")
                            st.rerun()
                    with col2:
                        if st.button("Cancel", key=f"cancel_delete_{contract_type}_{selected_id}"):
                            st.rerun()
    else:
        st.info(f"No {type_label.lower()} found. Click the '+ New {type_label[:-1]}' button to create one.")

def render_change_order_detail():
    """Render detailed view of a change order."""
    # Get the selected change order
    selected_id = st.session_state.selected_contract_id
    change_orders = load_contract_data("change_orders")
    co = next((c for c in change_orders if c.get("id") == selected_id), None)
    
    if not co:
        st.error(f"Change Order {selected_id} not found.")
        return
    
    st.header(f"Change Order: {co.get('id')}")
    
    # Basic change order information
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Project:** {co.get('project', '')}")
        st.markdown(f"**Description:** {co.get('description', '')}")
        st.markdown(f"**Reason:** {co.get('reason', '')}")
    with col2:
        st.markdown(f"**Date:** {co.get('date', '')}")
        st.markdown(f"**Status:** {co.get('status', '')}")
    
    # Financial information
    st.subheader("Financial Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Original Contract Amount", f"${co.get('original_amount', 0):,.2f}")
    with col2:
        st.metric("Previous Changes", f"${co.get('previous_changes', 0):,.2f}")
    with col3:
        st.metric("This Change", f"${co.get('this_change', 0):,.2f}")
    
    # Calculate new contract sum
    new_sum = co.get('original_amount', 0) + co.get('previous_changes', 0) + co.get('this_change', 0)
    st.metric("New Contract Sum", f"${new_sum:,.2f}")
    
    # Schedule impact
    st.subheader("Schedule Impact")
    days_added = co.get('days_added', 0)
    st.markdown(f"**Days Added to Schedule:** {days_added}")
    
    # Signatures
    st.subheader("Signatures")
    signatures = co.get('signatures', [])
    if signatures:
        for sig in signatures:
            st.markdown(f"- {sig}")
    else:
        st.info("No signatures yet.")
    
    # Metadata
    st.subheader("Metadata")
    st.markdown(f"**Created:** {co.get('created_at', '')}")
    st.markdown(f"**Last Updated:** {co.get('updated_at', '')}")
    
    # Action buttons
    st.subheader("Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Edit Change Order"):
            st.session_state.contracts_view = "edit"
            st.rerun()
    
    with col2:
        if co.get("status") != "Approved":
            if st.button("Approve Change Order"):
                # Approve the change order
                for c in change_orders:
                    if c.get("id") == selected_id:
                        c["status"] = "Approved"
                        c["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                save_contract_data("change_orders", change_orders)
                st.success(f"Change Order {selected_id} approved successfully.")
                st.rerun()
    
    with col3:
        if st.button("Delete Change Order"):
            # Confirm deletion
            st.warning(f"Are you sure you want to delete {selected_id}?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", key=f"confirm_delete_detail"):
                    # Delete the change order
                    change_orders = [c for c in change_orders if c.get("id") != selected_id]
                    save_contract_data("change_orders", change_orders)
                    st.success(f"{selected_id} deleted successfully.")
                    st.session_state.contracts_view = "list"
                    st.session_state.selected_contract_id = None
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_delete_detail"):
                    st.rerun()

def render_subcontract_detail():
    """Render detailed view of a subcontract."""
    # Get the selected subcontract
    selected_id = st.session_state.selected_contract_id
    subcontracts = load_contract_data("subcontracts")
    sc = next((c for c in subcontracts if c.get("id") == selected_id), None)
    
    if not sc:
        st.error(f"Subcontract {selected_id} not found.")
        return
    
    st.header(f"Subcontract: {sc.get('id')}")
    
    # Basic subcontract information
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Project:** {sc.get('project', '')}")
        st.markdown(f"**Company:** {sc.get('company', '')}")
        st.markdown(f"**Scope:** {sc.get('scope', '')}")
    with col2:
        st.markdown(f"**Date:** {sc.get('date', '')}")
        st.markdown(f"**Status:** {sc.get('status', '')}")
    
    # Contact information
    st.subheader("Contact Information")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Contact:** {sc.get('contact', '')}")
    with col2:
        st.markdown(f"**Email:** {sc.get('email', '')}")
    
    # Financial information
    st.subheader("Financial Information")
    st.metric("Contract Amount", f"${sc.get('amount', 0):,.2f}")
    
    # Schedule information
    st.subheader("Schedule")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Start Date:** {sc.get('start_date', '')}")
    with col2:
        st.markdown(f"**Completion Date:** {sc.get('completion_date', '')}")
    
    # Signatures
    st.subheader("Signatures")
    signatures = sc.get('signatures', [])
    if signatures:
        for sig in signatures:
            st.markdown(f"- {sig}")
    else:
        st.info("No signatures yet.")
    
    # Metadata
    st.subheader("Metadata")
    st.markdown(f"**Created:** {sc.get('created_at', '')}")
    st.markdown(f"**Last Updated:** {sc.get('updated_at', '')}")
    
    # Action buttons
    st.subheader("Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Edit Subcontract"):
            st.session_state.contracts_view = "edit"
            st.rerun()
    
    with col2:
        if sc.get("status") != "Executed":
            if st.button("Mark as Executed"):
                # Mark the subcontract as executed
                for c in subcontracts:
                    if c.get("id") == selected_id:
                        c["status"] = "Executed"
                        c["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                save_contract_data("subcontracts", subcontracts)
                st.success(f"Subcontract {selected_id} marked as executed successfully.")
                st.rerun()
    
    with col3:
        if st.button("Delete Subcontract"):
            # Confirm deletion
            st.warning(f"Are you sure you want to delete {selected_id}?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", key=f"confirm_delete_detail"):
                    # Delete the subcontract
                    subcontracts = [c for c in subcontracts if c.get("id") != selected_id]
                    save_contract_data("subcontracts", subcontracts)
                    st.success(f"{selected_id} deleted successfully.")
                    st.session_state.contracts_view = "list"
                    st.session_state.selected_contract_id = None
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_delete_detail"):
                    st.rerun()

def render_invoice_detail():
    """Render detailed view of an invoice."""
    # Get the selected invoice
    selected_id = st.session_state.selected_contract_id
    invoices = load_contract_data("invoices")
    inv = next((i for i in invoices if i.get("id") == selected_id), None)
    
    if not inv:
        st.error(f"Invoice {selected_id} not found.")
        return
    
    st.header(f"Invoice: {inv.get('id')}")
    
    # Basic invoice information
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Project:** {inv.get('project', '')}")
        st.markdown(f"**Description:** {inv.get('description', '')}")
        st.markdown(f"**Company:** {inv.get('company', '')}")
    with col2:
        st.markdown(f"**Date:** {inv.get('date', '')}")
        st.markdown(f"**Status:** {inv.get('status', '')}")
    
    # Financial information
    st.subheader("Financial Information")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Contract Amount", f"${inv.get('contract_amount', 0):,.2f}")
        st.metric("Previously Billed", f"${inv.get('previously_billed', 0):,.2f}")
    with col2:
        st.metric("Current Billing", f"${inv.get('current_billed', 0):,.2f}")
        st.metric("Retainage", f"${inv.get('retainage', 0):,.2f}")
    
    st.metric("Amount Due", f"${inv.get('amount_due', 0):,.2f}")
    
    # Signatures
    st.subheader("Signatures")
    signatures = inv.get('signatures', [])
    if signatures:
        for sig in signatures:
            st.markdown(f"- {sig}")
    else:
        st.info("No signatures yet.")
    
    # Metadata
    st.subheader("Metadata")
    st.markdown(f"**Created:** {inv.get('created_at', '')}")
    st.markdown(f"**Last Updated:** {inv.get('updated_at', '')}")
    
    # Action buttons
    st.subheader("Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Edit Invoice"):
            st.session_state.contracts_view = "edit"
            st.rerun()
    
    with col2:
        if inv.get("status") != "Paid":
            if st.button("Mark as Paid"):
                # Mark the invoice as paid
                for i in invoices:
                    if i.get("id") == selected_id:
                        i["status"] = "Paid"
                        i["updated_at"] = datetime.now().strftime("%Y-%m-%d")
                save_contract_data("invoices", invoices)
                st.success(f"Invoice {selected_id} marked as paid successfully.")
                st.rerun()
    
    with col3:
        if st.button("Delete Invoice"):
            # Confirm deletion
            st.warning(f"Are you sure you want to delete {selected_id}?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", key=f"confirm_delete_detail"):
                    # Delete the invoice
                    invoices = [i for i in invoices if i.get("id") != selected_id]
                    save_contract_data("invoices", invoices)
                    st.success(f"{selected_id} deleted successfully.")
                    st.session_state.contracts_view = "list"
                    st.session_state.selected_contract_id = None
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_delete_detail"):
                    st.rerun()

def render_contract_log():
    """Render a log of all contracts with their signature status."""
    st.header("Contract Log")
    
    # Load all contract data
    change_orders = load_contract_data("change_orders")
    subcontracts = load_contract_data("subcontracts")
    invoices = load_contract_data("invoices")
    
    # Prepare data for the log
    contract_log = []
    
    # Add change orders to the log
    for co in change_orders:
        signatures_complete = "Complete" if len(co.get("signatures", [])) >= 2 else "Incomplete"
        contract_log.append({
            "Number": co.get("id", ""),
            "Type": "Change Order",
            "Date": co.get("date", ""),
            "Description": co.get("description", ""),
            "Amount": co.get("this_change", 0),
            "Status": co.get("status", ""),
            "Signatures": signatures_complete
        })
    
    # Add subcontracts to the log
    for sc in subcontracts:
        signatures_complete = "Complete" if len(sc.get("signatures", [])) >= 2 else "Incomplete"
        contract_log.append({
            "Number": sc.get("id", ""),
            "Type": "Subcontract",
            "Date": sc.get("date", ""),
            "Description": sc.get("scope", ""),
            "Amount": sc.get("amount", 0),
            "Status": sc.get("status", ""),
            "Signatures": signatures_complete
        })
    
    # Add invoices to the log
    for inv in invoices:
        signatures_complete = "Complete" if len(inv.get("signatures", [])) >= 2 else "Incomplete"
        contract_log.append({
            "Number": inv.get("id", ""),
            "Type": "Invoice",
            "Date": inv.get("date", ""),
            "Description": inv.get("description", ""),
            "Amount": inv.get("amount_due", 0),
            "Status": inv.get("status", ""),
            "Signatures": signatures_complete
        })
    
    # Convert to DataFrame
    if contract_log:
        contracts_df = pd.DataFrame(contract_log)
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        with col1:
            type_filter = st.multiselect(
                "Contract Type",
                options=["All Types"] + sorted(list(set(c.get("Type", "") for c in contract_log))),
                default="All Types"
            )
        with col2:
            status_filter = st.multiselect(
                "Status",
                options=["All Statuses"] + sorted(list(set(c.get("Status", "") for c in contract_log))),
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
            },
            hide_index=True
        )
        
        # Summary metrics
        st.subheader("Contract Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_contracts = len(filtered_df)
            st.metric("Total Contracts", total_contracts)
        with col2:
            total_value = filtered_df["Amount"].sum()
            st.metric("Total Contract Value", f"${total_value:,.2f}")
        with col3:
            executed_contracts = len(filtered_df[filtered_df["Signatures"] == "Complete"])
            percent_executed = (executed_contracts / total_contracts * 100) if total_contracts > 0 else 0
            st.metric("Signed Contracts", f"{executed_contracts} ({percent_executed:.0f}%)")
        with col4:
            pending_signatures = len(filtered_df[filtered_df["Signatures"] == "Incomplete"])
            st.metric("Pending Signatures", pending_signatures)
    else:
        st.info("No contracts found in the system.")