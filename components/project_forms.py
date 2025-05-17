"""
Project form components for creating and editing projects.

This module provides UI components for project creation and editing forms.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date

def project_create_form():
    """
    Display form for creating a new construction project.
    
    Returns:
        dict: Project data if form is submitted, None otherwise
    """
    # Form container with card styling
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("Create New Project")
    
    # Create a form
    with st.form("new_project_form"):
        # Project basic information
        st.markdown("### Project Information")
        
        # First row - Project Name and Code
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name", 
                placeholder="Enter project name", 
                help="Full name of the project")
        
        with col2:
            project_code = st.text_input("Project Code", 
                placeholder="e.g., PRJ-2025-001", 
                help="Unique project identifier code")
        
        # Second row - Client and Project Type
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("Client", 
                placeholder="Enter client name", 
                help="Name of the client or owner")
        
        with col2:
            project_type = st.selectbox("Project Type", 
                options=["Commercial", "Residential", "Industrial", "Infrastructure", "Mixed-Use", "Healthcare", "Education", "Other"],
                help="Type of construction project")
        
        # Third row - Address and Location
        col1, col2 = st.columns(2)
        
        with col1:
            address = st.text_input("Address", 
                placeholder="Project address", 
                help="Physical address of the project")
        
        with col2:
            location = st.text_input("City/State", 
                placeholder="City, State", 
                help="City and state of the project")
        
        # Fourth row - Dates
        col1, col2, col3 = st.columns(3)
        
        today = date.today()
        with col1:
            start_date = st.date_input("Start Date", 
                value=today,
                help="Planned start date of the project")
        
        with col2:
            end_date = st.date_input("End Date", 
                value=today + timedelta(days=365),
                help="Planned completion date of the project")
        
        with col3:
            duration = st.number_input("Duration (days)", 
                min_value=1, 
                value=(end_date - start_date).days,
                help="Project duration in days")
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
        
        # Budget and Cost section
        st.markdown("### Budget Information")
        
        # First row - Budget, Contingency, and Total
        col1, col2, col3 = st.columns(3)
        
        with col1:
            base_budget = st.number_input("Base Budget ($)", 
                min_value=0, 
                value=1000000,
                step=10000,
                help="Base project budget excluding contingency")
        
        with col2:
            contingency_percent = st.number_input("Contingency (%)", 
                min_value=0.0, 
                max_value=100.0,
                value=10.0,
                step=0.5,
                help="Contingency percentage")
            
            contingency_amount = base_budget * (contingency_percent / 100)
        
        with col3:
            total_budget = base_budget + contingency_amount
            st.metric("Total Budget", f"${total_budget:,.2f}")
        
        # Second row - Contract Type and Payment Terms
        col1, col2 = st.columns(2)
        
        with col1:
            contract_type = st.selectbox("Contract Type", 
                options=["Fixed Price", "Cost Plus", "Guaranteed Maximum Price", "Time & Materials", "Unit Price", "Other"],
                help="Type of construction contract")
        
        with col2:
            payment_terms = st.selectbox("Payment Terms", 
                options=["Monthly", "Milestone-based", "Progress-based", "Custom"],
                help="Project payment terms")
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
        
        # Team and Management section
        st.markdown("### Team Information")
        
        # First row - Project Manager and Superintendent
        col1, col2 = st.columns(2)
        
        with col1:
            project_manager = st.text_input("Project Manager", 
                placeholder="Enter name", 
                help="Name of the project manager")
        
        with col2:
            superintendent = st.text_input("Superintendent", 
                placeholder="Enter name", 
                help="Name of the field superintendent")
        
        # Second row - Architect and Engineer
        col1, col2 = st.columns(2)
        
        with col1:
            architect = st.text_input("Architect", 
                placeholder="Enter name/firm", 
                help="Name of the architecture firm")
        
        with col2:
            engineer = st.text_input("Engineer", 
                placeholder="Enter name/firm", 
                help="Name of the engineering firm")
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
        
        # Additional Information
        st.markdown("### Additional Information")
        
        # Description
        description = st.text_area("Project Description", 
            placeholder="Enter a brief description of the project...",
            height=100,
            help="Detailed description of the project scope")
        
        # Status and priority
        col1, col2 = st.columns(2)
        
        with col1:
            status = st.selectbox("Project Status", 
                options=["Planning", "Preconstruction", "Active", "On Hold", "Closed"],
                help="Current status of the project")
        
        with col2:
            priority = st.selectbox("Priority", 
                options=["Low", "Medium", "High", "Critical"],
                help="Project priority level")
        
        # Submit button
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Create Project", use_container_width=True)
        
        if submitted:
            if not project_name or not project_code:
                st.error("Project Name and Project Code are required fields.")
                return None
            
            # Collect form data
            project_data = {
                "name": project_name,
                "code": project_code,
                "client": client_name,
                "type": project_type,
                "address": address,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "duration": duration,
                "base_budget": base_budget,
                "contingency_percent": contingency_percent,
                "contingency_amount": contingency_amount,
                "total_budget": total_budget,
                "contract_type": contract_type,
                "payment_terms": payment_terms,
                "project_manager": project_manager,
                "superintendent": superintendent,
                "architect": architect,
                "engineer": engineer,
                "description": description,
                "status": status,
                "priority": priority,
                "created_at": datetime.now(),
                "created_by": st.session_state.get("user_id", "admin")
            }
            
            return project_data
    
    # Close the form container
    st.markdown('</div>', unsafe_allow_html=True)
    return None

def project_edit_form(project_data=None):
    """
    Display form for editing an existing project.
    
    Args:
        project_data (dict): Existing project data
        
    Returns:
        dict: Updated project data if form is submitted, None otherwise
    """
    if not project_data:
        st.error("No project data provided for editing.")
        return None
    
    # Form container with card styling
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader(f"Edit Project: {project_data.get('name', '')}")
    
    # Create a form
    with st.form("edit_project_form"):
        # Project basic information
        st.markdown("### Project Information")
        
        # First row - Project Name and Code
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name", 
                value=project_data.get("name", ""),
                help="Full name of the project")
        
        with col2:
            project_code = st.text_input("Project Code", 
                value=project_data.get("code", ""),
                help="Unique project identifier code",
                disabled=True)  # Code shouldn't be changed once set
        
        # Second row - Client and Project Type
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("Client", 
                value=project_data.get("client", ""),
                help="Name of the client or owner")
        
        with col2:
            project_type = st.selectbox("Project Type", 
                options=["Commercial", "Residential", "Industrial", "Infrastructure", "Mixed-Use", "Healthcare", "Education", "Other"],
                index=["Commercial", "Residential", "Industrial", "Infrastructure", "Mixed-Use", "Healthcare", "Education", "Other"].index(project_data.get("type", "Commercial")),
                help="Type of construction project")
        
        # Third row - Address and Location
        col1, col2 = st.columns(2)
        
        with col1:
            address = st.text_input("Address", 
                value=project_data.get("address", ""),
                help="Physical address of the project")
        
        with col2:
            location = st.text_input("City/State", 
                value=project_data.get("location", ""),
                help="City and state of the project")
        
        # Fourth row - Dates
        col1, col2, col3 = st.columns(3)
        
        with col1:
            start_date = st.date_input("Start Date", 
                value=project_data.get("start_date", date.today()),
                help="Planned start date of the project")
        
        with col2:
            end_date = st.date_input("End Date", 
                value=project_data.get("end_date", date.today() + timedelta(days=365)),
                help="Planned completion date of the project")
        
        with col3:
            duration = st.number_input("Duration (days)", 
                min_value=1, 
                value=project_data.get("duration", (end_date - start_date).days),
                help="Project duration in days")
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
        
        # Budget and Cost section
        st.markdown("### Budget Information")
        
        # First row - Budget, Contingency, and Total
        col1, col2, col3 = st.columns(3)
        
        with col1:
            base_budget = st.number_input("Base Budget ($)", 
                min_value=0, 
                value=int(project_data.get("base_budget", 1000000)),
                step=10000,
                help="Base project budget excluding contingency")
        
        with col2:
            contingency_percent = st.number_input("Contingency (%)", 
                min_value=0.0, 
                max_value=100.0,
                value=float(project_data.get("contingency_percent", 10.0)),
                step=0.5,
                help="Contingency percentage")
            
            contingency_amount = base_budget * (contingency_percent / 100)
        
        with col3:
            total_budget = base_budget + contingency_amount
            st.metric("Total Budget", f"${total_budget:,.2f}")
        
        # Second row - Contract Type and Payment Terms
        col1, col2 = st.columns(2)
        
        contract_types = ["Fixed Price", "Cost Plus", "Guaranteed Maximum Price", "Time & Materials", "Unit Price", "Other"]
        with col1:
            contract_type = st.selectbox("Contract Type", 
                options=contract_types,
                index=contract_types.index(project_data.get("contract_type", "Fixed Price")),
                help="Type of construction contract")
        
        payment_terms_options = ["Monthly", "Milestone-based", "Progress-based", "Custom"]
        with col2:
            payment_terms = st.selectbox("Payment Terms", 
                options=payment_terms_options,
                index=payment_terms_options.index(project_data.get("payment_terms", "Monthly")),
                help="Project payment terms")
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
        
        # Team and Management section
        st.markdown("### Team Information")
        
        # First row - Project Manager and Superintendent
        col1, col2 = st.columns(2)
        
        with col1:
            project_manager = st.text_input("Project Manager", 
                value=project_data.get("project_manager", ""),
                help="Name of the project manager")
        
        with col2:
            superintendent = st.text_input("Superintendent", 
                value=project_data.get("superintendent", ""),
                help="Name of the field superintendent")
        
        # Second row - Architect and Engineer
        col1, col2 = st.columns(2)
        
        with col1:
            architect = st.text_input("Architect", 
                value=project_data.get("architect", ""),
                help="Name of the architecture firm")
        
        with col2:
            engineer = st.text_input("Engineer", 
                value=project_data.get("engineer", ""),
                help="Name of the engineering firm")
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
        
        # Additional Information
        st.markdown("### Additional Information")
        
        # Description
        description = st.text_area("Project Description", 
            value=project_data.get("description", ""),
            height=100,
            help="Detailed description of the project scope")
        
        # Status and priority
        col1, col2 = st.columns(2)
        
        status_options = ["Planning", "Preconstruction", "Active", "On Hold", "Closed"]
        with col1:
            status = st.selectbox("Project Status", 
                options=status_options,
                index=status_options.index(project_data.get("status", "Planning")),
                help="Current status of the project")
        
        priority_options = ["Low", "Medium", "High", "Critical"]
        with col2:
            priority = st.selectbox("Priority", 
                options=priority_options,
                index=priority_options.index(project_data.get("priority", "Medium")),
                help="Project priority level")
        
        # Submit button
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        
        with col1:
            submitted = st.form_submit_button("Save Changes", use_container_width=True)
        
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True, type="secondary")
        
        if submitted:
            if not project_name:
                st.error("Project Name is a required field.")
                return None
            
            # Update project data
            updated_data = project_data.copy()
            updated_data.update({
                "name": project_name,
                "client": client_name,
                "type": project_type,
                "address": address,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "duration": duration,
                "base_budget": base_budget,
                "contingency_percent": contingency_percent,
                "contingency_amount": contingency_amount,
                "total_budget": total_budget,
                "contract_type": contract_type,
                "payment_terms": payment_terms,
                "project_manager": project_manager,
                "superintendent": superintendent,
                "architect": architect,
                "engineer": engineer,
                "description": description,
                "status": status,
                "priority": priority,
                "updated_at": datetime.now(),
                "updated_by": st.session_state.get("user_id", "admin")
            })
            
            return updated_data
        
        if cancel:
            return False
    
    # Close the form container
    st.markdown('</div>', unsafe_allow_html=True)
    return None