"""
Engineering form components for Streamlit interface.

This module provides reusable form components for engineering items
such as RFIs and submittals with consistent styling and validation.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from components.form_helper import form_input_field, validate_form, form_action_buttons

# RFI Form Components
def rfi_form(is_edit=False, rfi_data=None):
    """
    Render a reusable RFI form with validation
    
    Args:
        is_edit: Whether this is an edit form or a new RFI
        rfi_data: Existing RFI data for editing
        
    Returns:
        Tuple of (form_submitted, form_data)
    """
    form_submitted = False
    form_data = {}
    
    # Common RFI form fields
    disciplines = [
        "Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", 
        "Civil", "Landscape", "Fire Protection", "Technology", "Other"
    ]
    
    locations = [
        "Building A - Level 1", "Building A - Level 2", "Building A - Level 3", 
        "Building B - Level 1", "Site", "Parking Garage", "Mechanical Room", 
        "Electrical Room", "Roof"
    ]
    
    responsibles = [
        "Architect", "Structural Engineer", "MEP Engineer", "Civil Engineer", 
        "Landscape Architect", "Owner", "General Contractor"
    ]
    
    priorities = ["Low", "Medium", "High", "Critical"]
    
    # Initialize error container
    if "form_errors" not in st.session_state:
        st.session_state.form_errors = {}
    
    with st.form(key=f"rfi_form_{'edit' if is_edit else 'new'}"):
        st.subheader(f"{'Edit' if is_edit else 'Create New'} RFI")
        
        # Extract defaults from existing data if editing
        defaults = {}
        if is_edit and rfi_data:
            defaults = {
                "title": rfi_data.get("title", ""),
                "discipline": rfi_data.get("discipline", ""),
                "location": rfi_data.get("location", ""),
                "priority": rfi_data.get("priority", "Medium"),
                "description": rfi_data.get("description", ""),
                "submitted_by": rfi_data.get("submitted_by", ""),
                "responsible": rfi_data.get("responsible", ""),
                "due_date": rfi_data.get("due_date", datetime.now() + timedelta(days=7)),
                "cost_impact": rfi_data.get("cost_impact", False),
                "schedule_impact": rfi_data.get("schedule_impact", False)
            }
        
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            title, title_error = form_input_field(
                "Title", 
                "rfi_title", 
                default=defaults.get("title", ""),
                required=True
            )
            form_data["title"] = title_error
            
            discipline, discipline_error = form_input_field(
                "Discipline",
                "rfi_discipline",
                field_type="select",
                options=disciplines,
                default=defaults.get("discipline", disciplines[0]),
                required=True
            )
            form_data["discipline"] = discipline_error
            
            location, location_error = form_input_field(
                "Location",
                "rfi_location",
                field_type="select",
                options=locations,
                default=defaults.get("location", locations[0])
            )
            form_data["location"] = location_error
            
            priority, priority_error = form_input_field(
                "Priority",
                "rfi_priority",
                field_type="select",
                options=priorities,
                default=defaults.get("priority", "Medium")
            )
            form_data["priority"] = priority_error
            
            submitted_by, submitted_by_error = form_input_field(
                "Submitted By",
                "rfi_submitted_by",
                default=defaults.get("submitted_by", ""),
                required=True
            )
            form_data["submitted_by"] = submitted_by_error
        
        with form_col2:
            responsible, responsible_error = form_input_field(
                "Responsible Party",
                "rfi_responsible",
                field_type="select",
                options=responsibles,
                default=defaults.get("responsible", responsibles[0]),
                required=True
            )
            form_data["responsible"] = responsible_error
            
            due_date, due_date_error = form_input_field(
                "Due Date",
                "rfi_due_date",
                field_type="date",
                default=defaults.get("due_date", datetime.now() + timedelta(days=7)),
                min_value=datetime.now(),
                required=True
            )
            form_data["due_date"] = due_date_error
            
            cost_impact, _ = form_input_field(
                "Cost Impact",
                "rfi_cost_impact",
                field_type="checkbox",
                default=defaults.get("cost_impact", False)
            )
            
            schedule_impact, _ = form_input_field(
                "Schedule Impact",
                "rfi_schedule_impact",
                field_type="checkbox",
                default=defaults.get("schedule_impact", False)
            )
        
        description, description_error = form_input_field(
            "Description",
            "rfi_description",
            field_type="textarea",
            default=defaults.get("description", ""),
            required=True,
            height=150
        )
        form_data["description"] = description_error
        
        # File upload
        attachments = st.file_uploader("Add Attachments", accept_multiple_files=True, key="rfi_attachments")
        
        # Form buttons
        submit_primary, submit_draft, _ = form_action_buttons(
            primary_label="Submit",
            secondary_label="Save as Draft",
            alignment="right"
        )
        
        # Handle form submission
        if submit_primary or submit_draft:
            form_is_valid = validate_form(form_data)
            
            if form_is_valid:
                # Collect form data
                form_result = {
                    "title": title,
                    "discipline": discipline,
                    "location": location,
                    "priority": priority,
                    "submitted_by": submitted_by,
                    "responsible": responsible,
                    "due_date": due_date,
                    "cost_impact": cost_impact,
                    "schedule_impact": schedule_impact,
                    "description": description,
                    "attachments": attachments,
                    "status": "Submitted" if submit_primary else "Draft"
                }
                
                # Clear form errors
                st.session_state.form_errors = {}
                
                # Set form submitted flag
                form_submitted = True
                
                # Show success message
                st.success(f"RFI {'submitted' if submit_primary else 'saved as draft'} successfully!")
                
                # Return form result
                return form_submitted, form_result
    
    # Return empty result if form wasn't submitted or had errors
    return form_submitted, None

# Submittal Form Components
def submittal_form(is_edit=False, submittal_data=None):
    """
    Render a reusable submittal form with validation
    
    Args:
        is_edit: Whether this is an edit form or a new submittal
        submittal_data: Existing submittal data for editing
        
    Returns:
        Tuple of (form_submitted, form_data)
    """
    form_submitted = False
    form_data = {}
    
    # Common submittal form fields
    specification_sections = [
        "03 30 00 - Cast-in-Place Concrete",
        "04 20 00 - Unit Masonry",
        "05 12 00 - Structural Steel Framing",
        "06 40 00 - Architectural Woodwork",
        "07 21 00 - Thermal Insulation",
        "07 52 00 - Modified Bituminous Membrane Roofing",
        "08 11 13 - Hollow Metal Doors and Frames",
        "08 71 00 - Door Hardware",
        "09 29 00 - Gypsum Board",
        "09 51 13 - Acoustical Panel Ceilings",
        "09 65 13 - Resilient Base and Accessories",
        "09 91 23 - Interior Painting",
        "21 13 13 - Wet-Pipe Sprinkler Systems",
        "22 40 00 - Plumbing Fixtures",
        "23 37 13 - Diffusers, Registers, and Grilles",
        "26 51 00 - Interior Lighting"
    ]
    
    submittal_types = [
        "Product Data", "Shop Drawings", "Samples", "Certificates", 
        "Test Reports", "Mix Designs", "Cut Sheets"
    ]
    
    submitting_parties = [
        "General Contractor",
        "Concrete Subcontractor", 
        "Masonry Subcontractor",
        "Steel Subcontractor",
        "Carpentry Subcontractor",
        "Insulation Subcontractor",
        "Roofing Subcontractor",
        "Door & Hardware Subcontractor",
        "Drywall Subcontractor",
        "Ceiling Subcontractor",
        "Flooring Subcontractor",
        "Painting Subcontractor",
        "Fire Protection Subcontractor",
        "Plumbing Subcontractor",
        "HVAC Subcontractor",
        "Electrical Subcontractor"
    ]
    
    reviewing_parties = [
        "Architect",
        "Structural Engineer",
        "MEP Engineer",
        "Civil Engineer",
        "Interior Designer",
        "Owner"
    ]
    
    priorities = ["Low", "Medium", "High"]
    
    # Initialize error container
    if "form_errors" not in st.session_state:
        st.session_state.form_errors = {}
    
    with st.form(key=f"submittal_form_{'edit' if is_edit else 'new'}"):
        st.subheader(f"{'Edit' if is_edit else 'Create New'} Submittal")
        
        # Extract defaults from existing data if editing
        defaults = {}
        if is_edit and submittal_data:
            defaults = {
                "spec_section": submittal_data.get("spec_section", ""),
                "submittal_type": submittal_data.get("submittal_type", ""),
                "title": submittal_data.get("title", ""),
                "submitting_party": submittal_data.get("submitting_party", ""),
                "reviewing_party": submittal_data.get("reviewing_party", ""),
                "priority": submittal_data.get("priority", "Medium"),
                "due_date": submittal_data.get("due_date", datetime.now() + timedelta(days=14)),
                "description": submittal_data.get("description", "")
            }
        
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            spec_section, spec_section_error = form_input_field(
                "Specification Section",
                "submittal_spec",
                field_type="select",
                options=specification_sections,
                default=defaults.get("spec_section", specification_sections[0]),
                required=True
            )
            form_data["spec_section"] = spec_section_error
            
            submittal_type, submittal_type_error = form_input_field(
                "Submittal Type",
                "submittal_type",
                field_type="select",
                options=submittal_types,
                default=defaults.get("submittal_type", submittal_types[0]),
                required=True
            )
            form_data["submittal_type"] = submittal_type_error
            
            title, title_error = form_input_field(
                "Title",
                "submittal_title",
                default=defaults.get("title", ""),
                required=True
            )
            form_data["title"] = title_error
            
            submitting_party, submitting_party_error = form_input_field(
                "Submitting Party",
                "submittal_submitter",
                field_type="select",
                options=submitting_parties,
                default=defaults.get("submitting_party", submitting_parties[0]),
                required=True
            )
            form_data["submitting_party"] = submitting_party_error
        
        with form_col2:
            reviewing_party, reviewing_party_error = form_input_field(
                "Reviewing Party",
                "submittal_reviewer",
                field_type="select",
                options=reviewing_parties,
                default=defaults.get("reviewing_party", reviewing_parties[0]),
                required=True
            )
            form_data["reviewing_party"] = reviewing_party_error
            
            priority, priority_error = form_input_field(
                "Priority",
                "submittal_priority",
                field_type="select",
                options=priorities,
                default=defaults.get("priority", "Medium")
            )
            form_data["priority"] = priority_error
            
            due_date, due_date_error = form_input_field(
                "Due Date",
                "submittal_due_date",
                field_type="date",
                default=defaults.get("due_date", datetime.now() + timedelta(days=14)),
                min_value=datetime.now(),
                required=True
            )
            form_data["due_date"] = due_date_error
        
        description, description_error = form_input_field(
            "Description",
            "submittal_description",
            field_type="textarea",
            default=defaults.get("description", ""),
            required=True,
            height=100
        )
        form_data["description"] = description_error
        
        # File upload
        attachments = st.file_uploader("Add Attachments", accept_multiple_files=True, key="submittal_attachments")
        
        # Form buttons
        submit_primary, submit_draft, _ = form_action_buttons(
            primary_label="Submit",
            secondary_label="Save as Draft",
            alignment="right"
        )
        
        # Handle form submission
        if submit_primary or submit_draft:
            form_is_valid = validate_form(form_data)
            
            if form_is_valid:
                # Collect form data
                form_result = {
                    "spec_section": spec_section,
                    "submittal_type": submittal_type,
                    "title": title,
                    "submitting_party": submitting_party,
                    "reviewing_party": reviewing_party,
                    "priority": priority,
                    "due_date": due_date,
                    "description": description,
                    "attachments": attachments,
                    "status": "Submitted" if submit_primary else "Draft"
                }
                
                # Clear form errors
                st.session_state.form_errors = {}
                
                # Set form submitted flag
                form_submitted = True
                
                # Show success message
                st.success(f"Submittal {'submitted' if submit_primary else 'saved as draft'} successfully!")
                
                # Return form result
                return form_submitted, form_result
    
    # Return empty result if form wasn't submitted or had errors
    return form_submitted, None