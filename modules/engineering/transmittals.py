"""
Transmittals functionality for the Engineering module.

This module provides functions for working with transmittals, which are formal
document packages sent between project stakeholders.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from enum import Enum

class TransmittalStatus(Enum):
    DRAFT = "Draft"
    SENT = "Sent" 
    RECEIVED = "Received"
    ACKNOWLEDGED = "Acknowledged"
    COMPLETED = "Completed"


def render_transmittals():
    """Render the Transmittals section"""
    
    st.header("Transmittals")
    
    # Header with Create Transmittal button at the top
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col3:
        if st.button("Create New Transmittal", type="primary", key="create_transmittal_btn", use_container_width=True):
            st.session_state.show_transmittal_form = True
            st.session_state.edit_transmittal_id = None
    
    # Transmittal form (would be expanded in a real implementation)
    if st.session_state.get("show_transmittal_form", False):
        with st.form("transmittal_form"):
            st.subheader("New Transmittal")
            
            # Basic transmittal fields
            col1, col2 = st.columns(2)
            
            with col1:
                transmittal_number = st.text_input("Transmittal Number", value=f"TR-{random.randint(100, 999)}")
                transmittal_date = st.date_input("Date", value=datetime.now())
                recipient = st.selectbox(
                    "To", 
                    ["Architect", "Owner", "Structural Engineer", "MEP Engineer", "Civil Engineer"]
                )
            
            with col2:
                sender = st.text_input("From", value="General Contractor")
                status = st.selectbox(
                    "Status", 
                    [status.value for status in TransmittalStatus]
                )
                delivery_method = st.selectbox(
                    "Delivery Method", 
                    ["Email", "Courier", "Mail", "FedEx", "Project Management System"]
                )
            
            # Description and purpose
            st.text_area("Description", placeholder="Brief description of transmittal contents")
            
            purpose_options = [
                "For Your Information",
                "For Your Review",
                "For Your Approval",
                "For Your Use",
                "As Requested",
                "Returned After Loan",
                "Resubmittal"
            ]
            
            purpose_cols = st.columns(3)
            purpose_selected = {}
            
            for i, purpose in enumerate(purpose_options):
                col_index = i % 3
                with purpose_cols[col_index]:
                    purpose_selected[purpose] = st.checkbox(purpose)
            
            # Document section
            st.subheader("Documents")
            
            document_options = [
                "Drawings",
                "Specifications",
                "Shop Drawings",
                "Submittals",
                "Samples",
                "Product Data",
                "Calculations",
                "Test Reports",
                "Meeting Minutes",
                "Other"
            ]
            
            document_cols = st.columns(2)
            document_selected = {}
            
            for i, doc_type in enumerate(document_options):
                col_index = i % 2
                with document_cols[col_index]:
                    document_selected[doc_type] = st.checkbox(doc_type, key=f"doc_{doc_type}")
            
            # Document upload
            uploaded_files = st.file_uploader(
                "Upload Documents", 
                accept_multiple_files=True,
                type=["pdf", "doc", "docx", "xls", "xlsx", "jpg", "jpeg", "png"],
                key="transmittal_files"
            )
            
            # Attachments list
            if uploaded_files:
                file_table = []
                for i, file in enumerate(uploaded_files):
                    file_table.append({
                        "Name": file.name,
                        "Size": f"{round(file.size / 1024, 1)} KB",
                        "Type": file.type
                    })
                
                st.dataframe(pd.DataFrame(file_table))
            
            # Remarks
            st.text_area("Remarks", placeholder="Any additional notes or remarks")
            
            # Form buttons
            col1, col2 = st.columns([1, 6])
            
            with col1:
                cancel = st.form_submit_button("Cancel")
            
            with col2:
                submitted = st.form_submit_button("Save Transmittal")
            
            # Handle form submission
            if submitted:
                st.success("Transmittal saved successfully!")
                st.session_state.show_transmittal_form = False
                st.rerun()
            
            if cancel:
                st.session_state.show_transmittal_form = False
                st.rerun()
    
    # Only show the list if not in form mode
    if not st.session_state.get("show_transmittal_form", False):
        # Sample data for transmittals
        transmittals = []
        
        # Generate sample transmittals
        for i in range(1, 21):
            # Generate dates with realistic workflow
            transmittal_date = datetime.now() - timedelta(days=random.randint(5, 60))
            
            # Components for a transmittal
            components = ["Drawings", "Specifications", "Shop Drawings", "Submittals", "Product Data"]
            included_components = random.sample(components, k=random.randint(1, 3))
            
            transmittals.append({
                "id": f"TR-{i:03d}",
                "number": i,
                "date": transmittal_date,
                "recipient": random.choice([
                    "Architect", "Owner", "Structural Engineer", 
                    "MEP Engineer", "Civil Engineer"
                ]),
                "sender": "General Contractor",
                "status": random.choice([status.value for status in TransmittalStatus]),
                "delivery_method": random.choice([
                    "Email", "Courier", "Mail", "FedEx", "Project Management System"
                ]),
                "components": ", ".join(included_components),
                "document_count": random.randint(1, 5)
            })
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.multiselect(
                "Status",
                [status.value for status in TransmittalStatus],
                default=[],
                key="transmittal_status_filter"
            )
        
        with col2:
            recipient_filter = st.multiselect(
                "Recipient",
                list(set(t["recipient"] for t in transmittals)),
                default=[],
                key="transmittal_recipient_filter"
            )
        
        with col3:
            date_range = st.date_input(
                "Date Range",
                value=(
                    datetime.now() - timedelta(days=60),
                    datetime.now()
                ),
                key="transmittal_date_filter"
            )
        
        # Apply filters
        filtered_transmittals = transmittals
        
        if status_filter:
            filtered_transmittals = [t for t in filtered_transmittals if t["status"] in status_filter]
        
        if recipient_filter:
            filtered_transmittals = [t for t in filtered_transmittals if t["recipient"] in recipient_filter]
        
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_transmittals = [
                t for t in filtered_transmittals 
                if start_date <= t["date"].date() <= end_date
            ]
        
        # Display transmittal list
        if filtered_transmittals:
            # Create DataFrame
            df = pd.DataFrame(filtered_transmittals)
            
            # Format for display
            display_df = df.copy()
            display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
            display_df["view"] = "View"
            
            # Prepare columns for display
            display_df = display_df[["id", "date", "recipient", "sender", "status", "components", "document_count", "view"]]
            
            # Create a nice table display
            st.dataframe(
                display_df,
                column_config={
                    "id": "Transmittal #",
                    "date": "Date",
                    "recipient": "To",
                    "sender": "From",
                    "status": st.column_config.TextColumn(
                        "Status",
                        help="Current status of the transmittal"
                    ),
                    "components": "Components",
                    "document_count": "Documents",
                    "view": "Action"
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Handle view button clicks
            if st.session_state.get("dataframe_clicked_row") and st.session_state.dataframe_clicked_row.get("view") == "View":
                row_index = st.session_state.dataframe_clicked_row_index
                selected_transmittal = transmittals[row_index]
                
                with st.expander(f"Transmittal {selected_transmittal['id']}", expanded=True):
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        st.write("**Date:**", selected_transmittal["date"].strftime("%Y-%m-%d"))
                        st.write("**From:**", selected_transmittal["sender"])
                        st.write("**Delivery Method:**", selected_transmittal["delivery_method"])
                    
                    with col2:
                        st.write("**To:**", selected_transmittal["recipient"])
                        st.write("**Status:**", selected_transmittal["status"])
                        st.write("**Components:**", selected_transmittal["components"])
                    
                    with col3:
                        st.write("**Documents:**", selected_transmittal["document_count"])
                        
                        # Action buttons
                        st.button("Print Transmittal", key=f"print_{selected_transmittal['id']}")
                        st.button("Download Documents", key=f"download_{selected_transmittal['id']}")
                    
                    # Documents table
                    st.subheader("Documents")
                    
                    # Generate sample document data
                    docs = []
                    for j in range(selected_transmittal["document_count"]):
                        doc_type = random.choice(selected_transmittal["components"].split(", "))
                        if doc_type == "Drawings":
                            name = f"Drawing {chr(65 + j)}-{random.randint(100, 999)}"
                        elif doc_type == "Specifications":
                            name = f"Spec Section {random.randint(1, 50)} {random.randint(10, 99)} {random.randint(10, 99)}"
                        elif doc_type == "Shop Drawings":
                            name = f"Shop Drawing SD-{random.randint(100, 999)}"
                        else:
                            name = f"Document {chr(65 + j)}-{random.randint(100, 999)}"
                            
                        docs.append({
                            "type": doc_type,
                            "name": name,
                            "format": random.choice(["PDF", "DOC", "XLS"]),
                            "size": f"{random.randint(100, 9999)} KB"
                        })
                    
                    # Display documents
                    st.dataframe(
                        pd.DataFrame(docs),
                        column_config={
                            "type": "Type",
                            "name": "Name",
                            "format": "Format",
                            "size": "Size"
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # History section
                    st.subheader("Transmittal History")
                    
                    # Generate sample history
                    history = [
                        {
                            "date": selected_transmittal["date"].strftime("%Y-%m-%d"),
                            "status": "Created",
                            "by": "John Smith",
                            "notes": "Transmittal created"
                        }
                    ]
                    
                    # Add some history entries based on status
                    if selected_transmittal["status"] in ["Sent", "Received", "Acknowledged", "Completed"]:
                        sent_date = selected_transmittal["date"] + timedelta(days=1)
                        history.append({
                            "date": sent_date.strftime("%Y-%m-%d"),
                            "status": "Sent",
                            "by": "John Smith",
                            "notes": f"Sent via {selected_transmittal['delivery_method']}"
                        })
                    
                    if selected_transmittal["status"] in ["Received", "Acknowledged", "Completed"]:
                        received_date = selected_transmittal["date"] + timedelta(days=3)
                        history.append({
                            "date": received_date.strftime("%Y-%m-%d"),
                            "status": "Received",
                            "by": "Jane Doe",
                            "notes": "Delivery confirmed"
                        })
                    
                    if selected_transmittal["status"] in ["Acknowledged", "Completed"]:
                        ack_date = selected_transmittal["date"] + timedelta(days=5)
                        history.append({
                            "date": ack_date.strftime("%Y-%m-%d"),
                            "status": "Acknowledged",
                            "by": "Robert Johnson",
                            "notes": "Receipt acknowledged"
                        })
                    
                    if selected_transmittal["status"] == "Completed":
                        complete_date = selected_transmittal["date"] + timedelta(days=10)
                        history.append({
                            "date": complete_date.strftime("%Y-%m-%d"),
                            "status": "Completed",
                            "by": "Robert Johnson",
                            "notes": "All documents reviewed and processed"
                        })
                    
                    # Display history
                    st.dataframe(
                        pd.DataFrame(history),
                        column_config={
                            "date": "Date",
                            "status": "Status",
                            "by": "By",
                            "notes": "Notes"
                        },
                        hide_index=True,
                        use_container_width=True
                    )
        else:
            st.info("No transmittals found matching the selected filters.")