"""
Digital Signature Demo Component for gcPanel.

This module demonstrates how to use the signature pad component
in construction forms like change orders, invoices and daily reports.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from components.signature_pad import render_signature_pad, save_signature_to_file

def render_signature_demo():
    """Render a demo of the digital signature component."""
    st.title("Digital Signature Integration")
    
    # Demo description
    st.markdown("""
    This page demonstrates the digital signature integration for gcPanel construction forms.
    Choose a form type below to see how digital signatures can be integrated.
    """)
    
    # Demo selection
    demo_type = st.selectbox(
        "Select Form Type",
        ["Change Order", "Daily Report", "Invoice", "Safety Incident Report"]
    )
    
    if demo_type == "Change Order":
        render_change_order_with_signature()
    elif demo_type == "Daily Report":
        render_daily_report_with_signature()
    elif demo_type == "Invoice":
        render_invoice_with_signature()
    elif demo_type == "Safety Incident Report":
        render_safety_report_with_signature()

def render_change_order_with_signature():
    """Render a change order form with digital signature."""
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
        
        # Signatures
        st.subheader("Signatures")
        
        tabs = st.tabs(["Contractor", "Owner", "Architect"])
        
        with tabs[0]:
            contractor_signature = render_signature_pad(
                key="contractor_signature",
                label="Contractor Signature",
                height=150
            )
        
        with tabs[1]:
            owner_signature = render_signature_pad(
                key="owner_signature", 
                label="Owner Signature",
                height=150
            )
            
        with tabs[2]:
            architect_signature = render_signature_pad(
                key="architect_signature",
                label="Architect Signature",
                height=150
            )
        
        # Submit button
        submitted = st.form_submit_button("Submit Change Order")
        
        if submitted:
            # Save signatures if provided
            signatures_saved = []
            
            if contractor_signature.get("signature"):
                contractor_file = save_signature_to_file(
                    contractor_signature,
                    f"signatures/CO-2025-042-contractor.png"
                )
                signatures_saved.append(f"Contractor: {contractor_signature.get('signer_name')}")
            
            if owner_signature.get("signature"):
                owner_file = save_signature_to_file(
                    owner_signature,
                    f"signatures/CO-2025-042-owner.png"
                )
                signatures_saved.append(f"Owner: {owner_signature.get('signer_name')}")
                
            if architect_signature.get("signature"):
                architect_file = save_signature_to_file(
                    architect_signature,
                    f"signatures/CO-2025-042-architect.png"
                )
                signatures_saved.append(f"Architect: {architect_signature.get('signer_name')}")
            
            # Show success message
            if signatures_saved:
                st.success(f"Change Order submitted with signatures from: {', '.join(signatures_saved)}")
            else:
                st.warning("Change Order saved as draft. No signatures were provided.")
                
            # Show final details
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

def render_daily_report_with_signature():
    """Render a daily report form with digital signature."""
    st.header("Daily Report Form")
    
    with st.form("daily_report_form"):
        # Basic report information
        cols = st.columns(3)
        with cols[0]:
            report_number = st.text_input("Report Number", value="DR-2025-105")
            project = st.text_input("Project", value="Highland Tower Development")
        with cols[1]:
            date = st.date_input("Date", value=datetime.now())
            weather = st.selectbox("Weather", ["Clear", "Cloudy", "Rain", "Snow", "Wind"])
        with cols[2]:
            temp_low = st.number_input("Temperature Low (°F)", value=45)
            temp_high = st.number_input("Temperature High (°F)", value=68)
        
        # Work performed
        st.subheader("Work Performed Today")
        work_performed = st.text_area(
            "Description of Work", 
            value="Completed floor 12 curtain wall installation on east and south faces. Began electrical rough-in for floor 13. Drywall finishing continued on floors 10-11."
        )
        
        # Manpower
        st.subheader("Manpower")
        manpower_data = {
            "Trade": ["Electricians", "Plumbers", "Carpenters", "Ironworkers", "Masons", "Drywall", "Glaziers"],
            "Contractor": ["Electro Inc.", "Plumb Perfect", "Wood Workers Co.", "Steel Team", "Mason Brothers", "Drywall Pro", "Glass Experts"],
            "Workers": [8, 5, 12, 6, 4, 10, 8]
        }
        edited_manpower = st.data_editor(pd.DataFrame(manpower_data), use_container_width=True)
        
        # Equipment
        st.subheader("Equipment On Site")
        equipment_data = {
            "Equipment": ["Tower Crane", "Excavator", "Loader", "Concrete Pump", "Man Lift"],
            "Quantity": [1, 2, 1, 1, 3],
            "Hours": [10, 8, 6, 4, 10]
        }
        edited_equipment = st.data_editor(pd.DataFrame(equipment_data), use_container_width=True)
        
        # Issues/Delays
        st.subheader("Issues and Delays")
        issues = st.text_area(
            "Describe any issues or delays", 
            value="Two-hour morning delay due to high winds affecting tower crane operation. Material delivery for floor 14 electrical delayed to tomorrow."
        )
        
        # Safety
        st.subheader("Safety Observations")
        safety = st.text_area(
            "Safety notes", 
            value="All workers observed using proper fall protection. One near-miss incident with material handling was reported and addressed."
        )
        
        # Photos
        st.subheader("Daily Photos")
        photos = st.file_uploader("Upload Daily Photos", accept_multiple_files=True)
        
        # Signature
        st.subheader("Signatures")
        
        tabs = st.tabs(["Superintendent", "Project Manager"])
        
        with tabs[0]:
            super_signature = render_signature_pad(
                key="superintendent_signature",
                label="Superintendent Signature",
                height=150
            )
        
        with tabs[1]:
            pm_signature = render_signature_pad(
                key="pm_signature", 
                label="Project Manager Signature",
                height=150
            )
        
        # Submit button
        submitted = st.form_submit_button("Submit Daily Report")
        
        if submitted:
            # Save signatures if provided
            signatures_saved = []
            
            if super_signature.get("signature"):
                super_file = save_signature_to_file(
                    super_signature,
                    f"signatures/DR-2025-105-superintendent.png"
                )
                signatures_saved.append(f"Superintendent: {super_signature.get('signer_name')}")
            
            if pm_signature.get("signature"):
                pm_file = save_signature_to_file(
                    pm_signature,
                    f"signatures/DR-2025-105-pm.png"
                )
                signatures_saved.append(f"Project Manager: {pm_signature.get('signer_name')}")
            
            # Show success message
            if signatures_saved:
                st.success(f"Daily Report submitted with signatures from: {', '.join(signatures_saved)}")
            else:
                st.warning("Daily Report saved as draft. No signatures were provided.")

def render_invoice_with_signature():
    """Render an invoice form with digital signature."""
    st.header("Invoice Form")
    
    with st.form("invoice_form"):
        # Basic invoice information
        cols = st.columns(2)
        with cols[0]:
            invoice_number = st.text_input("Invoice Number", value="INV-2025-078")
            project = st.text_input("Project", value="Highland Tower Development")
        with cols[1]:
            date = st.date_input("Date", value=datetime.now())
            due_date = st.date_input("Due Date", value=datetime.now().replace(month=datetime.now().month+1))
        
        # Vendor information
        st.subheader("Vendor Information")
        cols = st.columns(2)
        with cols[0]:
            vendor_name = st.text_input("Vendor Name", value="Elite Electrical Systems")
            vendor_address = st.text_area("Vendor Address", value="123 Contractor Way\nCity, State 12345")
        with cols[1]:
            contact_name = st.text_input("Contact Name", value="John Smith")
            contact_email = st.text_input("Contact Email", value="jsmith@eliteelectrical.com")
            contact_phone = st.text_input("Contact Phone", value="(555) 123-4567")
        
        # Line items
        st.subheader("Invoice Items")
        line_items = {
            "Description": ["Electrical Rough-In (Floors 10-12)", "Light Fixtures (Floor 9)", "Panel Installation (Floor 8)", "Conduit Materials", "Labor (480 hours)"],
            "Quantity": [3, 42, 6, 1, 480],
            "Unit Price": [12500.00, 350.00, 2800.00, 8750.00, 85.00],
            "Amount": [37500.00, 14700.00, 16800.00, 8750.00, 40800.00]
        }
        edited_items = st.data_editor(pd.DataFrame(line_items), use_container_width=True, 
                                      column_config={"Amount": st.column_config.NumberColumn(format="$%.2f")})
        
        # Totals
        subtotal = sum(line_items["Amount"])
        tax_rate = st.slider("Tax Rate (%)", min_value=0.0, max_value=15.0, value=8.0, step=0.1)
        tax_amount = subtotal * (tax_rate / 100)
        total = subtotal + tax_amount
        
        cols = st.columns(2)
        with cols[0]:
            st.metric("Subtotal", f"${subtotal:,.2f}")
            st.metric(f"Tax ({tax_rate}%)", f"${tax_amount:,.2f}")
        with cols[1]:
            st.metric("Total", f"${total:,.2f}")
        
        # Payment information
        st.subheader("Payment Information")
        cols = st.columns(2)
        with cols[0]:
            payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 45", "Net 60", "Due on Receipt"])
        with cols[1]:
            payment_method = st.selectbox("Payment Method", ["Check", "ACH", "Wire Transfer", "Credit Card"])
        
        payment_notes = st.text_area("Payment Notes", value="Please reference invoice number on all payments.")
        
        # Attachments
        st.subheader("Attachments")
        attachments = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True)
        
        # Signature
        st.subheader("Signatures")
        
        tabs = st.tabs(["Vendor", "Approver"])
        
        with tabs[0]:
            vendor_signature = render_signature_pad(
                key="vendor_signature",
                label="Vendor Signature",
                height=150
            )
        
        with tabs[1]:
            approver_signature = render_signature_pad(
                key="approver_signature", 
                label="Approver Signature",
                height=150
            )
        
        # Submit button
        submitted = st.form_submit_button("Submit Invoice")
        
        if submitted:
            # Save signatures if provided
            signatures_saved = []
            
            if vendor_signature.get("signature"):
                vendor_file = save_signature_to_file(
                    vendor_signature,
                    f"signatures/INV-2025-078-vendor.png"
                )
                signatures_saved.append(f"Vendor: {vendor_signature.get('signer_name')}")
            
            if approver_signature.get("signature"):
                approver_file = save_signature_to_file(
                    approver_signature,
                    f"signatures/INV-2025-078-approver.png"
                )
                signatures_saved.append(f"Approver: {approver_signature.get('signer_name')}")
            
            # Show success message
            if signatures_saved:
                st.success(f"Invoice submitted with signatures from: {', '.join(signatures_saved)}")
            else:
                st.warning("Invoice saved as draft. No signatures were provided.")

def render_safety_report_with_signature():
    """Render a safety incident report form with digital signature."""
    st.header("Safety Incident Report")
    
    with st.form("safety_incident_form"):
        # Basic incident information
        cols = st.columns(2)
        with cols[0]:
            incident_number = st.text_input("Incident Number", value="SIR-2025-012")
            project = st.text_input("Project", value="Highland Tower Development")
        with cols[1]:
            date = st.date_input("Incident Date", value=datetime.now())
            time = st.time_input("Incident Time")
        
        # Incident details
        st.subheader("Incident Details")
        
        incident_type = st.selectbox(
            "Incident Type", 
            ["Near Miss", "First Aid", "Medical Treatment", "Lost Time", "Property Damage", "Environmental"]
        )
        
        location = st.text_input("Location of Incident", value="Floor 12, East Wing")
        
        description = st.text_area(
            "Description of Incident", 
            value="Worker slipped on wet surface while carrying materials. No injury occurred, but materials were dropped from approximately 3 feet height."
        )
        
        # Persons involved
        st.subheader("Persons Involved")
        persons_data = {
            "Name": ["James Wilson", "Maria Rodriguez"],
            "Role": ["Carpenter", "Safety Officer"],
            "Company": ["Wood Workers Co.", "GC Construction"],
            "Witness": [True, True],
            "Injured": [False, False]
        }
        edited_persons = st.data_editor(pd.DataFrame(persons_data), use_container_width=True)
        
        # Corrective actions
        st.subheader("Corrective Actions")
        
        immediate_actions = st.text_area(
            "Immediate Actions Taken", 
            value="Area was cordoned off. Spill was cleaned up. Toolbox talk conducted with crew regarding proper housekeeping procedures."
        )
        
        preventive_actions = st.text_area(
            "Preventive Actions", 
            value="Update daily inspection checklist to include verification of surface conditions. Schedule refresher training on material handling procedures."
        )
        
        # Photos
        st.subheader("Incident Photos")
        photos = st.file_uploader("Upload Incident Photos", accept_multiple_files=True)
        
        # Signature
        st.subheader("Signatures")
        
        tabs = st.tabs(["Employee", "Supervisor", "Safety Manager"])
        
        with tabs[0]:
            employee_signature = render_signature_pad(
                key="employee_signature",
                label="Employee Signature",
                height=150
            )
        
        with tabs[1]:
            supervisor_signature = render_signature_pad(
                key="supervisor_signature", 
                label="Supervisor Signature",
                height=150
            )
            
        with tabs[2]:
            safety_manager_signature = render_signature_pad(
                key="safety_manager_signature", 
                label="Safety Manager Signature",
                height=150
            )
        
        # Submit button
        submitted = st.form_submit_button("Submit Safety Incident Report")
        
        if submitted:
            # Save signatures if provided
            signatures_saved = []
            
            if employee_signature.get("signature"):
                employee_file = save_signature_to_file(
                    employee_signature,
                    f"signatures/SIR-2025-012-employee.png"
                )
                signatures_saved.append(f"Employee: {employee_signature.get('signer_name')}")
            
            if supervisor_signature.get("signature"):
                supervisor_file = save_signature_to_file(
                    supervisor_signature,
                    f"signatures/SIR-2025-012-supervisor.png"
                )
                signatures_saved.append(f"Supervisor: {supervisor_signature.get('signer_name')}")
                
            if safety_manager_signature.get("signature"):
                safety_manager_file = save_signature_to_file(
                    safety_manager_signature,
                    f"signatures/SIR-2025-012-safety-manager.png"
                )
                signatures_saved.append(f"Safety Manager: {safety_manager_signature.get('signer_name')}")
            
            # Show success message
            if signatures_saved:
                st.success(f"Safety Incident Report submitted with signatures from: {', '.join(signatures_saved)}")
            else:
                st.warning("Safety Incident Report saved as draft. No signatures were provided.")