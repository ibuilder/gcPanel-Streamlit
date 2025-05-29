"""
Contract form components for Streamlit interface.

This module provides reusable form components for contract items
such as prime contracts, subcontracts, and change orders with
consistent styling and validation.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from components.form_helper import form_input_field, validate_form, form_action_buttons

# Contract Types
CONTRACT_TYPES = ['GMP', 'Cost Plus', 'Lump Sum', 'CMAR', 'Design-Build', 'Unit Price', 'Time and Materials']

# Contract Statuses
CONTRACT_STATUSES = ['Draft', 'Issued', 'Executed', 'In Progress', 'On Hold', 'Completed', 'Terminated']

# Vendor Types
VENDOR_TYPES = ['Subcontractor', 'Supplier', 'Consultant', 'Owner', 'General Contractor']

def contract_form(is_edit=False, contract_data=None):
    """
    Render a reusable contract form with validation
    
    Args:
        is_edit: Whether this is an edit form or a new contract
        contract_data: Existing contract data for editing
        
    Returns:
        Tuple of (form_submitted, form_data)
    """
    form_submitted = False
    form_data = {}
    
    # Initialize error container
    if "form_errors" not in st.session_state:
        st.session_state.form_errors = {}
    
    with st.form(key=f"contract_form_{'edit' if is_edit else 'new'}"):
        st.subheader(f"{'Edit' if is_edit else 'Create New'} Contract")
        
        # Extract defaults from existing data if editing
        defaults = {}
        if is_edit and contract_data:
            defaults = {
                "name": contract_data.get("name", ""),
                "id": contract_data.get("id", ""),
                "type": contract_data.get("type", ""),
                "vendor": contract_data.get("vendor", ""),
                "vendor_type": contract_data.get("vendor_type", "Subcontractor"),
                "issue_date": contract_data.get("issue_date", datetime.now()),
                "execution_date": contract_data.get("execution_date", None),
                "completion_date": contract_data.get("completion_date", datetime.now() + timedelta(days=180)),
                "original_value": contract_data.get("original_value", 0.0),
                "approved_changes": contract_data.get("approved_changes", 0.0),
                "scope": contract_data.get("scope", ""),
                "status": contract_data.get("status", "Draft"),
                "contact_name": contract_data.get("contact_name", ""),
                "contact_email": contract_data.get("contact_email", ""),
                "contact_phone": contract_data.get("contact_phone", ""),
                "inclusions": contract_data.get("inclusions", ""),
                "exclusions": contract_data.get("exclusions", ""),
                "retainage_pct": contract_data.get("retainage_pct", 10.0)
            }
        
        # Create tabs for different contract information sections
        tab1, tab2, tab3 = st.tabs(["Contract Information", "Financial Details", "Contact & Other"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                contract_id, contract_id_error = form_input_field(
                    "Contract ID",
                    "contract_id",
                    default=defaults.get("id", ""),
                    required=True,
                    help_text="Unique contract identifier"
                )
                form_data["contract_id_error"] = contract_id_error
                
                contract_name, contract_name_error = form_input_field(
                    "Contract Name",
                    "contract_name",
                    default=defaults.get("name", ""),
                    required=True,
                    help_text="Name or title of the contract"
                )
                form_data["contract_name_error"] = contract_name_error
                
                contract_type, contract_type_error = form_input_field(
                    "Contract Type",
                    "contract_type",
                    field_type="select",
                    options=CONTRACT_TYPES,
                    default=defaults.get("type", CONTRACT_TYPES[0]),
                    required=True
                )
                form_data["contract_type_error"] = contract_type_error
                
                status, status_error = form_input_field(
                    "Status",
                    "contract_status",
                    field_type="select",
                    options=CONTRACT_STATUSES,
                    default=defaults.get("status", "Draft"),
                    required=True
                )
                form_data["status_error"] = status_error
            
            with col2:
                vendor, vendor_error = form_input_field(
                    "Vendor/Party",
                    "contract_vendor",
                    default=defaults.get("vendor", ""),
                    required=True,
                    help_text="Name of the vendor or contracting party"
                )
                form_data["vendor_error"] = vendor_error
                
                vendor_type, vendor_type_error = form_input_field(
                    "Vendor Type",
                    "vendor_type",
                    field_type="select",
                    options=VENDOR_TYPES,
                    default=defaults.get("vendor_type", VENDOR_TYPES[0]),
                    required=True
                )
                form_data["vendor_type_error"] = vendor_type_error
                
                issue_date, issue_date_error = form_input_field(
                    "Issue Date",
                    "issue_date",
                    field_type="date",
                    default=defaults.get("issue_date", datetime.now()),
                    required=True
                )
                form_data["issue_date_error"] = issue_date_error
                
                execution_date, execution_date_error = form_input_field(
                    "Execution Date",
                    "execution_date",
                    field_type="date",
                    default=defaults.get("execution_date", None),
                    required=False
                )
                form_data["execution_date_error"] = execution_date_error
                
                completion_date, completion_date_error = form_input_field(
                    "Completion Date",
                    "completion_date",
                    field_type="date",
                    default=defaults.get("completion_date", datetime.now() + timedelta(days=180)),
                    required=True
                )
                form_data["completion_date_error"] = completion_date_error
            
            # Contract scope
            scope, scope_error = form_input_field(
                "Contract Scope",
                "contract_scope",
                field_type="textarea",
                default=defaults.get("scope", ""),
                required=True,
                height=150,
                help_text="Detailed description of contract scope"
            )
            form_data["scope_error"] = scope_error
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                original_value, original_value_error = form_input_field(
                    "Original Value ($)",
                    "original_value",
                    field_type="number",
                    default=defaults.get("original_value", 0.0),
                    required=True,
                    min_value=0.0,
                    help_text="Original contract value in dollars"
                )
                form_data["original_value_error"] = original_value_error
                
                approved_changes, approved_changes_error = form_input_field(
                    "Approved Changes ($)",
                    "approved_changes",
                    field_type="number",
                    default=defaults.get("approved_changes", 0.0),
                    required=False,
                    min_value=0.0,
                    help_text="Sum of all approved change orders"
                )
                form_data["approved_changes_error"] = approved_changes_error
                
                # Calculate current value
                current_value = float(original_value or 0) + float(approved_changes or 0)
                
                # Display current value (read-only)
                st.markdown(f"**Current Contract Value:** ${current_value:,.2f}")
            
            with col2:
                retainage_pct, retainage_pct_error = form_input_field(
                    "Retainage Percentage (%)",
                    "retainage_pct",
                    field_type="number",
                    default=defaults.get("retainage_pct", 10.0),
                    required=True,
                    min_value=0.0,
                    max_value=100.0,
                    help_text="Percentage of contract value retained until completion"
                )
                form_data["retainage_pct_error"] = retainage_pct_error
                
                # Paid to date (in real app would be calculated from payment records)
                paid_to_date, paid_to_date_error = form_input_field(
                    "Paid to Date ($)",
                    "paid_to_date",
                    field_type="number",
                    default=defaults.get("paid_to_date", 0.0),
                    required=False,
                    min_value=0.0,
                    max_value=current_value,
                    help_text="Total amount paid to date"
                )
                form_data["paid_to_date_error"] = paid_to_date_error
                
                # Show retention held and remaining balance (calculated)
                retention_held = float(paid_to_date or 0) * (float(retainage_pct or 0) / 100)
                remaining_balance = current_value - float(paid_to_date or 0)
                
                # Display calculated values
                st.markdown(f"**Retention Held:** ${retention_held:,.2f}")
                st.markdown(f"**Remaining Balance:** ${remaining_balance:,.2f}")
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                contact_name, contact_name_error = form_input_field(
                    "Contact Name",
                    "contact_name",
                    default=defaults.get("contact_name", ""),
                    required=True,
                    help_text="Primary contact person for this contract"
                )
                form_data["contact_name_error"] = contact_name_error
                
                contact_email, contact_email_error = form_input_field(
                    "Contact Email",
                    "contact_email",
                    default=defaults.get("contact_email", ""),
                    required=True,
                    help_text="Email address for the primary contact"
                )
                form_data["contact_email_error"] = contact_email_error
                
                contact_phone, contact_phone_error = form_input_field(
                    "Contact Phone",
                    "contact_phone",
                    default=defaults.get("contact_phone", ""),
                    required=True,
                    help_text="Phone number for the primary contact"
                )
                form_data["contact_phone_error"] = contact_phone_error
            
            with col2:
                inclusions, inclusions_error = form_input_field(
                    "Inclusions",
                    "inclusions",
                    field_type="textarea",
                    default=defaults.get("inclusions", ""),
                    required=False,
                    height=100,
                    help_text="Items specifically included in the contract"
                )
                form_data["inclusions_error"] = inclusions_error
                
                exclusions, exclusions_error = form_input_field(
                    "Exclusions",
                    "exclusions",
                    field_type="textarea",
                    default=defaults.get("exclusions", ""),
                    required=False,
                    height=100,
                    help_text="Items specifically excluded from the contract"
                )
                form_data["exclusions_error"] = exclusions_error
        
        # Form buttons
        submit_primary, submit_draft, _ = form_action_buttons(
            primary_label="Submit Contract",
            secondary_label="Save as Draft",
            alignment="right"
        )
        
        # Handle form submission
        if submit_primary or submit_draft:
            form_is_valid = validate_form(form_data)
            
            if form_is_valid:
                # Collect form data
                form_result = {
                    "id": contract_id,
                    "name": contract_name,
                    "type": contract_type,
                    "vendor": vendor,
                    "vendor_type": vendor_type,
                    "status": "Draft" if submit_draft else status,
                    "issue_date": issue_date,
                    "execution_date": execution_date,
                    "completion_date": completion_date,
                    "original_value": float(original_value),
                    "approved_changes": float(approved_changes or 0),
                    "current_value": current_value,
                    "paid_to_date": float(paid_to_date or 0),
                    "retention_held": retention_held,
                    "remaining_balance": remaining_balance,
                    "scope": scope,
                    "retainage_pct": float(retainage_pct),
                    "contact_name": contact_name,
                    "contact_email": contact_email,
                    "contact_phone": contact_phone,
                    "inclusions": inclusions,
                    "exclusions": exclusions
                }
                
                # Clear form errors
                st.session_state.form_errors = {}
                
                # Set form submitted flag
                form_submitted = True
                
                # Show success message
                st.success(f"Contract {'saved as draft' if submit_draft else 'submitted'} successfully!")
                
                # Return form result
                return form_submitted, form_result
    
    # Return empty result if form wasn't submitted or had errors
    return form_submitted, None

def change_order_form(is_edit=False, change_order_data=None):
    """
    Render a reusable change order form with validation
    
    Args:
        is_edit: Whether this is an edit form or a new change order
        change_order_data: Existing change order data for editing
        
    Returns:
        Tuple of (form_submitted, form_data)
    """
    form_submitted = False
    form_data = {}
    
    # Initialize error container
    if "form_errors" not in st.session_state:
        st.session_state.form_errors = {}
    
    # Change order statuses
    change_order_statuses = [
        "Draft", "Submitted", "Under Review", "Approved", "Rejected", "Pending"
    ]
    
    # Change order types
    change_order_types = [
        "Contract Scope Change", "Field Modification", "Time Extension", 
        "Owner Request", "Design Change", "Unforeseen Condition", "Other"
    ]
    
    with st.form(key=f"change_order_form_{'edit' if is_edit else 'new'}"):
        st.subheader(f"{'Edit' if is_edit else 'Create New'} Change Order")
        
        # Extract defaults from existing data if editing
        defaults = {}
        if is_edit and change_order_data:
            defaults = {
                "number": change_order_data.get("number", ""),
                "contract_id": change_order_data.get("contract_id", ""),
                "title": change_order_data.get("title", ""),
                "description": change_order_data.get("description", ""),
                "type": change_order_data.get("type", ""),
                "status": change_order_data.get("status", "Draft"),
                "date_submitted": change_order_data.get("date_submitted", datetime.now()),
                "date_approved": change_order_data.get("date_approved", None),
                "amount": change_order_data.get("amount", 0.0),
                "time_extension": change_order_data.get("time_extension", 0),
                "justification": change_order_data.get("justification", ""),
                "impact_description": change_order_data.get("impact_description", "")
            }
        
        col1, col2 = st.columns(2)
        
        with col1:
            co_number, co_number_error = form_input_field(
                "Change Order Number",
                "co_number",
                default=defaults.get("number", ""),
                required=True,
                help_text="Unique identifier for this change order"
            )
            form_data["co_number_error"] = co_number_error
            
            contract_id, contract_id_error = form_input_field(
                "Contract ID",
                "co_contract_id",
                default=defaults.get("contract_id", ""),
                required=True,
                help_text="ID of the contract this change order applies to"
            )
            form_data["contract_id_error"] = contract_id_error
            
            co_type, co_type_error = form_input_field(
                "Change Order Type",
                "co_type",
                field_type="select",
                options=change_order_types,
                default=defaults.get("type", change_order_types[0]),
                required=True
            )
            form_data["co_type_error"] = co_type_error
            
            co_status, co_status_error = form_input_field(
                "Status",
                "co_status",
                field_type="select",
                options=change_order_statuses,
                default=defaults.get("status", "Draft"),
                required=True
            )
            form_data["co_status_error"] = co_status_error
        
        with col2:
            co_title, co_title_error = form_input_field(
                "Title",
                "co_title",
                default=defaults.get("title", ""),
                required=True,
                help_text="Short title describing the change order"
            )
            form_data["co_title_error"] = co_title_error
            
            date_submitted, date_submitted_error = form_input_field(
                "Date Submitted",
                "co_date_submitted",
                field_type="date",
                default=defaults.get("date_submitted", datetime.now()),
                required=True
            )
            form_data["date_submitted_error"] = date_submitted_error
            
            date_approved, date_approved_error = form_input_field(
                "Date Approved",
                "co_date_approved",
                field_type="date",
                default=defaults.get("date_approved", None),
                required=False
            )
            form_data["date_approved_error"] = date_approved_error
            
            amount, amount_error = form_input_field(
                "Amount ($)",
                "co_amount",
                field_type="number",
                default=defaults.get("amount", 0.0),
                required=True,
                help_text="Dollar value of the change (negative for deductions)"
            )
            form_data["amount_error"] = amount_error
            
            time_extension, time_extension_error = form_input_field(
                "Time Extension (days)",
                "co_time_extension",
                field_type="number",
                default=defaults.get("time_extension", 0),
                required=False,
                min_value=0,
                help_text="Days added to contract completion date"
            )
            form_data["time_extension_error"] = time_extension_error
        
        # Description
        description, description_error = form_input_field(
            "Description",
            "co_description",
            field_type="textarea",
            default=defaults.get("description", ""),
            required=True,
            height=100,
            help_text="Detailed description of the change"
        )
        form_data["description_error"] = description_error
        
        # Justification
        justification, justification_error = form_input_field(
            "Justification",
            "co_justification",
            field_type="textarea",
            default=defaults.get("justification", ""),
            required=True,
            height=100,
            help_text="Reason why this change is necessary"
        )
        form_data["justification_error"] = justification_error
        
        # Impact description
        impact_description, impact_description_error = form_input_field(
            "Impact Description",
            "co_impact_description",
            field_type="textarea",
            default=defaults.get("impact_description", ""),
            required=False,
            height=100,
            help_text="Description of how this change impacts the project"
        )
        form_data["impact_description_error"] = impact_description_error
        
        # File upload
        co_attachments = st.file_uploader("Add Attachments", accept_multiple_files=True, key="co_attachments")
        
        # Form buttons
        submit_primary, submit_draft, _ = form_action_buttons(
            primary_label="Submit Change Order",
            secondary_label="Save as Draft",
            alignment="right"
        )
        
        # Handle form submission
        if submit_primary or submit_draft:
            form_is_valid = validate_form(form_data)
            
            if form_is_valid:
                # Collect form data
                form_result = {
                    "number": co_number,
                    "contract_id": contract_id,
                    "title": co_title,
                    "description": description,
                    "type": co_type,
                    "status": "Draft" if submit_draft else co_status,
                    "date_submitted": date_submitted,
                    "date_approved": date_approved,
                    "amount": float(amount),
                    "time_extension": int(time_extension or 0),
                    "justification": justification,
                    "impact_description": impact_description,
                    "attachments": co_attachments
                }
                
                # Clear form errors
                st.session_state.form_errors = {}
                
                # Set form submitted flag
                form_submitted = True
                
                # Show success message
                st.success(f"Change Order {'saved as draft' if submit_draft else 'submitted'} successfully!")
                
                # Return form result
                return form_submitted, form_result
    
    # Return empty result if form wasn't submitted or had errors
    return form_submitted, None