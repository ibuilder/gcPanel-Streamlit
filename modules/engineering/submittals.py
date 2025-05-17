import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import get_db_connection
from utils.auth import check_permission

# Module metadata
MODULE_DISPLAY_NAME = "Submittals"
MODULE_ICON = "upload"

def render_list():
    """Render the list view of submittals"""
    st.title("Submittals")
    
    # Check permission
    if not check_permission('read'):
        st.error("You don't have permission to view submittals")
        return
    
    # Add filter controls
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Pending", "Approved", "Rejected", "Revise & Resubmit"])
    with col2:
        discipline_filter = st.selectbox("Discipline", ["All", "Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil"])
    with col3:
        search = st.text_input("Search", placeholder="Search by keyword")
    
    # Create a button to add new submittal
    if check_permission('create'):
        if st.button("Add New Submittal"):
            st.session_state.current_view = "form"
            st.rerun()

    # Display sample data (in a real app, this would come from the database)
    data = {
        'ID': ['SUB-001', 'SUB-002', 'SUB-003', 'SUB-004', 'SUB-005'],
        'Title': [
            'Concrete Mix Design', 
            'Structural Steel Shop Drawings', 
            'HVAC Equipment Specifications', 
            'Electrical Panel Schedules',
            'Window Details'
        ],
        'Discipline': ['Structural', 'Structural', 'Mechanical', 'Electrical', 'Architectural'],
        'Submitted By': ['John Contractor', 'Steel Fabricator Inc.', 'Mechanical Sub', 'Electric Co.', 'Window Supplier'],
        'Date Submitted': ['2025-05-01', '2025-05-03', '2025-05-07', '2025-05-10', '2025-05-12'],
        'Status': ['Approved', 'Revise & Resubmit', 'Pending', 'Approved', 'Rejected'],
        'Review Date': ['2025-05-05', '2025-05-08', '', '2025-05-15', '2025-05-16']
    }
    
    df = pd.DataFrame(data)
    
    # Apply filters
    if status_filter != "All":
        df = df[df['Status'] == status_filter]
    if discipline_filter != "All":
        df = df[df['Discipline'] == discipline_filter]
    if search:
        df = df[df.astype(str).apply(lambda row: row.str.contains(search, case=False)).any(axis=1)]
    
    # Display data
    if df.empty:
        st.info("No submittals found matching your criteria")
    else:
        # Add styling based on status
        def highlight_status(val):
            if val == 'Approved':
                return 'background-color: #d4edda; color: #155724'
            elif val == 'Rejected':
                return 'background-color: #f8d7da; color: #721c24'
            elif val == 'Revise & Resubmit':
                return 'background-color: #fff3cd; color: #856404'
            else:
                return 'background-color: #e2e3e5; color: #383d41'
        
        # Apply styling
        styled_df = df.style.applymap(highlight_status, subset=['Status'])
        
        # Display table with styling
        st.dataframe(styled_df, hide_index=True)
        
        # Add action buttons for each row
        st.write("### Actions")
        submit_id = st.selectbox("Select Submittal", df['ID'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("View Details"):
                st.session_state.current_view = "view"
                st.session_state.editing_id = submit_id
                st.rerun()
        with col2:
            if check_permission('update'):
                if st.button("Edit Submittal"):
                    st.session_state.current_view = "form"
                    st.session_state.editing_id = submit_id
                    st.rerun()
        with col3:
            if check_permission('delete'):
                if st.button("Delete Submittal"):
                    st.error(f"Are you sure you want to delete {submit_id}? This action cannot be undone.")
                    if st.button("Confirm Delete"):
                        st.success(f"Submittal {submit_id} deleted successfully")
                        st.rerun()

def render_view():
    """Render the detail view of a submittal"""
    submit_id = st.session_state.get('editing_id', 'SUB-001')
    
    # Check permission
    if not check_permission('read'):
        st.error("You don't have permission to view submittal details")
        return
    
    # Sample submittal data
    if submit_id == 'SUB-001':
        title = "Concrete Mix Design"
        discipline = "Structural"
        submitted_by = "John Contractor"
        date_submitted = "2025-05-01"
        status = "Approved"
        review_date = "2025-05-05"
        reviewer = "Dr. Engineer"
        comments = "Mix design meets project specifications. Approved as noted with minor modifications to water-cement ratio."
        description = """
        Submittal for concrete mix design to be used for foundation elements.
        - 4000 PSI Concrete
        - 3/4" Maximum aggregate size
        - 0.45 Water-cement ratio
        - Air entrainment as per specifications
        - Fly ash content as allowed
        """
    else:
        # Generic data for other submittal IDs
        title = f"Submittal {submit_id}"
        discipline = "General"
        submitted_by = "Contractor"
        date_submitted = "2025-05-01"
        status = "Pending"
        review_date = ""
        reviewer = ""
        comments = ""
        description = "Generic submittal description"
    
    # Render header
    st.title(f"Submittal Details: {submit_id}")
    
    # Back button
    if st.button("Back to List"):
        st.session_state.current_view = "list"
        if 'editing_id' in st.session_state:
            del st.session_state.editing_id
        st.rerun()
    
    # Display submittal details
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Submittal Information")
        st.write(f"**Title:** {title}")
        st.write(f"**Discipline:** {discipline}")
        st.write(f"**Submitted By:** {submitted_by}")
        st.write(f"**Date Submitted:** {date_submitted}")
        
        # Action buttons
        if check_permission('update'):
            if st.button("Edit"):
                st.session_state.current_view = "form"
                st.rerun()
    
    with col2:
        st.subheader("Review Information")
        st.write(f"**Status:** {status}")
        st.write(f"**Review Date:** {review_date}")
        st.write(f"**Reviewer:** {reviewer}")
    
    # Description and comments
    st.subheader("Description")
    st.write(description)
    
    st.subheader("Review Comments")
    st.write(comments if comments else "No comments provided yet.")
    
    # Attachments section
    st.subheader("Attachments")
    
    # Sample attachments
    attachment_data = {
        'Filename': ['ConcreteSpec.pdf', 'TestResults.xlsx', 'Photos.zip'],
        'Type': ['PDF', 'Excel', 'Archive'],
        'Size': ['2.4 MB', '1.2 MB', '5.8 MB'],
        'Uploaded': ['2025-05-01', '2025-05-01', '2025-05-01']
    }
    
    attachments_df = pd.DataFrame(attachment_data)
    st.dataframe(attachments_df, hide_index=True)
    
    # Button to download all attachments
    st.download_button(
        label="Download All Attachments",
        data=b"Sample download content",
        file_name=f"Submittal_{submit_id}_Attachments.zip",
        mime="application/zip"
    )
    
    # Review section for admins, managers and contributors
    if check_permission('update'):
        st.subheader("Review Submittal")
        
        review_status = st.selectbox("Review Status", ["Pending", "Approved", "Rejected", "Revise & Resubmit"])
        review_comments = st.text_area("Review Comments", height=100)
        
        if st.button("Submit Review"):
            st.success(f"Submittal {submit_id} has been marked as '{review_status}'")
            # In a real app, this would update the database
            st.rerun()

def render_form():
    """Render the form for creating or editing a submittal"""
    # Check permission
    if not check_permission('create'):
        st.error("You don't have permission to create or edit submittals")
        return
    
    # Determine if we're editing or creating new
    editing_id = st.session_state.get('editing_id', None)
    
    if editing_id:
        st.title(f"Edit Submittal: {editing_id}")
        # Pre-fill form with existing data (in a real app, this would come from the database)
        title = "Concrete Mix Design"
        discipline = "Structural"
        specification_section = "03 30 00"
        description = "Submittal for concrete mix design to be used for foundation elements."
    else:
        st.title("Create New Submittal")
        # Empty form
        title = ""
        discipline = ""
        specification_section = ""
        description = ""
    
    # Create form
    with st.form("submittal_form"):
        title = st.text_input("Title", value=title)
        
        col1, col2 = st.columns(2)
        with col1:
            discipline = st.selectbox("Discipline", 
                ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil"],
                index=["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil"].index(discipline) if discipline else 0
            )
        with col2:
            specification_section = st.text_input("Specification Section", value=specification_section)
        
        description = st.text_area("Description", value=description, height=100)
        
        # File upload
        uploaded_files = st.file_uploader("Attach Files", accept_multiple_files=True)
        
        # Submittal options
        st.subheader("Submittal Options")
        priority = st.select_slider("Priority", options=["Low", "Medium", "High"], value="Medium")
        
        col1, col2 = st.columns(2)
        with col1:
            review_time = st.number_input("Expected Review Time (days)", min_value=1, max_value=30, value=7)
        with col2:
            submittal_type = st.selectbox("Submittal Type", ["Shop Drawing", "Product Data", "Sample", "Test Report", "Certificate", "Other"])
        
        # Form submission buttons
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Save Submittal")
        with col2:
            cancel = st.form_submit_button("Cancel")
    
    # Handle form submission
    if submit_button:
        if not title:
            st.error("Title is required")
        else:
            if editing_id:
                st.success(f"Submittal {editing_id} updated successfully")
            else:
                st.success("New submittal created successfully")
            
            # Reset and go back to list view
            st.session_state.current_view = "list"
            if 'editing_id' in st.session_state:
                del st.session_state.editing_id
            st.rerun()
    
    # Handle cancel
    if cancel:
        st.session_state.current_view = "list"
        if 'editing_id' in st.session_state:
            del st.session_state.editing_id
        st.rerun()