"""
Engineering components for Streamlit interface.

This module provides UI components for engineering processes including
RFIs, submittals, and other engineering document management.
"""

import streamlit as st
from datetime import date, datetime
from typing import Optional, List
from core.repositories.engineering_repository import SubmittalRepository, RfiRepository
from core.repositories.project_repository import ProjectRepository
from core.models.engineering import Submittal, SubmittalStatus, Rfi, RfiStatus
from components.auth import check_authentication

def submittals_list_component(project_id: Optional[int] = None):
    """
    Display a list of submittals with filtering and selection options.
    
    Args:
        project_id: Optional project ID to filter submittals
    """
    if not check_authentication():
        st.warning("Please log in to view submittals")
        return
    
    st.subheader("Submittals")
    
    # Initialize repositories
    submittal_repo = SubmittalRepository()
    project_repo = ProjectRepository()
    
    # Get current user
    user = st.session_state.user
    
    # Project selection if not provided
    if not project_id:
        # Get projects based on user role
        if user.has_role("admin") or user.has_role("project_manager"):
            projects = project_repo.get_active_projects()
        else:
            projects = project_repo.get_user_projects(user.id)
        
        if not projects:
            st.info("No projects available. Please create a project or ask to be assigned to a project.")
            return
            
        # Select project
        project_options = {f"{p.code} - {p.name}": p.id for p in projects}
        selected_project = st.selectbox(
            "Select Project:",
            options=list(project_options.keys())
        )
        
        project_id = project_options[selected_project]
    
    # Status filter
    status_options = ["All"] + [s.value.title() for s in SubmittalStatus]
    selected_status = st.selectbox(
        "Filter by Status:",
        options=status_options,
        index=0
    )
    
    # Get submittals based on filters
    if selected_status == "All":
        submittals = submittal_repo.get_project_submittals(project_id)
    else:
        status_enum = SubmittalStatus(selected_status.lower())
        submittals = submittal_repo.get_project_submittals(project_id, status_enum)
    
    # Display submittals in a table
    if submittals:
        submittal_data = []
        for submittal in submittals:
            status_color = get_submittal_status_color(submittal.status)
            submittal_data.append({
                "ID": submittal.id,
                "Number": submittal.submittal_number,
                "Title": submittal.title,
                "Spec Section": submittal.spec_section or "",
                "Status": f":{status_color}[{submittal.status.value.title()}]",
                "Submission Date": submittal.submission_date or "",
                "Due Date": submittal.due_date or "",
                "Days": get_days_indicator(submittal)
            })
        
        st.dataframe(
            submittal_data,
            column_config={
                "ID": st.column_config.NumberColumn(
                    "ID",
                    help="Submittal ID",
                    width="small"
                ),
                "Number": st.column_config.TextColumn(
                    "Number",
                    help="Submittal Number",
                    width="small"
                ),
                "Title": st.column_config.TextColumn(
                    "Title",
                    help="Submittal Title",
                    width="medium"
                ),
                "Spec Section": st.column_config.TextColumn(
                    "Spec Section",
                    help="Specification Section",
                    width="small"
                ),
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Current status",
                    width="small"
                ),
                "Submission Date": st.column_config.DateColumn(
                    "Submitted",
                    help="Submission date",
                    width="small",
                    format="MMM DD, YYYY"
                ),
                "Due Date": st.column_config.DateColumn(
                    "Due Date",
                    help="Review due date",
                    width="small",
                    format="MMM DD, YYYY"
                ),
                "Days": st.column_config.TextColumn(
                    "Days",
                    help="Days remaining or overdue",
                    width="small"
                ),
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Submittal selection
        col1, col2 = st.columns([2, 1])
        with col1:
            submittal_numbers = [s.submittal_number for s in submittals]
            selected_number = st.selectbox("Select a submittal to view details:", submittal_numbers)
        
        with col2:
            st.write("")
            st.write("")
            if st.button("View Submittal Details", key="view_submittal"):
                selected_submittal = next((s for s in submittals if s.submittal_number == selected_number), None)
                if selected_submittal:
                    st.session_state.selected_submittal_id = selected_submittal.id
                    st.rerun()
    else:
        st.info("No submittals found matching the selected filters.")
    
    # Create new submittal button
    if st.button("Create New Submittal"):
        st.session_state.create_submittal_project_id = project_id
        st.rerun()

def submittal_details_component(submittal_id: Optional[int] = None):
    """
    Display submittal details including attachments and status history.
    
    Args:
        submittal_id: Optional submittal ID to display
    """
    if not check_authentication():
        st.warning("Please log in to view submittal details")
        return
    
    # Get submittal ID from session state if not provided
    if not submittal_id and "selected_submittal_id" in st.session_state:
        submittal_id = st.session_state.selected_submittal_id
    
    if not submittal_id:
        st.warning("No submittal selected")
        return
    
    # Initialize repository and get submittal with attachments
    submittal_repo = SubmittalRepository()
    project_repo = ProjectRepository()
    submittal = submittal_repo.get_with_attachments(submittal_id)
    
    if not submittal:
        st.error(f"Submittal with ID {submittal_id} not found")
        return
    
    # Get project information
    project = project_repo.get_by_id(submittal.project_id)
    
    # Display submittal header
    st.title(f"Submittal {submittal.submittal_number}")
    st.caption(f"Project: {project.code} - {project.name}")
    
    # Submittal status with colored badge
    status_color = get_submittal_status_color(submittal.status)
    st.markdown(f"**Status:** :{status_color}[{submittal.status.value.title()}]")
    
    # Submittal details in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Submittal Information")
        st.write(f"**Title:** {submittal.title}")
        st.write(f"**Specification Section:** {submittal.spec_section or 'N/A'}")
        st.write(f"**Submission Date:** {format_date(submittal.submission_date)}")
        st.write(f"**Due Date:** {format_date(submittal.due_date)}")
        st.write(f"**Review Date:** {format_date(submittal.review_date)}")
        
        if submittal.is_critical:
            st.markdown("**Critical Submittal:** :red[Yes]")
        
    with col2:
        st.subheader("Personnel")
        if submittal.created_by:
            st.write(f"**Created By:** {submittal.created_by.full_name}")
        else:
            st.write("**Created By:** Unknown")
            
        if submittal.assignee:
            st.write(f"**Assigned To:** {submittal.assignee.full_name}")
        else:
            st.write("**Assigned To:** Unassigned")
        
        # Calculate and display days remaining or overdue
        if submittal.due_date:
            if submittal.status in [SubmittalStatus.APPROVED, SubmittalStatus.APPROVED_AS_NOTED,
                                   SubmittalStatus.REJECTED, SubmittalStatus.CLOSED]:
                st.write("**Review Complete**")
            else:
                days = submittal.days_remaining
                if days is not None:
                    if days < 0:
                        st.markdown(f"**Overdue:** :red[{abs(days)} days]")
                    elif days == 0:
                        st.markdown("**Due:** :orange[Today]")
                    else:
                        st.markdown(f"**Due in:** :blue[{days} days]")
    
    # Notes section
    st.subheader("Notes")
    st.write(submittal.notes or "No notes provided")
    
    # Attachments section
    st.subheader("Attachments")
    if submittal.attachments:
        for attachment in submittal.attachments:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{attachment.filename}**")
                if attachment.description:
                    st.write(attachment.description)
            with col2:
                st.write(f"Type: {attachment.file_type or 'Unknown'}")
            with col3:
                st.write(f"Size: {format_file_size(attachment.file_size)}")
                st.button(f"Download", key=f"download_{attachment.id}")
    else:
        st.info("No attachments available")
    
    # Status update section (only for assigned reviewers, project managers, or admins)
    user = st.session_state.user
    can_update = (user.id == submittal.assignee_id or 
                 user.has_role("admin") or 
                 user.has_role("project_manager"))
    
    if can_update and submittal.status not in [SubmittalStatus.CLOSED]:
        st.subheader("Update Status")
        
        with st.form("update_submittal_status"):
            # Determine available status options based on current status
            if submittal.status == SubmittalStatus.DRAFT:
                status_options = [
                    SubmittalStatus.SUBMITTED.value.title(),
                    SubmittalStatus.CLOSED.value.title()
                ]
            elif submittal.status == SubmittalStatus.SUBMITTED:
                status_options = [
                    SubmittalStatus.UNDER_REVIEW.value.title(),
                    SubmittalStatus.CLOSED.value.title()
                ]
            elif submittal.status == SubmittalStatus.UNDER_REVIEW:
                status_options = [
                    SubmittalStatus.APPROVED.value.title(),
                    SubmittalStatus.APPROVED_AS_NOTED.value.title(),
                    SubmittalStatus.REVISE_AND_RESUBMIT.value.title(),
                    SubmittalStatus.REJECTED.value.title(),
                    SubmittalStatus.CLOSED.value.title()
                ]
            else:
                status_options = [s.value.title() for s in SubmittalStatus 
                                 if s != submittal.status]
            
            new_status = st.selectbox(
                "New Status:",
                options=status_options
            )
            
            notes = st.text_area("Status Update Notes:", height=100)
            
            submit = st.form_submit_button("Update Status")
            
            if submit:
                status_enum = SubmittalStatus(new_status.lower())
                if submittal_repo.update_status(submittal.id, status_enum, notes):
                    st.success(f"Status updated to {new_status}")
                    st.rerun()
                else:
                    st.error("Failed to update status")

def rfi_list_component(project_id: Optional[int] = None):
    """
    Display a list of RFIs with filtering and selection options.
    
    Args:
        project_id: Optional project ID to filter RFIs
    """
    if not check_authentication():
        st.warning("Please log in to view RFIs")
        return
    
    st.subheader("Requests for Information (RFIs)")
    
    # Initialize repositories
    rfi_repo = RfiRepository()
    project_repo = ProjectRepository()
    
    # Get current user
    user = st.session_state.user
    
    # Project selection if not provided
    if not project_id:
        # Get projects based on user role
        if user.has_role("admin") or user.has_role("project_manager"):
            projects = project_repo.get_active_projects()
        else:
            projects = project_repo.get_user_projects(user.id)
        
        if not projects:
            st.info("No projects available. Please create a project or ask to be assigned to a project.")
            return
            
        # Select project
        project_options = {f"{p.code} - {p.name}": p.id for p in projects}
        selected_project = st.selectbox(
            "Select Project:",
            options=list(project_options.keys())
        )
        
        project_id = project_options[selected_project]
    
    # Status filter
    status_options = ["All"] + [s.value.title() for s in RfiStatus]
    selected_status = st.selectbox(
        "Filter by Status:",
        options=status_options,
        index=0
    )
    
    # Get RFIs based on filters
    if selected_status == "All":
        rfis = rfi_repo.get_project_rfis(project_id)
    else:
        status_enum = RfiStatus(selected_status.lower())
        rfis = rfi_repo.get_project_rfis(project_id, status_enum)
    
    # Display RFIs in a table
    if rfis:
        rfi_data = []
        for rfi in rfis:
            status_color = get_rfi_status_color(rfi.status)
            rfi_data.append({
                "ID": rfi.id,
                "Number": rfi.rfi_number,
                "Subject": rfi.subject,
                "Status": f":{status_color}[{rfi.status.value.title()}]",
                "Submission Date": rfi.submission_date or "",
                "Due Date": rfi.due_date or "",
                "Days Open": rfi.days_open if rfi.submission_date else ""
            })
        
        st.dataframe(
            rfi_data,
            column_config={
                "ID": st.column_config.NumberColumn(
                    "ID",
                    help="RFI ID",
                    width="small"
                ),
                "Number": st.column_config.TextColumn(
                    "Number",
                    help="RFI Number",
                    width="small"
                ),
                "Subject": st.column_config.TextColumn(
                    "Subject",
                    help="RFI Subject",
                    width="medium"
                ),
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Current status",
                    width="small"
                ),
                "Submission Date": st.column_config.DateColumn(
                    "Submitted",
                    help="Submission date",
                    width="small",
                    format="MMM DD, YYYY"
                ),
                "Due Date": st.column_config.DateColumn(
                    "Due Date",
                    help="Response due date",
                    width="small",
                    format="MMM DD, YYYY"
                ),
                "Days Open": st.column_config.NumberColumn(
                    "Days Open",
                    help="Days the RFI has been open",
                    width="small"
                ),
            },
            use_container_width=True,
            hide_index=True
        )
        
        # RFI selection
        col1, col2 = st.columns([2, 1])
        with col1:
            rfi_numbers = [r.rfi_number for r in rfis]
            selected_number = st.selectbox("Select an RFI to view details:", rfi_numbers)
        
        with col2:
            st.write("")
            st.write("")
            if st.button("View RFI Details", key="view_rfi"):
                selected_rfi = next((r for r in rfis if r.rfi_number == selected_number), None)
                if selected_rfi:
                    st.session_state.selected_rfi_id = selected_rfi.id
                    st.rerun()
    else:
        st.info("No RFIs found matching the selected filters.")
    
    # Create new RFI button
    if st.button("Create New RFI"):
        st.session_state.create_rfi_project_id = project_id
        st.rerun()

def rfi_details_component(rfi_id: Optional[int] = None):
    """
    Display RFI details including attachments and response.
    
    Args:
        rfi_id: Optional RFI ID to display
    """
    if not check_authentication():
        st.warning("Please log in to view RFI details")
        return
    
    # Get RFI ID from session state if not provided
    if not rfi_id and "selected_rfi_id" in st.session_state:
        rfi_id = st.session_state.selected_rfi_id
    
    if not rfi_id:
        st.warning("No RFI selected")
        return
    
    # Initialize repository and get RFI with attachments
    rfi_repo = RfiRepository()
    project_repo = ProjectRepository()
    rfi = rfi_repo.get_with_attachments(rfi_id)
    
    if not rfi:
        st.error(f"RFI with ID {rfi_id} not found")
        return
    
    # Get project information
    project = project_repo.get_by_id(rfi.project_id)
    
    # Display RFI header
    st.title(f"RFI {rfi.rfi_number}")
    st.caption(f"Project: {project.code} - {project.name}")
    
    # RFI status with colored badge
    status_color = get_rfi_status_color(rfi.status)
    st.markdown(f"**Status:** :{status_color}[{rfi.status.value.title()}]")
    
    # RFI details in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("RFI Information")
        st.write(f"**Subject:** {rfi.subject}")
        st.write(f"**Submission Date:** {format_date(rfi.submission_date)}")
        st.write(f"**Due Date:** {format_date(rfi.due_date)}")
        st.write(f"**Response Date:** {format_date(rfi.response_date)}")
        
        if rfi.is_critical:
            st.markdown("**Critical RFI:** :red[Yes]")
        
    with col2:
        st.subheader("Personnel")
        if rfi.created_by:
            st.write(f"**Created By:** {rfi.created_by.full_name}")
        else:
            st.write("**Created By:** Unknown")
            
        if rfi.assignee:
            st.write(f"**Assigned To:** {rfi.assignee.full_name}")
        else:
            st.write("**Assigned To:** Unassigned")
        
        # Calculate and display days open or overdue
        if rfi.submission_date:
            if rfi.status in [RfiStatus.ANSWERED, RfiStatus.CLOSED]:
                if rfi.response_date:
                    days = (rfi.response_date - rfi.submission_date).days
                    st.write(f"**Days to Answer:** {days} days")
            else:
                days_open = rfi.days_open
                st.write(f"**Days Open:** {days_open} days")
                
                # Check if overdue
                if rfi.due_date and rfi.due_date < date.today():
                    overdue_days = (date.today() - rfi.due_date).days
                    st.markdown(f"**Overdue:** :red[{overdue_days} days]")
    
    # Question section
    st.subheader("Question")
    st.write(rfi.question)
    
    # Answer section
    st.subheader("Answer")
    if rfi.answer:
        st.write(rfi.answer)
    else:
        st.info("No answer provided yet")
    
    # Attachments section
    st.subheader("Attachments")
    if rfi.attachments:
        for attachment in rfi.attachments:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{attachment.filename}**")
                if attachment.description:
                    st.write(attachment.description)
            with col2:
                st.write(f"Type: {attachment.file_type or 'Unknown'}")
            with col3:
                st.write(f"Size: {format_file_size(attachment.file_size)}")
                st.button(f"Download", key=f"download_{attachment.id}")
    else:
        st.info("No attachments available")
    
    # Answer response section (only for assigned responders, project managers, or admins)
    user = st.session_state.user
    can_answer = (user.id == rfi.assignee_id or 
                 user.has_role("admin") or 
                 user.has_role("project_manager"))
    
    if can_answer and rfi.status not in [RfiStatus.CLOSED]:
        st.subheader("Provide Response")
        
        with st.form("update_rfi_response"):
            # Determine available status options based on current status
            if rfi.status == RfiStatus.DRAFT:
                status_options = [
                    RfiStatus.SUBMITTED.value.title(),
                    RfiStatus.CLOSED.value.title()
                ]
            elif rfi.status in [RfiStatus.SUBMITTED, RfiStatus.UNDER_REVIEW]:
                status_options = [
                    RfiStatus.ANSWERED.value.title(),
                    RfiStatus.NEEDS_CLARIFICATION.value.title(),
                    RfiStatus.CLOSED.value.title()
                ]
            else:
                status_options = [s.value.title() for s in RfiStatus 
                                 if s != rfi.status]
            
            new_status = st.selectbox(
                "New Status:",
                options=status_options
            )
            
            answer = st.text_area("Response:", height=150, value=rfi.answer or "")
            
            submit = st.form_submit_button("Submit Response")
            
            if submit:
                status_enum = RfiStatus(new_status.lower())
                if rfi_repo.update_status(rfi.id, status_enum, answer):
                    st.success(f"Response submitted and status updated to {new_status}")
                    st.rerun()
                else:
                    st.error("Failed to submit response")

def get_submittal_status_color(status: SubmittalStatus) -> str:
    """Get appropriate color for submittal status badge"""
    status_colors = {
        SubmittalStatus.DRAFT: "gray",
        SubmittalStatus.SUBMITTED: "blue",
        SubmittalStatus.UNDER_REVIEW: "orange",
        SubmittalStatus.APPROVED: "green", 
        SubmittalStatus.APPROVED_AS_NOTED: "violet",
        SubmittalStatus.REVISE_AND_RESUBMIT: "yellow",
        SubmittalStatus.REJECTED: "red",
        SubmittalStatus.CLOSED: "gray"
    }
    return status_colors.get(status, "gray")

def get_rfi_status_color(status: RfiStatus) -> str:
    """Get appropriate color for RFI status badge"""
    status_colors = {
        RfiStatus.DRAFT: "gray",
        RfiStatus.SUBMITTED: "blue",
        RfiStatus.UNDER_REVIEW: "orange",
        RfiStatus.ANSWERED: "green", 
        RfiStatus.NEEDS_CLARIFICATION: "yellow",
        RfiStatus.CLOSED: "gray"
    }
    return status_colors.get(status, "gray")

def get_days_indicator(submittal: Submittal) -> str:
    """Get days remaining/overdue indicator for a submittal"""
    if submittal.status in [SubmittalStatus.APPROVED, SubmittalStatus.APPROVED_AS_NOTED,
                           SubmittalStatus.REJECTED, SubmittalStatus.CLOSED]:
        return ""
        
    if not submittal.due_date:
        return ""
        
    days = submittal.days_remaining
    if days is not None:
        if days < 0:
            return f":red[{abs(days)} days overdue]"
        elif days == 0:
            return ":orange[Due today]"
        else:
            return f":blue[{days} days remaining]"
    return ""

def format_date(date_value) -> str:
    """Format a date value or return 'N/A' if None"""
    if date_value:
        if isinstance(date_value, (date, datetime)):
            return date_value.strftime("%b %d, %Y")
        return str(date_value)
    return "N/A"

def format_file_size(size_in_bytes) -> str:
    """Format file size in human-readable form"""
    if size_in_bytes is None:
        return "Unknown"
        
    # Convert to KB, MB as appropriate
    if size_in_bytes < 1024:
        return f"{size_in_bytes} bytes"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.1f} KB"
    else:
        return f"{size_in_bytes / (1024 * 1024):.1f} MB"