"""
RFI form component with integrated relationship management.

This module extends the basic RFI form with the ability to establish
relationships between RFIs and other project entities.
"""

import streamlit as st
from datetime import datetime, timedelta
import random
from typing import Dict, Any, Tuple, Optional

from components.relationship_picker import render_relationship_picker, render_document_relationship_picker

def rfi_form_with_relationships(
    is_edit: bool = False, 
    rfi_data: Optional[Dict[str, Any]] = None,
    project_id: Optional[str] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Render an enhanced RFI form with relationship management.
    
    Args:
        is_edit: Whether this is an edit form or a new RFI
        rfi_data: Existing RFI data for editing
        project_id: Optional project ID for project association
        
    Returns:
        Tuple of (form_submitted, form_data)
    """
    form_title = "Edit RFI" if is_edit else "Create RFI"
    
    # Default values
    if rfi_data is None:
        rfi_data = {}
    
    rfi_id = rfi_data.get("id", f"RFI-{random.randint(1000, 9999)}")
    
    with st.form(key=f"rfi_form_{rfi_id}"):
        st.subheader(form_title)
        
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input(
                "Title",
                value=rfi_data.get("title", ""),
                placeholder="Brief descriptive title"
            )
            
            discipline = st.selectbox(
                "Discipline",
                [
                    "Architectural", "Structural", "Mechanical", "Electrical", 
                    "Plumbing", "Civil", "Landscape", "Fire Protection", "Technology", "Other"
                ],
                index=[
                    "Architectural", "Structural", "Mechanical", "Electrical", 
                    "Plumbing", "Civil", "Landscape", "Fire Protection", "Technology", "Other"
                ].index(rfi_data.get("discipline", "Architectural")) if "discipline" in rfi_data else 0
            )
            
            location = st.selectbox(
                "Location",
                [
                    "Building A - Level 1", "Building A - Level 2", "Building A - Level 3", 
                    "Building B - Level 1", "Site", "Parking Garage", "Mechanical Room", 
                    "Electrical Room", "Roof"
                ],
                index=[
                    "Building A - Level 1", "Building A - Level 2", "Building A - Level 3", 
                    "Building B - Level 1", "Site", "Parking Garage", "Mechanical Room", 
                    "Electrical Room", "Roof"
                ].index(rfi_data.get("location", "Building A - Level 1")) if "location" in rfi_data else 0
            )
        
        with col2:
            status = st.selectbox(
                "Status",
                ["Draft", "Submitted", "Under Review", "Answered", "Closed", "Overdue"],
                index=["Draft", "Submitted", "Under Review", "Answered", "Closed", "Overdue"].index(
                    rfi_data.get("status", "Draft")) if "status" in rfi_data else 0
            )
            
            submitted_by = st.text_input(
                "Submitted By",
                value=rfi_data.get("submitted_by", "John Smith"),
                placeholder="Name of submitter"
            )
            
            due_date = st.date_input(
                "Due Date",
                value=datetime.strptime(rfi_data.get("due_date"), "%Y-%m-%d").date() 
                if "due_date" in rfi_data else datetime.now().date() + timedelta(days=7)
            )
        
        # Description and supplemental information
        st.subheader("Details")
        
        description = st.text_area(
            "Description/Question",
            value=rfi_data.get("description", ""),
            placeholder="Detailed description of the issue and question",
            height=150
        )
        
        # RFI response (if editing)
        if is_edit and rfi_data.get("status") in ["Answered", "Closed"]:
            response = st.text_area(
                "Response",
                value=rfi_data.get("response", ""),
                placeholder="Response to the RFI",
                height=150
            )
            
            response_date = st.date_input(
                "Response Date",
                value=datetime.strptime(rfi_data.get("response_date"), "%Y-%m-%d").date() 
                if "response_date" in rfi_data else datetime.now().date()
            )
        else:
            response = None
            response_date = None
        
        # Impact assessment
        st.subheader("Impact Assessment")
        
        cost_impact = st.checkbox(
            "Potential Cost Impact",
            value=rfi_data.get("cost_impact", False)
        )
        
        schedule_impact = st.checkbox(
            "Potential Schedule Impact",
            value=rfi_data.get("schedule_impact", False)
        )
        
        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High", "Critical"],
            index=["Low", "Medium", "High", "Critical"].index(
                rfi_data.get("priority", "Medium")) if "priority" in rfi_data else 1
        )
        
        # Attachments (in a real app, this would be a file uploader)
        st.subheader("Attachments")
        attachments = st.file_uploader(
            "Upload Attachments",
            accept_multiple_files=True,
            type=["pdf", "jpg", "jpeg", "png", "dwg"]
        )
        
        # Relationships section (outside the form since it has its own submit buttons)
        st.subheader("Relationships")
        st.info("You can add relationships after saving the RFI.")
        
        # Form buttons
        col1, col2 = st.columns([1, 4])
        with col1:
            submit_button = st.form_submit_button("Save RFI")
        with col2:
            cancel_button = st.form_submit_button("Cancel")
        
    # Construct form data
    form_data = {}
    form_submitted = False
    
    if submit_button:
        form_data = {
            "title": title,
            "discipline": discipline,
            "location": location,
            "status": status,
            "submitted_by": submitted_by,
            "due_date": due_date.strftime("%Y-%m-%d"),
            "description": description,
            "cost_impact": cost_impact,
            "schedule_impact": schedule_impact,
            "priority": priority,
            "attachments": attachments
        }
        
        # Add response fields if present
        if response:
            form_data["response"] = response
        if response_date:
            form_data["response_date"] = response_date.strftime("%Y-%m-%d")
        
        # Add the RFI ID for existing RFIs
        if is_edit:
            form_data["id"] = rfi_id
        
        form_submitted = True
    
    # If canceled
    if cancel_button:
        form_submitted = True
        form_data = {"canceled": True}
    
    # Display relationships section after form is submitted to create a new RFI
    if is_edit:
        st.subheader("Manage Relationships")
        
        # Tab for different relationship types
        rel_tab1, rel_tab2 = st.tabs(["Project Items", "Documents"])
        
        with rel_tab1:
            # Render relationship picker for project items
            render_relationship_picker(
                entity_id=rfi_id,
                entity_type="RFI",
                key_prefix=f"rfi_{rfi_id}"
            )
        
        with rel_tab2:
            # Render document relationship picker
            render_document_relationship_picker(
                entity_id=rfi_id,
                entity_type="RFI",
                key_prefix=f"rfi_doc_{rfi_id}"
            )
    
    return form_submitted, form_data