"""
Project management components for Streamlit interface.

This module provides UI components for project management including
project listing, creation, editing, and details display.
"""

import streamlit as st
from datetime import date, datetime
from typing import Optional, List
from core.repositories.project_repository import ProjectRepository
from core.models.project import Project, ProjectStatus, ProjectMilestone
from components.auth import check_authentication

def project_list_component():
    """
    Display a list of projects with filtering and selection options.
    """
    if not check_authentication():
        st.warning("Please log in to view projects")
        return
    
    st.subheader("Projects")
    
    # Initialize repository
    project_repo = ProjectRepository()
    
    # Get projects based on user role
    user = st.session_state.user
    if user.has_role("admin") or user.has_role("project_manager"):
        projects = project_repo.get_active_projects()
        st.write(f"Showing all {len(projects)} active projects")
    else:
        projects = project_repo.get_user_projects(user.id)
        st.write(f"Showing {len(projects)} projects assigned to you")
    
    # Display projects in a table
    if projects:
        project_data = []
        for project in projects:
            status_color = get_status_color(project.status)
            project_data.append({
                "ID": project.id,
                "Code": project.code,
                "Name": project.name,
                "Status": f":{status_color}[{project.status.value.title()}]",
                "Location": project.location,
                "Start Date": project.start_date,
                "End Date": project.end_date
            })
        
        st.dataframe(
            project_data,
            column_config={
                "ID": st.column_config.NumberColumn(
                    "ID",
                    help="Project ID",
                    width="small"
                ),
                "Code": st.column_config.TextColumn(
                    "Code",
                    help="Project Code",
                    width="small"
                ),
                "Name": st.column_config.TextColumn(
                    "Name",
                    help="Project Name",
                    width="medium"
                ),
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Current project status",
                    width="small"
                ),
                "Location": st.column_config.TextColumn(
                    "Location",
                    help="Project Location",
                    width="medium"
                ),
                "Start Date": st.column_config.DateColumn(
                    "Start Date",
                    help="Project start date",
                    width="small",
                    format="MMM DD, YYYY"
                ),
                "End Date": st.column_config.DateColumn(
                    "End Date",
                    help="Project end date",
                    width="small",
                    format="MMM DD, YYYY"
                )
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Project selection
        col1, col2 = st.columns([2, 1])
        with col1:
            project_codes = [p.code for p in projects]
            selected_code = st.selectbox("Select a project to view details:", project_codes)
        
        with col2:
            st.write("")
            st.write("")
            if st.button("View Project Details", key="view_project"):
                if "selected_project_code" in st.session_state:
                    st.session_state.selected_project_code = selected_code
                    st.rerun()
    else:
        st.info("No projects found. Please create a new project or ask to be assigned to a project.")

def project_details_component(project_code: Optional[str] = None):
    """
    Display project details including milestones and team members.
    
    Args:
        project_code: Optional project code to display
    """
    if not check_authentication():
        st.warning("Please log in to view project details")
        return
    
    # Get project code from session state if not provided
    if not project_code and "selected_project_code" in st.session_state:
        project_code = st.session_state.selected_project_code
    
    if not project_code:
        st.warning("No project selected")
        return
    
    # Initialize repository and get project
    project_repo = ProjectRepository()
    project = project_repo.get_by_code(project_code)
    
    if not project:
        st.error(f"Project with code {project_code} not found")
        return
    
    # Display project header
    st.title(project.name)
    st.caption(f"Project Code: {project.code}")
    
    # Project status with colored badge
    status_color = get_status_color(project.status)
    st.markdown(f"**Status:** :{status_color}[{project.status.value.title()}]")
    
    # Project details in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Project Information")
        st.write(f"**Description:** {project.description or 'N/A'}")
        st.write(f"**Location:** {project.location}")
        st.write(f"**Start Date:** {format_date(project.start_date)}")
        st.write(f"**End Date:** {format_date(project.end_date)}")
        if project.duration_days:
            st.write(f"**Duration:** {project.duration_days} days")
        
    with col2:
        st.subheader("Project Stakeholders")
        st.write(f"**Owner:** {project.owner_name or 'N/A'}")
        st.write(f"**Architect:** {project.architect_name or 'N/A'}")
        
        st.subheader("Team Members")
        if project.team_members:
            for member in project.team_members:
                st.write(f"- {member.full_name} ({', '.join([r.name for r in member.roles])})")
        else:
            st.write("No team members assigned")
    
    # Project milestones
    st.subheader("Milestones")
    milestones = project_repo.get_project_milestones(project.id)
    
    if milestones:
        milestone_data = []
        for milestone in milestones:
            status = "Completed" if milestone.is_completed else "Pending"
            color = "green" if milestone.is_completed else "orange" if milestone.is_delayed else "blue"
            milestone_data.append({
                "Name": milestone.name,
                "Description": milestone.description or "",
                "Target Date": milestone.target_date,
                "Actual Date": milestone.actual_date or "-",
                "Status": f":{color}[{status}]"
            })
        
        st.dataframe(
            milestone_data,
            column_config={
                "Name": st.column_config.TextColumn("Name", width="medium"),
                "Description": st.column_config.TextColumn("Description", width="large"),
                "Target Date": st.column_config.DateColumn("Target Date", format="MMM DD, YYYY"),
                "Actual Date": st.column_config.TextColumn("Actual Date", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small")
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No milestones defined for this project")
    
    # Project actions
    st.subheader("Project Actions")
    
    # Only allow status changes for admins and project managers
    user = st.session_state.user
    if user.has_role("admin") or user.has_role("project_manager"):
        col1, col2 = st.columns([1, 3])
        with col1:
            status_options = [status.value.title() for status in ProjectStatus]
            current_index = status_options.index(project.status.value.title())
            selected_status = st.selectbox(
                "Change Project Status:",
                options=status_options,
                index=current_index
            )
        
        with col2:
            st.write("")
            st.write("")
            if st.button("Update Status"):
                new_status = ProjectStatus(selected_status.lower())
                if project_repo.update_project_status(project.id, new_status):
                    st.success(f"Project status updated to {selected_status}")
                    st.rerun()
                else:
                    st.error("Failed to update project status")

def project_create_component():
    """
    Display form for creating a new project.
    """
    if not check_authentication():
        st.warning("Please log in to create a project")
        return
    
    # Check if user has permission
    user = st.session_state.user
    if not user.has_role("admin") and not user.has_role("project_manager"):
        st.error("You don't have permission to create projects")
        return
    
    st.subheader("Create New Project")
    
    with st.form("create_project_form"):
        # Basic project information
        name = st.text_input("Project Name *")
        code = st.text_input("Project Code *", help="Unique identifier for the project")
        description = st.text_area("Description")
        
        # Dates
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date.today())
        with col2:
            end_date = st.date_input("End Date", value=date.today())
        
        # Location
        st.subheader("Location")
        col1, col2 = st.columns(2)
        with col1:
            address = st.text_input("Address")
            city = st.text_input("City")
        with col2:
            state = st.text_input("State/Province")
            zip_code = st.text_input("Zip/Postal Code")
        country = st.text_input("Country")
        
        # Project details
        st.subheader("Project Details")
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("Budget", min_value=0.0, step=10000.0)
        with col2:
            status = st.selectbox(
                "Initial Status",
                options=[status.value.title() for status in ProjectStatus],
                index=0  # Default to PLANNING
            )
        
        # Stakeholders
        st.subheader("Stakeholders")
        col1, col2 = st.columns(2)
        with col1:
            owner_name = st.text_input("Owner/Client Name")
        with col2:
            architect_name = st.text_input("Architect")
        
        # Submit button
        submit = st.form_submit_button("Create Project")
        
        if submit:
            if not name or not code:
                st.error("Project name and code are required")
                return
            
            # Check if end date is after start date
            if end_date < start_date:
                st.error("End date must be after start date")
                return
            
            # Create project
            project_repo = ProjectRepository()
            
            # Convert status string to enum
            status_enum = ProjectStatus(status.lower())
            
            # Prepare project data
            project_data = {
                "name": name,
                "code": code,
                "description": description,
                "status": status_enum,
                "start_date": start_date,
                "end_date": end_date,
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "country": country,
                "budget": budget if budget > 0 else None,
                "owner_name": owner_name,
                "architect_name": architect_name
            }
            
            # Create project
            project = project_repo.create(project_data)
            
            if project:
                st.success(f"Project '{name}' created successfully!")
                
                # Add creator as team member
                project_repo.add_team_member(project.id, user.id)
                
                # Store created project in session state
                st.session_state.selected_project_code = code
                st.rerun()
            else:
                st.error("Failed to create project. The project code may already be in use.")

def format_date(date_value) -> str:
    """Format a date value or return 'N/A' if None"""
    if date_value:
        if isinstance(date_value, (date, datetime)):
            return date_value.strftime("%b %d, %Y")
        return str(date_value)
    return "N/A"

def get_status_color(status: ProjectStatus) -> str:
    """Get appropriate color for status badge"""
    status_colors = {
        ProjectStatus.PLANNING: "blue",
        ProjectStatus.PRECONSTRUCTION: "violet",
        ProjectStatus.CONSTRUCTION: "orange", 
        ProjectStatus.CLOSEOUT: "green",
        ProjectStatus.COMPLETE: "green",
        ProjectStatus.ON_HOLD: "red"
    }
    return status_colors.get(status, "gray")