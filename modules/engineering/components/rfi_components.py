"""
RFI (Request for Information) components for the Engineering module.

This module provides the UI components for RFI management including:
- RFI list view
- RFI details view
- RFI form (add/edit)
- RFI analysis view
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.express as px
import plotly.graph_objects as go

# Sample data for demonstration
def generate_sample_rfis():
    """Generate sample RFI data for demonstration"""
    categories = ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil"]
    statuses = ["Open", "Answered", "Closed", "On Hold"]
    priorities = ["Low", "Medium", "High", "Critical"]
    
    rfis = []
    
    for i in range(1, 16):
        # Generate random dates within a reasonable range
        issue_date = datetime.now() - timedelta(days=random.randint(1, 60))
        
        # Some RFIs are answered, some are not
        is_answered = random.choice([True, False])
        answer_date = None
        resolution_days = None
        status = "Open"
        
        if is_answered:
            # Answer date is after issue date
            answer_date = issue_date + timedelta(days=random.randint(1, 14))
            resolution_days = (answer_date - issue_date).days
            
            # Determine status based on answer
            if random.random() < 0.7:  # 70% chance to be closed if answered
                status = "Closed"
            else:
                status = "Answered"
        else:
            # If not answered, it's either Open or On Hold
            status = random.choice(["Open", "On Hold"])
        
        # Format dates as strings for display
        issue_date_str = issue_date.strftime("%Y-%m-%d")
        answer_date_str = answer_date.strftime("%Y-%m-%d") if answer_date else ""
        
        # Create RFI record
        rfi = {
            "ID": f"RFI-{i:03d}",
            "Title": f"Clarification on {random.choice(categories)} Detail",
            "Description": f"Request for clarification regarding the {random.choice(categories).lower()} drawings on level {random.randint(1, 15)}.",
            "Category": random.choice(categories),
            "Priority": random.choice(priorities),
            "Status": status,
            "Issue_Date": issue_date_str,
            "Answer_Date": answer_date_str,
            "Resolution_Days": resolution_days,
            "Submitted_By": random.choice(["J. Smith", "L. Johnson", "A. Martinez", "K. Wong", "S. Davis"]),
            "Assigned_To": random.choice(["Design Team", "Structural Engineer", "MEP Engineer", "Architect", "Civil Engineer"])
        }
        
        rfis.append(rfi)
    
    return rfis

def render_rfi_list():
    """Render the RFI list view with filtering and sorting"""
    st.subheader("Requests for Information (RFIs)")
    
    # Get sample data
    rfis = generate_sample_rfis()
    
    with st.expander("Filters", expanded=True):
        # Create columns for the filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Status filter
            statuses = ["All Statuses"] + sorted(list(set(rfi["Status"] for rfi in rfis)))
            selected_status = st.selectbox("Status", statuses, key="rfi_status_filter")
            
            # Category filter
            categories = ["All Categories"] + sorted(list(set(rfi["Category"] for rfi in rfis)))
            selected_category = st.selectbox("Category", categories, key="rfi_category_filter")
        
        with col2:
            # Priority filter
            priorities = ["All Priorities"] + sorted(list(set(rfi["Priority"] for rfi in rfis)))
            selected_priority = st.selectbox("Priority", priorities, key="rfi_priority_filter")
            
            # Assignment filter
            assignments = ["All Assignments"] + sorted(list(set(rfi["Assigned_To"] for rfi in rfis)))
            selected_assignment = st.selectbox("Assigned To", assignments, key="rfi_assignment_filter")
        
        with col3:
            # Date range filter
            min_date = min(datetime.strptime(rfi["Issue_Date"], "%Y-%m-%d") for rfi in rfis)
            max_date = max(
                datetime.strptime(rfi["Answer_Date"], "%Y-%m-%d") if rfi["Answer_Date"] else datetime.now() 
                for rfi in rfis
            )
            
            start_date = st.date_input(
                "Start Date",
                value=min_date,
                key="rfi_start_date"
            )
            
            end_date = st.date_input(
                "End Date",
                value=max_date,
                key="rfi_end_date"
            )
            
            # Search field
            search_term = st.text_input("Search", key="rfi_search", placeholder="Search RFIs...")
    
    # Filter the data based on selections
    filtered_rfis = rfis
    
    # Filter by status
    if selected_status != "All Statuses":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["Status"] == selected_status]
    
    # Filter by category
    if selected_category != "All Categories":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["Category"] == selected_category]
    
    # Filter by priority
    if selected_priority != "All Priorities":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["Priority"] == selected_priority]
    
    # Filter by assignment
    if selected_assignment != "All Assignments":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["Assigned_To"] == selected_assignment]
    
    # Filter by date range
    filtered_rfis = [
        rfi for rfi in filtered_rfis 
        if start_date <= datetime.strptime(rfi["Issue_Date"], "%Y-%m-%d").date() <= end_date
    ]
    
    # Filter by search term
    if search_term:
        filtered_rfis = [rfi for rfi in filtered_rfis if 
                         search_term.lower() in rfi["ID"].lower() or
                         search_term.lower() in rfi["Title"].lower() or
                         search_term.lower() in rfi["Description"].lower()]
    
    # Layout for action buttons
    col1, col2 = st.columns([0.8, 0.2])
    
    with col1:
        # Show item count
        st.caption(f"Showing {len(filtered_rfis)} RFIs")
    
    with col2:
        # Add button
        if st.button("➕ Add RFI", use_container_width=True):
            st.session_state.rfi_view = "add"
            st.rerun()
    
    # Analysis button
    if st.button("📊 View Analysis", use_container_width=True):
        st.session_state.rfi_view = "analysis"
        st.rerun()
    
    # Check if we have any results
    if not filtered_rfis:
        st.info("No RFIs match your filters.")
        return
    
    # Display the filtered RFIs
    for rfi in filtered_rfis:
        # Create a container for each RFI
        rfi_container = st.container()
        
        with rfi_container:
            # Add a subtle divider between RFIs
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
            
            # Create a row with columns for the RFI data and action buttons
            row_container = st.container()
            
            # Create a more balanced row layout with condensed columns
            col1, col2, col3, col4, col_actions = row_container.columns([1, 2, 2, 1.5, 0.5])
            
            with col1:
                # Status indicator
                status_color = {
                    "Open": "🔴",
                    "Answered": "🟠",
                    "Closed": "🟢",
                    "On Hold": "⚪"
                }
                
                st.write(f"{status_color.get(rfi['Status'], '⚪')} **{rfi['ID']}**")
                
                # Priority indicator
                priority_color = {
                    "Low": "🔵",
                    "Medium": "🟡",
                    "High": "🟠",
                    "Critical": "🔴"
                }
                
                st.caption(f"{priority_color.get(rfi['Priority'], '⚪')} {rfi['Priority']} Priority")
            
            with col2:
                st.write(f"**{rfi['Title']}**")
                st.caption(f"Category: {rfi['Category']}")
            
            with col3:
                # Submitted and assignment info
                st.write(f"**Submitted By:** {rfi['Submitted_By']}")
                st.caption(f"Assigned To: {rfi['Assigned_To']}")
            
            with col4:
                # Dates and resolution time
                st.write(f"**Issued:** {rfi['Issue_Date']}")
                
                if rfi['Answer_Date']:
                    st.caption(f"Answered: {rfi['Answer_Date']} ({rfi['Resolution_Days']} days)")
                else:
                    # Calculate days open
                    issue_date = datetime.strptime(rfi['Issue_Date'], "%Y-%m-%d")
                    days_open = (datetime.now() - issue_date).days
                    st.caption(f"Outstanding: {days_open} days")
            
            # Action buttons in a single column
            with col_actions:
                # Create two buttons stacked in the actions column
                if st.button("👁️", key=f"view_{rfi['ID']}", help="View RFI details"):
                    # Store RFI details in session state
                    st.session_state.selected_rfi_id = rfi['ID'] 
                    st.session_state.selected_rfi_data = rfi
                    # Set view mode
                    st.session_state["rfi_view"] = "view"
                    # Force refresh
                    st.rerun()
                
                if st.button("✏️", key=f"edit_{rfi['ID']}", help="Edit RFI"):
                    # Store RFI data for editing
                    st.session_state.edit_rfi_id = rfi['ID']
                    st.session_state.edit_rfi_data = rfi
                    # Set edit mode 
                    st.session_state["rfi_view"] = "edit"
                    # Force refresh
                    st.rerun()

def render_rfi_details():
    """Render the RFI details view (single record view)"""
    st.subheader("RFI Details")
    
    # Ensure we have a selected RFI
    if not st.session_state.get("selected_rfi_id"):
        st.error("No RFI selected. Please select an RFI from the list.")
        # Return to list view
        st.session_state.rfi_view = "list"
        st.rerun()
        return
    
    # Get the selected RFI data
    rfi = st.session_state.get("selected_rfi_data", None)
    
    if not rfi:
        # If somehow we have an ID but no data, try to find it
        rfis = generate_sample_rfis()
        rfi = next((r for r in rfis if r["ID"] == st.session_state.selected_rfi_id), None)
        
        if not rfi:
            st.error(f"RFI with ID {st.session_state.selected_rfi_id} not found.")
            # Return to list view
            st.session_state.rfi_view = "list"
            st.rerun()
            return
    
    # Display RFI details
    with st.container():
        # Create columns for basic info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Status indicator
            status_color = {
                "Open": "🔴",
                "Answered": "🟠",
                "Closed": "🟢",
                "On Hold": "⚪"
            }
            
            status_bg_color = {
                "Open": "#FEE2E2",  # Light red
                "Answered": "#FEF3C7",  # Light yellow
                "Closed": "#D1FAE5",  # Light green
                "On Hold": "#F3F4F6"   # Light gray
            }
            
            st.markdown(
                f"<div style='background-color: {status_bg_color.get(rfi['Status'], '#F3F4F6')}; padding: 8px; border-radius: 4px;'>"
                f"<strong>Status:</strong> {status_color.get(rfi['Status'], '⚪')} {rfi['Status']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col2:
            # Priority indicator
            priority_color = {
                "Low": "🔵",
                "Medium": "🟡",
                "High": "🟠",
                "Critical": "🔴"
            }
            
            priority_bg_color = {
                "Low": "#DBEAFE",  # Light blue
                "Medium": "#FEF3C7",  # Light yellow
                "High": "#FFEDD5",  # Light orange
                "Critical": "#FEE2E2"  # Light red
            }
            
            st.markdown(
                f"<div style='background-color: {priority_bg_color.get(rfi['Priority'], '#F3F4F6')}; padding: 8px; border-radius: 4px;'>"
                f"<strong>Priority:</strong> {priority_color.get(rfi['Priority'], '⚪')} {rfi['Priority']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"<div style='background-color: #F3F4F6; padding: 8px; border-radius: 4px;'>"
                f"<strong>Category:</strong> {rfi['Category']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"<div style='background-color: #F3F4F6; padding: 8px; border-radius: 4px;'>"
                f"<strong>ID:</strong> {rfi['ID']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        # Title and description
        st.markdown(f"## {rfi['Title']}")
        
        st.markdown("### Description")
        st.markdown(
            f"<div style='background-color: #F9FAFB; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
            f"{rfi['Description']}"
            f"</div>",
            unsafe_allow_html=True
        )
        
        # Submission details
        st.markdown("### Submission Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Submitted By:** {rfi['Submitted_By']}")
            st.markdown(f"**Issue Date:** {rfi['Issue_Date']}")
        
        with col2:
            st.markdown(f"**Assigned To:** {rfi['Assigned_To']}")
            
            if rfi['Answer_Date']:
                st.markdown(f"**Answer Date:** {rfi['Answer_Date']}")
                st.markdown(f"**Resolution Time:** {rfi['Resolution_Days']} days")
            else:
                # Calculate days open
                issue_date = datetime.strptime(rfi['Issue_Date'], "%Y-%m-%d")
                days_open = (datetime.now() - issue_date).days
                st.markdown(f"**Days Outstanding:** {days_open} days")
        
        # Generate a random longer description for detail
        additional_details = [
            f"This RFI relates to the {rfi['Category'].lower()} drawings that show incomplete details for the connection between components.",
            f"Further clarification needed on the {rfi['Category'].lower()} specifications as there appears to be a discrepancy with the design intent.",
            f"The {rfi['Category'].lower()} documents do not provide sufficient detail for installation. Request additional information.",
            f"There is a conflict between the {rfi['Category'].lower()} drawings and the structural requirements. Please advise on the proper approach.",
            f"The team has identified a potential issue with the {rfi['Category'].lower()} design that may impact the schedule if not addressed promptly."
        ]
        
        st.markdown("### Detailed Information")
        st.markdown(
            f"<div style='background-color: #F9FAFB; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
            f"{random.choice(additional_details)}"
            f"</div>",
            unsafe_allow_html=True
        )
        
        # Add response section
        st.markdown("### Response")
        
        if rfi['Answer_Date']:
            # Generate random response for answered RFIs
            responses = [
                f"The {rfi['Category'].lower()} details have been clarified in the updated drawings. Please refer to revision C of the plans.",
                f"After review, the design team confirms that the approach shown in detail 5/A4.2 is correct. Proceed with installation as shown.",
                f"The discrepancy has been resolved. The correct dimension is 24\" not 18\" as shown in the original drawings.",
                f"We have reviewed the conflict and determined that the structural requirements take precedence. Please adjust the {rfi['Category'].lower()} accordingly.",
                f"Additional information has been provided in the attached detail. This will be incorporated into the next drawing revision."
            ]
            
            st.markdown(
                f"<div style='background-color: #F0FDF4; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(responses)}"
                f"</div>",
                unsafe_allow_html=True
            )
        else:
            st.info("This RFI has not been answered yet.")
        
        # Add attachments section (placeholder)
        st.markdown("### Attachments")
        
        # Simulate some attachments
        has_attachments = random.choice([True, False])
        
        if has_attachments:
            attachments = [
                {"name": f"{rfi['ID']}_Drawing_Detail.pdf", "type": "PDF", "size": "2.4 MB", "date": rfi['Issue_Date']},
                {"name": f"{rfi['ID']}_Photo.jpg", "type": "Image", "size": "1.8 MB", "date": rfi['Issue_Date']}
            ]
            
            if rfi['Answer_Date']:
                attachments.append({"name": f"{rfi['ID']}_Response_Detail.pdf", "type": "PDF", "size": "3.1 MB", "date": rfi['Answer_Date']})
            
            # Create a DataFrame for the attachments
            df_attachments = pd.DataFrame(attachments)
            
            # Display the attachments
            st.dataframe(df_attachments, use_container_width=True)
        else:
            st.info("No attachments for this RFI.")
        
        # Add comment section (placeholder)
        st.markdown("### Comments")
        
        # Simulate some comments
        has_comments = random.choice([True, False])
        
        if has_comments:
            comments = [
                {"author": rfi['Submitted_By'], "date": rfi['Issue_Date'], "text": "Submitted this RFI after team discussion."},
                {"author": "Project Manager", "date": rfi['Issue_Date'], "text": "Forwarded to design team for review."}
            ]
            
            if rfi['Answer_Date']:
                comments.append({"author": rfi['Assigned_To'], "date": rfi['Answer_Date'], "text": "Response provided with updated details."})
                comments.append({"author": "Project Manager", "date": rfi['Answer_Date'], "text": "Response reviewed and accepted."})
            
            # Display the comments
            for comment in comments:
                st.markdown(
                    f"<div style='background-color: #F9FAFB; padding: 10px; border-radius: 4px; margin-bottom: 10px;'>"
                    f"<strong>{comment['author']}</strong> <small>{comment['date']}</small><br>"
                    f"{comment['text']}"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("No comments for this RFI.")
        
        # Action buttons at the bottom
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Edit RFI", use_container_width=True):
                st.session_state.edit_rfi_id = rfi['ID']
                st.session_state.edit_rfi_data = rfi
                st.session_state.rfi_view = "edit"
                st.rerun()
        
        with col2:
            if st.button("📊 View Analysis", use_container_width=True):
                st.session_state.rfi_view = "analysis"
                st.rerun()

def render_rfi_form(is_edit=False):
    """Render the RFI creation/edit form"""
    if is_edit:
        st.subheader("Edit RFI")
        # Ensure we have an RFI to edit
        if not st.session_state.get("edit_rfi_id"):
            st.error("No RFI selected for editing. Please select an RFI from the list.")
            # Return to list view
            st.session_state.rfi_view = "list"
            st.rerun()
            return
        
        # Get the RFI data for editing
        rfi = st.session_state.get("edit_rfi_data", {})
    else:
        st.subheader("Create New RFI")
        # Initialize empty RFI for new entries
        rfi = {
            "ID": f"RFI-{random.randint(100, 999)}",
            "Title": "",
            "Description": "",
            "Category": "",
            "Priority": "Medium",
            "Status": "Open",
            "Issue_Date": datetime.now().strftime("%Y-%m-%d"),
            "Answer_Date": "",
            "Resolution_Days": None,
            "Submitted_By": "",
            "Assigned_To": ""
        }
    
    # Create the form
    with st.form(key="rfi_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            # For display only in edit mode
            if is_edit:
                st.text_input("RFI ID", value=rfi.get("ID", ""), disabled=True)
            
            title = st.text_input("Title *", value=rfi.get("Title", ""))
            
            # Categories
            categories = ["Architectural", "Structural", "Mechanical", "Electrical", "Plumbing", "Civil"]
            
            # Find index of selected category if editing
            category_index = 0
            if is_edit and rfi.get("Category") in categories:
                category_index = categories.index(rfi.get("Category"))
            
            selected_category = st.selectbox(
                "Category *",
                categories,
                index=category_index
            )
        
        with col2:
            # Priority options
            priorities = ["Low", "Medium", "High", "Critical"]
            
            # Find index of selected priority if editing
            priority_index = priorities.index("Medium")  # Default to Medium
            if is_edit and rfi.get("Priority") in priorities:
                priority_index = priorities.index(rfi.get("Priority"))
            
            selected_priority = st.selectbox(
                "Priority *",
                priorities,
                index=priority_index
            )
            
            # Status options
            statuses = ["Open", "Answered", "Closed", "On Hold"]
            
            # Find index of selected status if editing
            status_index = statuses.index("Open")  # Default to Open
            if is_edit and rfi.get("Status") in statuses:
                status_index = statuses.index(rfi.get("Status"))
            
            selected_status = st.selectbox(
                "Status *",
                statuses,
                index=status_index
            )
        
        # Description
        st.subheader("Description")
        description = st.text_area(
            "Description *",
            value=rfi.get("Description", ""),
            height=150,
            placeholder="Provide a detailed description of the information requested..."
        )
        
        # Submission details
        st.subheader("Submission Details")
        col1, col2 = st.columns(2)
        
        with col1:
            submitted_by = st.text_input(
                "Submitted By *",
                value=rfi.get("Submitted_By", ""),
                placeholder="Name of person submitting the RFI"
            )
            
            issue_date = st.date_input(
                "Issue Date *",
                value=datetime.strptime(rfi.get("Issue_Date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        with col2:
            assigned_to = st.text_input(
                "Assigned To *",
                value=rfi.get("Assigned_To", ""),
                placeholder="Person or team this RFI is assigned to"
            )
            
            # Only show answer date if status is Answered or Closed
            if selected_status in ["Answered", "Closed"]:
                answer_date_value = None
                if rfi.get("Answer_Date"):
                    answer_date_value = datetime.strptime(rfi.get("Answer_Date"), "%Y-%m-%d")
                else:
                    answer_date_value = datetime.now()
                
                answer_date = st.date_input(
                    "Answer Date",
                    value=answer_date_value
                )
            else:
                answer_date = None
        
        # Response section (only show if status is Answered or Closed)
        if selected_status in ["Answered", "Closed"]:
            st.subheader("Response")
            response = st.text_area(
                "Response",
                value=rfi.get("Response", ""),
                height=150,
                placeholder="Provide the response to this RFI..."
            )
        else:
            response = ""
        
        # Attachments
        st.subheader("Attachments")
        uploaded_files = st.file_uploader("Upload Attachments", accept_multiple_files=True)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "Save RFI" if is_edit else "Create RFI",
                use_container_width=True
            )
        
        with col2:
            cancel_button = st.form_submit_button(
                "Cancel",
                use_container_width=True
            )
    
    # Handle form submission
    if submit_button:
        # Validate required fields
        if not title:
            st.error("Please enter a title.")
            return
        
        if not description:
            st.error("Please enter a description.")
            return
        
        if not submitted_by:
            st.error("Please enter who submitted this RFI.")
            return
        
        if not assigned_to:
            st.error("Please enter who this RFI is assigned to.")
            return
        
        # Calculate resolution days if answered
        resolution_days = None
        if answer_date and selected_status in ["Answered", "Closed"]:
            resolution_days = (answer_date - issue_date).days
        
        # In a real app, this would save to database
        if is_edit:
            st.success(f"RFI {rfi['ID']} updated successfully!")
        else:
            st.success(f"New RFI created successfully!")
        
        # Return to list view
        st.session_state.rfi_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to previous view
        if is_edit and st.session_state.get("selected_rfi_id") == st.session_state.get("edit_rfi_id"):
            # If editing from detail view, return to detail view
            st.session_state.rfi_view = "view"
        else:
            # Otherwise return to list view
            st.session_state.rfi_view = "list"
        
        st.rerun()

def render_rfi_analysis():
    """Render the RFI analysis view with charts and metrics"""
    st.subheader("RFI Analysis")
    
    # Get sample data
    rfis = generate_sample_rfis()
    
    # Calculate summary metrics
    total_rfis = len(rfis)
    open_rfis = sum(1 for rfi in rfis if rfi["Status"] in ["Open", "On Hold"])
    answered_rfis = sum(1 for rfi in rfis if rfi["Status"] == "Answered")
    closed_rfis = sum(1 for rfi in rfis if rfi["Status"] == "Closed")
    
    # Calculate average resolution time
    resolution_times = [rfi["Resolution_Days"] for rfi in rfis if rfi["Resolution_Days"] is not None]
    avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0
    
    # Summary metrics in a nice grid
    st.subheader("Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total RFIs", f"{total_rfis}")
    
    with col2:
        st.metric("Open RFIs", f"{open_rfis}", delta=f"{open_rfis/total_rfis:.0%}")
    
    with col3:
        st.metric("Closed RFIs", f"{closed_rfis}", delta=f"{closed_rfis/total_rfis:.0%}")
    
    with col4:
        st.metric("Avg. Resolution Time", f"{avg_resolution_time:.1f} days")
    
    # Create tabs for different analysis views
    tab1, tab2, tab3 = st.tabs(["Status & Priority", "Categories", "Response Times"])
    
    # Tab 1: Status & Priority Analysis
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Status breakdown
            status_counts = {}
            for rfi in rfis:
                status = rfi["Status"]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            status_df = pd.DataFrame({
                'Status': list(status_counts.keys()),
                'Count': list(status_counts.values())
            })
            
            # Create Plotly pie chart
            fig = px.pie(
                status_df, 
                values='Count', 
                names='Status',
                title='RFI Status Distribution',
                color='Status',
                color_discrete_map={
                    'Open': '#EF4444',      # Red
                    'Answered': '#F59E0B',  # Amber
                    'Closed': '#10B981',    # Green
                    'On Hold': '#9CA3AF'    # Gray
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Priority breakdown
            priority_counts = {}
            for rfi in rfis:
                priority = rfi["Priority"]
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            priority_df = pd.DataFrame({
                'Priority': list(priority_counts.keys()),
                'Count': list(priority_counts.values())
            })
            
            # Sort by priority level
            priority_order = ['Critical', 'High', 'Medium', 'Low']
            priority_df['Priority'] = pd.Categorical(priority_df['Priority'], categories=priority_order, ordered=True)
            priority_df = priority_df.sort_values('Priority')
            
            # Create Plotly bar chart
            fig = px.bar(
                priority_df, 
                x='Priority', 
                y='Count',
                title='RFI Priority Distribution',
                color='Priority',
                color_discrete_map={
                    'Critical': '#EF4444',  # Red
                    'High': '#F59E0B',      # Amber
                    'Medium': '#FBBF24',    # Yellow
                    'Low': '#3B82F6'        # Blue
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Status by priority
        st.subheader("Status by Priority")
        
        # Create a cross-tabulation of status and priority
        status_priority = []
        for rfi in rfis:
            status_priority.append({
                'Status': rfi['Status'],
                'Priority': rfi['Priority']
            })
        
        # Create DataFrame
        sp_df = pd.DataFrame(status_priority)
        
        # Create a pivot table
        pivot_table = pd.crosstab(sp_df['Priority'], sp_df['Status'])
        
        # Reorder priority levels
        pivot_table = pivot_table.reindex(priority_order)
        
        # Create stacked bar chart
        fig = px.bar(
            pivot_table, 
            barmode='stack',
            title='RFI Status by Priority',
            color_discrete_map={
                'Open': '#EF4444',      # Red
                'Answered': '#F59E0B',  # Amber
                'Closed': '#10B981',    # Green
                'On Hold': '#9CA3AF'    # Gray
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Categories Analysis
    with tab2:
        # Category breakdown
        category_counts = {}
        for rfi in rfis:
            category = rfi["Category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        category_df = pd.DataFrame({
            'Category': list(category_counts.keys()),
            'Count': list(category_counts.values())
        })
        
        # Sort by count
        category_df = category_df.sort_values('Count', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            category_df, 
            x='Count', 
            y='Category',
            title='RFI Category Distribution',
            orientation='h',
            color='Count',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Category by status
        status_category = []
        for rfi in rfis:
            status_category.append({
                'Status': rfi['Status'],
                'Category': rfi['Category']
            })
        
        # Create DataFrame
        sc_df = pd.DataFrame(status_category)
        
        # Create a pivot table
        pivot_table = pd.crosstab(sc_df['Category'], sc_df['Status'])
        
        # Create stacked bar chart
        fig = px.bar(
            pivot_table, 
            barmode='stack',
            title='RFI Status by Category',
            color_discrete_map={
                'Open': '#EF4444',      # Red
                'Answered': '#F59E0B',  # Amber
                'Closed': '#10B981',    # Green
                'On Hold': '#9CA3AF'    # Gray
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Response Times Analysis
    with tab3:
        # Prepare data for response time analysis
        response_times = []
        for rfi in rfis:
            if rfi["Resolution_Days"] is not None:
                response_times.append({
                    'ID': rfi['ID'],
                    'Category': rfi['Category'],
                    'Priority': rfi['Priority'],
                    'Resolution_Days': rfi['Resolution_Days']
                })
        
        # Convert to DataFrame
        rt_df = pd.DataFrame(response_times)
        
        if not rt_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Average resolution time by priority
                avg_by_priority = rt_df.groupby('Priority')['Resolution_Days'].mean().reset_index()
                
                # Sort by priority level
                avg_by_priority['Priority'] = pd.Categorical(avg_by_priority['Priority'], categories=priority_order, ordered=True)
                avg_by_priority = avg_by_priority.sort_values('Priority')
                
                # Create bar chart
                fig = px.bar(
                    avg_by_priority, 
                    x='Priority', 
                    y='Resolution_Days',
                    title='Avg. Resolution Time by Priority (Days)',
                    color='Priority',
                    color_discrete_map={
                        'Critical': '#EF4444',  # Red
                        'High': '#F59E0B',      # Amber
                        'Medium': '#FBBF24',    # Yellow
                        'Low': '#3B82F6'        # Blue
                    }
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Average resolution time by category
                avg_by_category = rt_df.groupby('Category')['Resolution_Days'].mean().reset_index()
                
                # Sort by resolution time
                avg_by_category = avg_by_category.sort_values('Resolution_Days', ascending=False)
                
                # Create bar chart
                fig = px.bar(
                    avg_by_category, 
                    x='Category', 
                    y='Resolution_Days',
                    title='Avg. Resolution Time by Category (Days)',
                    color='Resolution_Days',
                    color_continuous_scale=px.colors.sequential.Viridis
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Resolution time distribution
            fig = px.histogram(
                rt_df, 
                x='Resolution_Days',
                nbins=10,
                title='Resolution Time Distribution (Days)',
                color_discrete_sequence=['#3B82F6']  # Blue
            )
            
            # Add a vertical line for the average
            fig.add_vline(
                x=avg_resolution_time,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Avg: {avg_resolution_time:.1f} days",
                annotation_position="top right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No resolution time data available for analysis.")
    
    # Trend analysis
    st.subheader("RFI Trend Analysis")
    
    # Prepare data for trend analysis
    trend_data = []
    for rfi in rfis:
        issue_date = datetime.strptime(rfi["Issue_Date"], "%Y-%m-%d")
        trend_data.append({
            'Date': issue_date,
            'Type': 'Issued',
            'Count': 1
        })
        
        if rfi["Answer_Date"]:
            answer_date = datetime.strptime(rfi["Answer_Date"], "%Y-%m-%d")
            trend_data.append({
                'Date': answer_date,
                'Type': 'Answered',
                'Count': 1
            })
    
    # Convert to DataFrame
    trend_df = pd.DataFrame(trend_data)
    
    # Group by date and type
    trend_by_date = trend_df.groupby([pd.Grouper(key='Date', freq='W'), 'Type'])['Count'].sum().reset_index()
    
    # Create cumulative sums
    issued_cum = trend_by_date[trend_by_date['Type'] == 'Issued'].sort_values('Date')
    issued_cum['Cumulative'] = issued_cum['Count'].cumsum()
    
    answered_cum = trend_by_date[trend_by_date['Type'] == 'Answered'].sort_values('Date')
    if not answered_cum.empty:
        answered_cum['Cumulative'] = answered_cum['Count'].cumsum()
    
    # Create the figure
    fig = go.Figure()
    
    # Add issued line
    fig.add_trace(go.Scatter(
        x=issued_cum['Date'],
        y=issued_cum['Cumulative'],
        mode='lines+markers',
        name='RFIs Issued',
        line=dict(color='#3B82F6', width=2)  # Blue
    ))
    
    # Add answered line if we have data
    if not answered_cum.empty:
        fig.add_trace(go.Scatter(
            x=answered_cum['Date'],
            y=answered_cum['Cumulative'],
            mode='lines+markers',
            name='RFIs Answered',
            line=dict(color='#10B981', width=2)  # Green
        ))
    
    # Layout
    fig.update_layout(
        title='Cumulative RFIs Over Time',
        xaxis_title='Date',
        yaxis_title='Cumulative Count',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)