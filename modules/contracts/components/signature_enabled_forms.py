"""
Signature-Enabled Form Components for Contracts Module.

This module provides contract forms with integrated digital signature capabilities.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from components.form_signature_field import signature_field, save_signature

def change_order_with_signatures():
    """Render a change order form with integrated signature fields."""
    st.header("Change Order Form")
    
    with st.form("change_order_form"):
        # Basic change order information
        cols = st.columns(2)
        with cols[0]:
            co_number = st.text_input("Change Order Number", value="CO-2025-042")
            project = st.text_input("Project", value="Highland Tower Development")
        with cols[1]:
            date = st.date_input("Date", value=datetime.now())
            status = st.selectbox("Status", ["Draft", "Pending Approval", "Approved", "Rejected"])
        
        # Financial information
        st.subheader("Financial Information")
        cols = st.columns(3)
        with cols[0]:
            original_amount = st.number_input("Original Contract Amount", value=45500000.00, format="%.2f")
        with cols[1]:
            previous_changes = st.number_input("Previous Change Orders", value=124500.00, format="%.2f")
        with cols[2]:
            this_change = st.number_input("This Change Order Amount", value=36750.00, format="%.2f")
        
        # Calculate new contract sum
        new_contract_sum = original_amount + previous_changes + this_change
        st.metric("New Contract Sum", f"${new_contract_sum:,.2f}")
        
        # Change details
        st.subheader("Change Description")
        reason = st.selectbox(
            "Reason for Change", 
            ["Owner Request", "Design Error/Omission", "Unforeseen Condition", "Code Requirement", "Value Engineering"]
        )
        description = st.text_area(
            "Description", 
            value="Addition of electrical conduits in east stairwell to accommodate new security equipment. Work includes labor and materials for conduit installation and associated drywall repair."
        )
        
        # Time impact
        st.subheader("Schedule Impact")
        cols = st.columns(2)
        with cols[0]:
            days_added = st.number_input("Days Added to Schedule", value=3, min_value=0)
        with cols[1]:
            new_completion = st.date_input("New Completion Date", value=datetime.strptime("2027-07-03", "%Y-%m-%d"))
        
        # Attachments
        st.subheader("Attachments")
        attachments = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True)
        
        # Signature fields embedded directly in the form
        st.subheader("Signatures")
        
        # Create tabs for the different signatories
        tabs = st.tabs(["Contractor", "Owner", "Architect"])
        
        with tabs[0]:
            contractor_signature = signature_field(
                label="Contractor Signature",
                key="contractor_signature",
                required=True
            )
        
        with tabs[1]:
            owner_signature = signature_field(
                label="Owner Signature", 
                key="owner_signature",
                required=True
            )
            
        with tabs[2]:
            architect_signature = signature_field(
                label="Architect Signature",
                key="architect_signature"
            )
        
        # Submit button
        submitted = st.form_submit_button("Submit Change Order")
        
        if submitted:
            # Process the form data
            signatures_saved = []
            
            # Save signatures if provided
            if contractor_signature.get("image"):
                contractor_file = save_signature(
                    contractor_signature,
                    f"signatures/CO-{co_number}-contractor.png"
                )
                signatures_saved.append(f"Contractor: {contractor_signature.get('name')}")
            
            if owner_signature.get("image"):
                owner_file = save_signature(
                    owner_signature,
                    f"signatures/CO-{co_number}-owner.png"
                )
                signatures_saved.append(f"Owner: {owner_signature.get('name')}")
                
            if architect_signature.get("image"):
                architect_file = save_signature(
                    architect_signature,
                    f"signatures/CO-{co_number}-architect.png"
                )
                signatures_saved.append(f"Architect: {architect_signature.get('name')}")
            
            # Show success message
            if len(signatures_saved) >= 2:  # Require at least contractor and owner signatures
                st.success(f"Change Order submitted with signatures from: {', '.join(signatures_saved)}")
                
                # Show final change order details
                st.json({
                    "change_order": {
                        "number": co_number,
                        "project": project,
                        "date": date.strftime("%Y-%m-%d"),
                        "amount": this_change,
                        "new_contract_sum": new_contract_sum,
                        "days_added": days_added,
                        "signatures": signatures_saved
                    }
                })
            else:
                if signatures_saved:
                    st.warning(f"Change Order saved as draft. Required signatures missing. Signatures received: {', '.join(signatures_saved)}")
                else:
                    st.warning("Change Order saved as draft. No signatures were provided.")

def subcontract_with_signatures():
    """Render a subcontract form with integrated signature fields."""
    st.header("Subcontract Agreement")
    
    with st.form("subcontract_form"):
        # Basic subcontract information
        cols = st.columns(2)
        with cols[0]:
            subcontract_number = st.text_input("Subcontract Number", value="SC-2025-078")
            project = st.text_input("Project", value="Highland Tower Development")
            scope = st.text_input("Scope of Work", value="Electrical")
        with cols[1]:
            date = st.date_input("Date", value=datetime.now())
            status = st.selectbox("Status", ["Draft", "Pending Execution", "Executed", "Terminated"])
        
        # Subcontractor information
        st.subheader("Subcontractor Information")
        cols = st.columns(2)
        with cols[0]:
            company_name = st.text_input("Company Name", value="Elite Electrical Systems")
            contact_name = st.text_input("Contact Name", value="John Smith")
            email = st.text_input("Email", value="jsmith@eliteelectrical.com")
        with cols[1]:
            address = st.text_area("Address", value="123 Contractor Way\nCity, State 12345")
            phone = st.text_input("Phone", value="(555) 123-4567")
        
        # Contract details
        st.subheader("Contract Details")
        cols = st.columns(2)
        with cols[0]:
            contract_sum = st.number_input("Contract Sum", value=1250000.00, format="%.2f")
            retainage = st.number_input("Retainage Percentage", value=10.0, format="%.1f")
        with cols[1]:
            start_date = st.date_input("Start Date", value=datetime.strptime("2025-08-15", "%Y-%m-%d"))
            completion_date = st.date_input("Completion Date", value=datetime.strptime("2026-04-30", "%Y-%m-%d"))
        
        # Payment terms
        st.subheader("Payment Terms")
        payment_terms = st.text_area(
            "Payment Terms", 
            value="Monthly progress payments based on percentage complete, less retainage. Retainage to be released upon substantial completion and delivery of all closeout documentation."
        )
        
        # Insurance requirements
        st.subheader("Insurance Requirements")
        insurance = st.text_area(
            "Insurance Requirements", 
            value="Subcontractor shall maintain commercial general liability insurance with limits not less than $2,000,000 per occurrence, automobile liability insurance with limits not less than $1,000,000, and worker's compensation insurance as required by law."
        )
        
        # Attachments
        st.subheader("Attachments")
        attachments = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True)
        
        # Signature fields embedded directly in the form
        st.subheader("Signatures")
        
        # Create tabs for the different signatories
        tabs = st.tabs(["Subcontractor", "General Contractor"])
        
        with tabs[0]:
            subcontractor_signature = signature_field(
                label="Subcontractor Signature",
                key="subcontractor_signature",
                required=True
            )
        
        with tabs[1]:
            gc_signature = signature_field(
                label="General Contractor Signature", 
                key="gc_signature",
                required=True
            )
        
        # Submit button
        submitted = st.form_submit_button("Submit Subcontract")
        
        if submitted:
            # Process the form data
            signatures_saved = []
            
            # Save signatures if provided
            if subcontractor_signature.get("image"):
                sub_file = save_signature(
                    subcontractor_signature,
                    f"signatures/SC-{subcontract_number}-subcontractor.png"
                )
                signatures_saved.append(f"Subcontractor: {subcontractor_signature.get('name')}")
            
            if gc_signature.get("image"):
                gc_file = save_signature(
                    gc_signature,
                    f"signatures/SC-{subcontract_number}-gc.png"
                )
                signatures_saved.append(f"General Contractor: {gc_signature.get('name')}")
            
            # Show success message
            if len(signatures_saved) == 2:  # Require both signatures
                st.success(f"Subcontract executed with signatures from: {', '.join(signatures_saved)}")
                
                # Show final subcontract details
                st.json({
                    "subcontract": {
                        "number": subcontract_number,
                        "project": project,
                        "scope": scope,
                        "date": date.strftime("%Y-%m-%d"),
                        "company": company_name,
                        "amount": contract_sum,
                        "signatures": signatures_saved
                    }
                })
            else:
                if signatures_saved:
                    st.warning(f"Subcontract saved as draft. Required signatures missing. Signatures received: {', '.join(signatures_saved)}")
                else:
                    st.warning("Subcontract saved as draft. No signatures were provided.")

def invoice_with_signatures():
    """Render an invoice form with integrated signature fields."""
    st.header("Invoice Form")
    
    with st.form("invoice_form"):
        # Basic invoice information
        cols = st.columns(2)
        with cols[0]:
            invoice_number = st.text_input("Invoice Number", value="INV-2025-125")
            project = st.text_input("Project", value="Highland Tower Development")
            description = st.text_input("Invoice Description", value="April 2025 Progress Billing")
        with cols[1]:
            date = st.date_input("Date", value=datetime.now())
            due_date = st.date_input("Due Date", value=datetime.now().replace(day=datetime.now().day + 30))
        
        # Billing information
        st.subheader("Billing Information")
        cols = st.columns(2)
        with cols[0]:
            contract_amount = st.number_input("Original Contract Amount", value=1250000.00, format="%.2f")
            approved_changes = st.number_input("Approved Change Orders", value=36750.00, format="%.2f")
            current_contract = contract_amount + approved_changes
        
        with cols[1]:
            prev_billed = st.number_input("Previously Billed", value=475000.00, format="%.2f")
            current_billed = st.number_input("Current Billing", value=225000.00, format="%.2f")
            total_billed = prev_billed + current_billed
            percent_complete = (total_billed / current_contract) * 100 if current_contract > 0 else 0
        
        st.markdown(f"**Current Contract Sum:** ${current_contract:,.2f}")
        st.markdown(f"**Total Billed to Date:** ${total_billed:,.2f} ({percent_complete:.1f}% Complete)")
        
        # Line items
        st.subheader("Invoice Items")
        line_items = {
            "Description": ["Mobilization", "Rough-in (Floors 1-5)", "Panel Installation", "Light Fixtures", "Material"],
            "Scheduled Value": [75000.00, 450000.00, 225000.00, 350000.00, 186750.00],
            "Previous Applications": [75000.00, 250000.00, 125000.00, 25000.00, 0.00],
            "This Period": [0.00, 100000.00, 50000.00, 50000.00, 25000.00],
            "Total Complete": [75000.00, 350000.00, 175000.00, 75000.00, 25000.00],
            "% Complete": [100.0, 77.8, 77.8, 21.4, 13.4]
        }
        edited_items = st.data_editor(pd.DataFrame(line_items), use_container_width=True, 
                                     column_config={"Scheduled Value": st.column_config.NumberColumn(format="$%.2f"),
                                                   "Previous Applications": st.column_config.NumberColumn(format="$%.2f"),
                                                   "This Period": st.column_config.NumberColumn(format="$%.2f"),
                                                   "Total Complete": st.column_config.NumberColumn(format="$%.2f"),
                                                   "% Complete": st.column_config.NumberColumn(format="%.1f%%")})
        
        # Retainage
        retainage_percent = st.number_input("Retainage Percentage", value=10.0, min_value=0.0, max_value=100.0, format="%.1f")
        retainage_amount = current_billed * (retainage_percent / 100)
        amount_due = current_billed - retainage_amount
        
        st.markdown(f"**Current Amount Billed:** ${current_billed:,.2f}")
        st.markdown(f"**Less Retainage ({retainage_percent}%):** ${retainage_amount:,.2f}")
        st.metric("Amount Due This Invoice", f"${amount_due:,.2f}")
        
        # Attachments
        st.subheader("Attachments")
        attachments = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True)
        
        # Signature fields embedded directly in the form
        st.subheader("Signatures")
        
        # Create tabs for the different signatories
        tabs = st.tabs(["Contractor", "Owner/CM", "Architect"])
        
        with tabs[0]:
            contractor_signature = signature_field(
                label="Contractor Signature",
                key="invoice_contractor_signature",
                required=True
            )
        
        with tabs[1]:
            owner_signature = signature_field(
                label="Owner/CM Signature", 
                key="invoice_owner_signature",
                required=True
            )
            
        with tabs[2]:
            architect_signature = signature_field(
                label="Architect Signature",
                key="invoice_architect_signature"
            )
        
        # Submit button
        submitted = st.form_submit_button("Submit Invoice")
        
        if submitted:
            # Process the form data
            signatures_saved = []
            
            # Save signatures if provided
            if contractor_signature.get("image"):
                contractor_file = save_signature(
                    contractor_signature,
                    f"signatures/INV-{invoice_number}-contractor.png"
                )
                signatures_saved.append(f"Contractor: {contractor_signature.get('name')}")
            
            if owner_signature.get("image"):
                owner_file = save_signature(
                    owner_signature,
                    f"signatures/INV-{invoice_number}-owner.png"
                )
                signatures_saved.append(f"Owner/CM: {owner_signature.get('name')}")
                
            if architect_signature.get("image"):
                architect_file = save_signature(
                    architect_signature,
                    f"signatures/INV-{invoice_number}-architect.png"
                )
                signatures_saved.append(f"Architect: {architect_signature.get('name')}")
            
            # Show success message based on number of signatures
            if len(signatures_saved) >= 2:
                st.success(f"Invoice submitted with signatures from: {', '.join(signatures_saved)}")
            else:
                if signatures_saved:
                    st.warning(f"Invoice saved as draft. Required signatures missing. Signatures received: {', '.join(signatures_saved)}")
                else:
                    st.warning("Invoice saved as draft. No signatures were provided.")