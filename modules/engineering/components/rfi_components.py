"""
RFI components for the Engineering module.

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

# Sample data for demonstration
def generate_sample_rfis():
    """Generate sample RFI data for demonstration"""
    return [
        {
            "ID": "RFI-2025-001",
            "Title": "Foundation Depth Clarification",
            "Submitter": "David Kim",
            "Assignee": "Sarah Williams",
            "Date_Created": "2025-01-15",
            "Date_Due": "2025-01-22",
            "Date_Closed": "2025-01-20",
            "Priority": "Medium",
            "Status": "Closed",
            "Category": "Structural"
        },
        {
            "ID": "RFI-2025-002",
            "Title": "Electrical Panel Location",
            "Submitter": "Sarah Williams",
            "Assignee": "James Smith",
            "Date_Created": "2025-02-03",
            "Date_Due": "2025-02-10",
            "Date_Closed": None,
            "Priority": "High",
            "Status": "Open",
            "Category": "Electrical"
        },
        {
            "ID": "RFI-2025-003",
            "Title": "HVAC Duct Routing Conflict",
            "Submitter": "Michael Davis",
            "Assignee": "Emma Brown",
            "Date_Created": "2025-02-10",
            "Date_Due": "2025-02-17",
            "Date_Closed": None,
            "Priority": "Medium",
            "Status": "Open",
            "Category": "Mechanical"
        },
        {
            "ID": "RFI-2025-004",
            "Title": "Window Frame Detail",
            "Submitter": "Jennifer Wilson",
            "Assignee": "Sarah Williams",
            "Date_Created": "2025-01-20",
            "Date_Due": "2025-01-27",
            "Date_Closed": "2025-01-25",
            "Priority": "Low",
            "Status": "Closed",
            "Category": "Architectural"
        },
        {
            "ID": "RFI-2025-005",
            "Title": "Plumbing Fixture Substitution",
            "Submitter": "James Smith",
            "Assignee": "David Kim",
            "Date_Created": "2025-02-05",
            "Date_Due": "2025-02-12",
            "Date_Closed": "2025-02-09",
            "Priority": "Medium",
            "Status": "Closed",
            "Category": "Plumbing"
        },
        {
            "ID": "RFI-2025-006",
            "Title": "Ceiling Height Clarification",
            "Submitter": "Emma Brown",
            "Assignee": "Jennifer Wilson",
            "Date_Created": "2025-02-15",
            "Date_Due": "2025-02-22",
            "Date_Closed": None,
            "Priority": "Low",
            "Status": "Under Review",
            "Category": "Architectural"
        },
        {
            "ID": "RFI-2025-007",
            "Title": "Fire Sprinkler Coverage",
            "Submitter": "David Kim",
            "Assignee": "Michael Davis",
            "Date_Created": "2025-02-18",
            "Date_Due": "2025-02-25",
            "Date_Closed": None,
            "Priority": "High",
            "Status": "Under Review",
            "Category": "Fire Protection"
        }
    ]

def render_rfi_list():
    """Render the RFI list view with filtering and sorting"""
    st.subheader("Requests for Information")
    
    # Get sample data
    rfis = generate_sample_rfis()
    
    with st.expander("Filters", expanded=True):
        # Create columns for the filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Category filter
            categories = ["All Categories"] + sorted(list(set(rfi["Category"] for rfi in rfis)))
            selected_category = st.selectbox("Category", categories, key="rfi_category_filter")
            
            # Status filter
            statuses = ["All Statuses"] + sorted(list(set(rfi["Status"] for rfi in rfis)))
            selected_status = st.selectbox("Status", statuses, key="rfi_status_filter")
        
        with col2:
            # Priority filter
            priorities = ["All Priorities"] + sorted(list(set(rfi["Priority"] for rfi in rfis)))
            selected_priority = st.selectbox("Priority", priorities, key="rfi_priority_filter")
            
            # Assignee filter
            assignees = ["All Assignees"] + sorted(list(set(rfi["Assignee"] for rfi in rfis)))
            selected_assignee = st.selectbox("Assignee", assignees, key="rfi_assignee_filter")
        
        with col3:
            # Date range filter
            min_date = min(datetime.strptime(rfi["Date_Created"], "%Y-%m-%d") for rfi in rfis)
            max_date = max(datetime.strptime(rfi["Date_Created"], "%Y-%m-%d") for rfi in rfis)
            
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
    
    if selected_category != "All Categories":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["Category"] == selected_category]
    
    if selected_status != "All Statuses":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["Status"] == selected_status]
    
    if selected_priority != "All Priorities":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["Priority"] == selected_priority]
    
    if selected_assignee != "All Assignees":
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["Assignee"] == selected_assignee]
    
    # Filter by date range
    filtered_rfis = [
        rfi for rfi in filtered_rfis 
        if start_date <= datetime.strptime(rfi["Date_Created"], "%Y-%m-%d").date() <= end_date
    ]
    
    if search_term:
        filtered_rfis = [rfi for rfi in filtered_rfis if 
                       search_term.lower() in rfi["Title"].lower() or 
                       search_term.lower() in rfi["ID"].lower() or
                       search_term.lower() in rfi["Submitter"].lower() or
                       search_term.lower() in rfi["Assignee"].lower()]

    # Add button
    if st.button("➕ Add RFI", use_container_width=True):
        st.session_state.rfi_view = "add"
        st.rerun()
    
    # Check if we have any results
    if not filtered_rfis:
        st.info("No RFIs match your filters.")
        return
    
    # Show item count
    st.caption(f"Showing {len(filtered_rfis)} RFIs")
    
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
            col1, col2, col3, col4, col_actions = row_container.columns([0.8, 3, 2, 1.5, 0.7])
            
            with col1:
                st.write(f"**{rfi['ID']}**")
                st.caption(f"{rfi['Date_Created']}")
            
            with col2:
                st.write(f"❓ **{rfi['Title']}**")
                st.caption(f"Category: {rfi['Category']}")
            
            with col3:
                # Person information
                st.markdown(f"<small><b>Assignee:</b> {rfi['Assignee']}<br><b>Submitter:</b> {rfi['Submitter']}</small>", unsafe_allow_html=True)
            
            with col4:
                # Status and priority
                status_color = {
                    "Open": "blue",
                    "Under Review": "orange",
                    "Closed": "green",
                    "Overdue": "red"
                }.get(rfi['Status'], "grey")
                
                priority_color = {
                    "High": "red",
                    "Medium": "orange",
                    "Low": "green"
                }.get(rfi['Priority'], "grey")
                
                # Calculate days remaining or overdue
                due_date = datetime.strptime(rfi["Date_Due"], "%Y-%m-%d").date()
                today = datetime.now().date()
                days_remaining = (due_date - today).days
                
                days_text = ""
                if rfi["Status"] != "Closed":
                    if days_remaining < 0:
                        days_text = f"<span style='color:red;'>{abs(days_remaining)} days overdue</span>"
                    elif days_remaining == 0:
                        days_text = "<span style='color:orange;'>Due today</span>"
                    else:
                        days_text = f"{days_remaining} days remaining"
                else:
                    if rfi["Date_Closed"]:
                        closed_date = datetime.strptime(rfi["Date_Closed"], "%Y-%m-%d").date()
                        days_to_close = (closed_date - datetime.strptime(rfi["Date_Created"], "%Y-%m-%d").date()).days
                        days_text = f"Closed in {days_to_close} days"
                
                # Status, priority, and days text
                st.markdown(f"""
                <span style='color:{status_color};'><b>{rfi['Status']}</b></span> | 
                <span style='color:{priority_color};'>{rfi['Priority']}</span><br>
                <small>{days_text}</small>
                """, unsafe_allow_html=True)
            
            # Action buttons in a single column
            with col_actions:
                # Create two buttons side by side in the actions column
                action_btn_cols = st.columns(2)
                
                # View button
                with action_btn_cols[0]:
                    if st.button("👁️", key=f"view_{rfi['ID']}", help="View RFI details"):
                        # Store RFI details in session state
                        st.session_state.selected_rfi_id = rfi['ID'] 
                        st.session_state.selected_rfi_data = rfi
                        # Set view mode
                        st.session_state["rfi_view"] = "view"
                        # Force refresh
                        st.rerun()
                
                # Edit button
                with action_btn_cols[1]:
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
        # Style for RFI details
        st.markdown("""
        <style>
            .rfi-details {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            .rfi-header {
                margin-bottom: 20px;
            }
            .rfi-section {
                margin-top: 15px;
                margin-bottom: 15px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Start RFI details container
        st.markdown('<div class="rfi-details">', unsafe_allow_html=True)
        
        # Header section
        st.markdown(f'<div class="rfi-header">', unsafe_allow_html=True)
        st.markdown(f"# {rfi['Title']}")
        
        # Calculate status tag
        status_color = {
            "Open": "blue",
            "Under Review": "orange",
            "Closed": "green",
            "Overdue": "red"
        }.get(rfi['Status'], "grey")
        
        priority_color = {
            "High": "red",
            "Medium": "orange",
            "Low": "green"
        }.get(rfi['Priority'], "grey")
        
        st.markdown(f"""
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
          <div style="background-color: {status_color}; color: white; padding: 3px 8px; border-radius: 4px;">
            {rfi['Status']}
          </div>
          <div style="background-color: {priority_color}; color: white; padding: 3px 8px; border-radius: 4px;">
            {rfi['Priority']} Priority
          </div>
          <div style="background-color: #f0f0f0; padding: 3px 8px; border-radius: 4px;">
            {rfi['Category']}
          </div>
          <div style="background-color: #f0f0f0; padding: 3px 8px; border-radius: 4px;">
            {rfi['ID']}
          </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # RFI information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div class="rfi-section">', unsafe_allow_html=True)
            st.markdown("### People")
            st.markdown(f"**Submitted by:** {rfi['Submitter']}")
            st.markdown(f"**Assigned to:** {rfi['Assignee']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="rfi-section">', unsafe_allow_html=True)
            st.markdown("### Dates")
            st.markdown(f"**Created:** {rfi['Date_Created']}")
            st.markdown(f"**Due:** {rfi['Date_Due']}")
            
            if rfi["Date_Closed"]:
                st.markdown(f"**Closed:** {rfi['Date_Closed']}")
                
                # Calculate turnaround time
                created_date = datetime.strptime(rfi["Date_Created"], "%Y-%m-%d").date()
                closed_date = datetime.strptime(rfi["Date_Closed"], "%Y-%m-%d").date()
                turnaround_days = (closed_date - created_date).days
                
                st.markdown(f"**Turnaround time:** {turnaround_days} days")
            else:
                # Calculate days remaining or overdue
                due_date = datetime.strptime(rfi["Date_Due"], "%Y-%m-%d").date()
                today = datetime.now().date()
                days_remaining = (due_date - today).days
                
                if days_remaining < 0:
                    st.markdown(f"**Status:** <span style='color:red;'>{abs(days_remaining)} days overdue</span>", unsafe_allow_html=True)
                elif days_remaining == 0:
                    st.markdown(f"**Status:** <span style='color:orange;'>Due today</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**Status:** {days_remaining} days remaining")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Question and response
        st.markdown(f'<div class="rfi-section">', unsafe_allow_html=True)
        st.markdown("### Question")
        
        # Generate a random detailed question
        questions = [
            f"Please clarify the {rfi['Title'].lower()}. The drawings show conflicting information on Sheet A-101 vs. structural details on Sheet S-201. What is the correct specification?",
            f"Regarding the {rfi['Title'].lower()}, we need additional information about the requirements. The specifications are unclear about the exact dimensions and materials to be used.",
            f"We have encountered an issue with the {rfi['Title'].lower()} during implementation. The current design appears to conflict with existing conditions on site. Please provide guidance on how to proceed."
        ]
        
        st.markdown(random.choice(questions))
        
        # If closed, show response
        if rfi["Status"] == "Closed" and rfi["Date_Closed"]:
            st.markdown("### Response")
            
            responses = [
                f"After reviewing the drawings, the correct specification for the {rfi['Title'].lower()} is as shown on Sheet S-201. Please proceed with the dimensions and materials indicated there.",
                f"The {rfi['Title'].lower()} should follow the specifications in Addendum #2, section 3.4.2. This supersedes the information shown on the original drawings.",
                f"For the {rfi['Title'].lower()}, please use the following adjusted specifications: [detailed measurements and materials]. These modifications have been approved by the design team and owner."
            ]
            
            st.markdown(random.choice(responses))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Attachments (placeholder)
        st.markdown(f'<div class="rfi-section">', unsafe_allow_html=True)
        st.markdown("### Attachments")
        
        # Generate some random attachments
        attachment_types = ["Drawing", "Specification", "Photo", "Sketch", "Calculation"]
        
        # Generate some random attachments
        attachments = []
        num_attachments = random.randint(0, 3)
        for i in range(num_attachments):
            attachment_type = random.choice(attachment_types)
            attachments.append({
                "Name": f"{attachment_type} - {rfi['ID']} - {i+1}",
                "Type": attachment_type,
                "Size": f"{random.randint(1, 10)} MB",
                "Date": (datetime.strptime(rfi['Date_Created'], "%Y-%m-%d") - timedelta(days=random.randint(0, 2))).strftime("%Y-%m-%d")
            })
        
        # Display attachments
        if attachments:
            attachments_df = pd.DataFrame(attachments)
            st.dataframe(attachments_df, use_container_width=True)
        else:
            st.info("No attachments have been added to this RFI.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Related items (placeholder)
        st.markdown(f'<div class="rfi-section">', unsafe_allow_html=True)
        st.markdown("### Related Items")
        
        # Generate some random related items
        related_items = []
        num_related = random.randint(0, 2)
        
        item_types = ["Submittal", "Change Order", "Daily Report", "Issue"]
        
        for i in range(num_related):
            item_type = random.choice(item_types)
            related_items.append({
                "ID": f"{item_type[:3].upper()}-2025-{random.randint(1, 100):03d}",
                "Type": item_type,
                "Title": f"Related {item_type} for {rfi['Title']}",
                "Status": random.choice(["Open", "Closed", "Under Review"])
            })
        
        # Display related items
        if related_items:
            related_df = pd.DataFrame(related_items)
            st.dataframe(related_df, use_container_width=True)
        else:
            st.info("No related items linked to this RFI.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Edit RFI", use_container_width=True):
                st.session_state.edit_rfi_id = rfi['ID']
                st.session_state.edit_rfi_data = rfi
                st.session_state.rfi_view = "edit"
                st.rerun()
        
        with col2:
            if rfi["Status"] != "Closed":
                if st.button("✓ Mark as Closed", use_container_width=True):
                    # In a real app, this would update the database
                    st.success(f"RFI {rfi['ID']} marked as closed.")
                    # Return to list view
                    st.session_state.rfi_view = "list"
                    st.rerun()
            else:
                if st.button("📊 View Analysis", use_container_width=True):
                    st.session_state.rfi_view = "analysis"
                    st.rerun()
        
        # End the RFI details container
        st.markdown('</div>', unsafe_allow_html=True)


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
        today = datetime.now()
        rfi = {
            "ID": f"RFI-{today.year}-{random.randint(100, 999)}",
            "Title": "",
            "Submitter": "",
            "Assignee": "",
            "Date_Created": today.strftime("%Y-%m-%d"),
            "Date_Due": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
            "Date_Closed": None,
            "Priority": "Medium",
            "Status": "Open",
            "Category": ""
        }
    
    # Create the form
    with st.form(key="rfi_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("RFI Title *", value=rfi.get("Title", ""))
            
            # Category dropdown
            category_options = ["Architectural", "Structural", "Mechanical", "Electrical", 
                               "Plumbing", "Civil", "Fire Protection", "Landscape", "Other"]
            
            # Find index of selected category if editing
            category_index = 0
            if is_edit and rfi.get("Category") in category_options:
                category_index = category_options.index(rfi.get("Category"))
            
            selected_category = st.selectbox(
                "Category *",
                category_options,
                index=category_index
            )
        
        with col2:
            # For display only
            if is_edit:
                st.text_input("RFI ID", value=rfi.get("ID", ""), disabled=True)
            
            # Priority dropdown
            priority_options = ["High", "Medium", "Low"]
            
            # Find index of selected priority if editing
            priority_index = 1  # Default to Medium
            if is_edit and rfi.get("Priority") in priority_options:
                priority_index = priority_options.index(rfi.get("Priority"))
            
            selected_priority = st.selectbox(
                "Priority *",
                priority_options,
                index=priority_index
            )
            
            # Status dropdown
            status_options = ["Open", "Under Review", "Closed"]
            
            # Find index of selected status if editing
            status_index = 0
            if is_edit and rfi.get("Status") in status_options:
                status_index = status_options.index(rfi.get("Status"))
            
            selected_status = st.selectbox(
                "Status *",
                status_options,
                index=status_index
            )
        
        # People
        st.subheader("People")
        col1, col2 = st.columns(2)
        
        with col1:
            submitter = st.text_input("Submitter *", value=rfi.get("Submitter", ""))
        
        with col2:
            assignee = st.text_input("Assignee *", value=rfi.get("Assignee", ""))
        
        # Dates
        st.subheader("Dates")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            created_date = st.date_input(
                "Date Created *",
                value=datetime.strptime(rfi.get("Date_Created", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        with col2:
            due_date = st.date_input(
                "Date Due *",
                value=datetime.strptime(rfi.get("Date_Due", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        with col3:
            if selected_status == "Closed":
                closed_date = st.date_input(
                    "Date Closed",
                    value=datetime.strptime(rfi.get("Date_Closed", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d") if rfi.get("Date_Closed") else datetime.now()
                )
            else:
                closed_date = None
        
        # Question
        st.subheader("Question")
        question = st.text_area("Question *", value=rfi.get("Question", ""), height=100)
        
        # Response (if status is Closed or in edit mode)
        if selected_status == "Closed" or (is_edit and rfi.get("Status") == "Closed"):
            st.subheader("Response")
            response = st.text_area("Response", value=rfi.get("Response", ""), height=100)
        
        # Attachments
        st.subheader("Attachments")
        uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)
        
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
            st.error("Please enter an RFI title.")
            return
        
        if not submitter:
            st.error("Please enter a submitter name.")
            return
        
        if not assignee:
            st.error("Please enter an assignee name.")
            return
        
        if not question:
            st.error("Please enter a question.")
            return
            
        # In a real app, this would save to database
        if is_edit:
            st.success(f"RFI '{title}' updated successfully!")
        else:
            st.success(f"RFI '{title}' created successfully!")
        
        # Return to list view
        st.session_state.rfi_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to previous view
        st.session_state.rfi_view = "list"
        st.rerun()


def render_rfi_analysis():
    """Render the RFI analysis view with charts and metrics"""
    st.subheader("RFI Analysis")
    
    # Get sample data
    rfis = generate_sample_rfis()
    
    # Calculate summary metrics
    total_rfis = len(rfis)
    open_rfis = len([rfi for rfi in rfis if rfi["Status"] == "Open"])
    closed_rfis = len([rfi for rfi in rfis if rfi["Status"] == "Closed"])
    under_review_rfis = len([rfi for rfi in rfis if rfi["Status"] == "Under Review"])
    
    # Calculate average response time for closed RFIs
    response_times = []
    for rfi in rfis:
        if rfi["Status"] == "Closed" and rfi["Date_Closed"]:
            created_date = datetime.strptime(rfi["Date_Created"], "%Y-%m-%d")
            closed_date = datetime.strptime(rfi["Date_Closed"], "%Y-%m-%d")
            response_time = (closed_date - created_date).days
            response_times.append(response_time)
    
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    # Summary metrics
    st.subheader("RFI Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total RFIs", f"{total_rfis}")
    
    with col2:
        st.metric("Open", f"{open_rfis}", f"{open_rfis/total_rfis:.1%} of total")
    
    with col3:
        st.metric("Under Review", f"{under_review_rfis}", f"{under_review_rfis/total_rfis:.1%} of total")
    
    with col4:
        st.metric("Closed", f"{closed_rfis}", f"{closed_rfis/total_rfis:.1%} of total")
    
    # Add average response time
    if response_times:
        st.metric("Average Response Time", f"{avg_response_time:.1f} days")
    
    # RFI distribution
    st.subheader("RFI Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution by category
        category_data = {}
        for rfi in rfis:
            category = rfi["Category"]
            if category in category_data:
                category_data[category] += 1
            else:
                category_data[category] = 1
        
        # Create a DataFrame for the chart
        category_df = pd.DataFrame({
            'Category': list(category_data.keys()),
            'Count': list(category_data.values())
        })
        
        st.write("#### Distribution by Category")
        st.bar_chart(category_df.set_index('Category'))
    
    with col2:
        # Distribution by status
        status_data = {
            "Open": open_rfis,
            "Under Review": under_review_rfis,
            "Closed": closed_rfis
        }
        
        # Create a DataFrame for the chart
        status_df = pd.DataFrame({
            'Status': list(status_data.keys()),
            'Count': list(status_data.values())
        })
        
        st.write("#### Distribution by Status")
        st.bar_chart(status_df.set_index('Status'))
    
    # RFI trend over time
    st.subheader("RFI Trend")
    
    # Group RFIs by month
    rfis_by_date = {}
    for rfi in rfis:
        month = rfi["Date_Created"][:7]  # YYYY-MM
        if month in rfis_by_date:
            rfis_by_date[month]["New"] += 1
            if rfi["Status"] == "Closed" and rfi["Date_Closed"] and rfi["Date_Closed"][:7] == month:
                rfis_by_date[month]["Closed"] += 1
        else:
            rfis_by_date[month] = {
                "New": 1,
                "Closed": 1 if rfi["Status"] == "Closed" and rfi["Date_Closed"] and rfi["Date_Closed"][:7] == month else 0
            }
    
    # Sort by date
    sorted_months = sorted(rfis_by_date.keys())
    
    # Create data for chart
    trend_data = []
    
    for month in sorted_months:
        trend_data.append({
            "Month": month,
            "New RFIs": rfis_by_date[month]["New"],
            "Closed RFIs": rfis_by_date[month]["Closed"]
        })
    
    # Create a DataFrame
    trend_df = pd.DataFrame(trend_data)
    
    # Display trend chart
    st.line_chart(trend_df.set_index('Month'))
    
    # RFI turnaround time analysis
    st.subheader("RFI Turnaround Time")
    
    # Calculate turnaround times by category
    category_turnaround = {}
    for rfi in rfis:
        if rfi["Status"] == "Closed" and rfi["Date_Closed"]:
            category = rfi["Category"]
            created_date = datetime.strptime(rfi["Date_Created"], "%Y-%m-%d")
            closed_date = datetime.strptime(rfi["Date_Closed"], "%Y-%m-%d")
            turnaround_time = (closed_date - created_date).days
            
            if category in category_turnaround:
                category_turnaround[category]["Total"] += turnaround_time
                category_turnaround[category]["Count"] += 1
            else:
                category_turnaround[category] = {"Total": turnaround_time, "Count": 1}
    
    # Calculate averages
    category_avg = {}
    for category, data in category_turnaround.items():
        category_avg[category] = data["Total"] / data["Count"]
    
    # Create a DataFrame for the chart
    turnaround_df = pd.DataFrame({
        'Category': list(category_avg.keys()),
        'Average Days': list(category_avg.values())
    })
    
    # Display the chart
    st.bar_chart(turnaround_df.set_index('Category'))