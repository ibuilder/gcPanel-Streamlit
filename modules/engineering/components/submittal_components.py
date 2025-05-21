"""
Submittal components for the Engineering module.

This module provides the UI components for submittal management including:
- Submittal list view
- Submittal details view
- Submittal form (add/edit)
- Submittal analysis view
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.express as px
import plotly.graph_objects as go

# Sample data for demonstration
def generate_sample_submittals():
    """Generate sample submittal data for demonstration"""
    categories = ["Mechanical", "Electrical", "Structural", "Architectural", "Plumbing", "Civil", "Finishes"]
    statuses = ["Pending", "Approved", "Approved as Noted", "Revise and Resubmit", "Rejected"]
    
    submittals = []
    
    for i in range(1, 20):
        # Generate random dates within a reasonable range
        submission_date = datetime.now() - timedelta(days=random.randint(1, 90))
        
        # Some submittals are reviewed, some are not
        is_reviewed = random.choice([True, False])
        review_date = None
        approval_status = "Pending"
        
        if is_reviewed:
            # Review date is after submission date
            review_date = submission_date + timedelta(days=random.randint(2, 21))
            
            # Generate a status for reviewed submittals
            status_weights = [0.45, 0.25, 0.20, 0.10]  # weights for different outcomes
            status_options = ["Approved", "Approved as Noted", "Revise and Resubmit", "Rejected"]
            approval_status = random.choices(status_options, weights=status_weights, k=1)[0]
        
        # Format dates as strings for display
        submission_date_str = submission_date.strftime("%Y-%m-%d")
        review_date_str = review_date.strftime("%Y-%m-%d") if review_date else ""
        
        # Create submittal record
        submittal = {
            "ID": f"SUB-{i:03d}",
            "Title": f"{random.choice(categories)} {generate_random_item(categories)}",
            "Description": f"Submittal for {random.choice(categories).lower()} component specifications and installation details.",
            "Category": random.choice(categories),
            "Spec_Section": f"{random.randint(1, 16)}{random.randint(1000, 9999)}",
            "Status": approval_status,
            "Submission_Date": submission_date_str,
            "Review_Date": review_date_str,
            "Review_Days": (review_date - submission_date).days if review_date else None,
            "Submitted_By": random.choice(["Contractor", "Subcontractor", "Vendor", "Manufacturer"]),
            "Reviewed_By": random.choice(["Architect", "Engineer", "Design Team", "Project Manager"]) if is_reviewed else ""
        }
        
        submittals.append(submittal)
    
    return submittals

def generate_random_item(categories):
    """Generate a random item based on category"""
    items = {
        "Mechanical": ["Pump", "Chiller", "Air Handler", "Fan", "Ductwork", "VAV Box", "Grille", "Damper"],
        "Electrical": ["Panel", "Switch", "Receptacle", "Fixture", "Transformer", "Generator", "Conduit", "Wire"],
        "Structural": ["Steel", "Concrete Mix", "Rebar", "Connection", "Beam", "Column", "Joist", "Deck"],
        "Architectural": ["Door", "Window", "Partition", "Ceiling", "Flooring", "Wall", "Hardware", "Finish"],
        "Plumbing": ["Pipe", "Fixture", "Valve", "Pump", "Heater", "Insulation", "Drain", "Trap"],
        "Civil": ["Drainage", "Paving", "Site", "Utility", "Grading", "Erosion Control", "Storm Water"],
        "Finishes": ["Paint", "Tile", "Carpet", "Wallcovering", "Ceiling", "Flooring", "Cabinet", "Countertop"]
    }
    
    # Get a random category if not in our dictionary
    category = random.choice(list(items.keys())) if not any(cat in categories for cat in items.keys()) else \
              next((cat for cat in categories if cat in items.keys()), random.choice(list(items.keys())))
    
    # Return a random item from that category
    return f"{random.choice(items[category])}"

def render_submittal_list():
    """Render the submittal list view with filtering and sorting"""
    st.subheader("Submittals")
    
    # Get sample data
    submittals = generate_sample_submittals()
    
    with st.expander("Filters", expanded=True):
        # Create columns for the filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Status filter
            statuses = ["All Statuses"] + sorted(list(set(submittal["Status"] for submittal in submittals)))
            selected_status = st.selectbox("Status", statuses, key="submittal_status_filter")
            
            # Category filter
            categories = ["All Categories"] + sorted(list(set(submittal["Category"] for submittal in submittals)))
            selected_category = st.selectbox("Category", categories, key="submittal_category_filter")
        
        with col2:
            # Spec section filter
            spec_sections = ["All Spec Sections"] + sorted(list(set(submittal["Spec_Section"] for submittal in submittals)))
            selected_spec = st.selectbox("Spec Section", spec_sections, key="submittal_spec_filter")
            
            # Submitted by filter
            submitters = ["All Submitters"] + sorted(list(set(submittal["Submitted_By"] for submittal in submittals)))
            selected_submitter = st.selectbox("Submitted By", submitters, key="submittal_submitter_filter")
        
        with col3:
            # Date range filter
            min_date = min(datetime.strptime(submittal["Submission_Date"], "%Y-%m-%d") for submittal in submittals)
            max_date = max(
                datetime.strptime(submittal["Review_Date"], "%Y-%m-%d") if submittal["Review_Date"] else datetime.now() 
                for submittal in submittals
            )
            
            start_date = st.date_input(
                "Start Date",
                value=min_date,
                key="submittal_start_date"
            )
            
            end_date = st.date_input(
                "End Date",
                value=max_date,
                key="submittal_end_date"
            )
            
            # Search field
            search_term = st.text_input("Search", key="submittal_search", placeholder="Search submittals...")
    
    # Filter the data based on selections
    filtered_submittals = submittals
    
    # Filter by status
    if selected_status != "All Statuses":
        filtered_submittals = [submittal for submittal in filtered_submittals if submittal["Status"] == selected_status]
    
    # Filter by category
    if selected_category != "All Categories":
        filtered_submittals = [submittal for submittal in filtered_submittals if submittal["Category"] == selected_category]
    
    # Filter by spec section
    if selected_spec != "All Spec Sections":
        filtered_submittals = [submittal for submittal in filtered_submittals if submittal["Spec_Section"] == selected_spec]
    
    # Filter by submitter
    if selected_submitter != "All Submitters":
        filtered_submittals = [submittal for submittal in filtered_submittals if submittal["Submitted_By"] == selected_submitter]
    
    # Filter by date range (submission date)
    filtered_submittals = [
        submittal for submittal in filtered_submittals 
        if start_date <= datetime.strptime(submittal["Submission_Date"], "%Y-%m-%d").date() <= end_date
    ]
    
    # Filter by search term
    if search_term:
        filtered_submittals = [submittal for submittal in filtered_submittals if 
                              search_term.lower() in submittal["ID"].lower() or
                              search_term.lower() in submittal["Title"].lower() or
                              search_term.lower() in submittal["Description"].lower()]
    
    # Layout for action buttons
    col1, col2 = st.columns([0.8, 0.2])
    
    with col1:
        # Show item count
        st.caption(f"Showing {len(filtered_submittals)} submittals")
    
    with col2:
        # Add button
        if st.button("➕ Add Submittal", use_container_width=True):
            st.session_state.submittal_view = "add"
            st.rerun()
    
    # Analysis button
    if st.button("📊 View Analysis", use_container_width=True):
        st.session_state.submittal_view = "analysis"
        st.rerun()
    
    # Check if we have any results
    if not filtered_submittals:
        st.info("No submittals match your filters.")
        return
    
    # Display the filtered submittals
    for submittal in filtered_submittals:
        # Create a container for each submittal
        submittal_container = st.container()
        
        with submittal_container:
            # Add a subtle divider between submittals
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
            
            # Create a row with columns for the submittal data and action buttons
            row_container = st.container()
            
            # Create a more balanced row layout with condensed columns
            col1, col2, col3, col4, col_actions = row_container.columns([1, 2, 2, 1.5, 0.5])
            
            with col1:
                # Status indicator
                status_color = {
                    "Pending": "⚪",
                    "Approved": "🟢",
                    "Approved as Noted": "🟡",
                    "Revise and Resubmit": "🟠",
                    "Rejected": "🔴"
                }
                
                st.write(f"{status_color.get(submittal['Status'], '⚪')} **{submittal['ID']}**")
                st.caption(f"Spec: {submittal['Spec_Section']}")
            
            with col2:
                st.write(f"**{submittal['Title']}**")
                st.caption(f"Category: {submittal['Category']}")
            
            with col3:
                # Submitted and review info
                st.write(f"**Submitted By:** {submittal['Submitted_By']}")
                if submittal['Reviewed_By']:
                    st.caption(f"Reviewed By: {submittal['Reviewed_By']}")
                else:
                    st.caption("Not yet reviewed")
            
            with col4:
                # Dates and review time
                st.write(f"**Submitted:** {submittal['Submission_Date']}")
                
                if submittal['Review_Date']:
                    st.caption(f"Reviewed: {submittal['Review_Date']} ({submittal['Review_Days']} days)")
                else:
                    # Calculate days pending
                    submission_date = datetime.strptime(submittal['Submission_Date'], "%Y-%m-%d")
                    days_pending = (datetime.now() - submission_date).days
                    st.caption(f"Pending: {days_pending} days")
            
            # Action buttons in a single column
            with col_actions:
                # Create two buttons stacked in the actions column
                if st.button("👁️", key=f"view_{submittal['ID']}", help="View submittal details"):
                    # Store submittal details in session state
                    st.session_state.selected_submittal_id = submittal['ID'] 
                    st.session_state.selected_submittal_data = submittal
                    # Set view mode
                    st.session_state["submittal_view"] = "view"
                    # Force refresh
                    st.rerun()
                
                if st.button("✏️", key=f"edit_{submittal['ID']}", help="Edit submittal"):
                    # Store submittal data for editing
                    st.session_state.edit_submittal_id = submittal['ID']
                    st.session_state.edit_submittal_data = submittal
                    # Set edit mode 
                    st.session_state["submittal_view"] = "edit"
                    # Force refresh
                    st.rerun()

def render_submittal_details():
    """Render the submittal details view (single record view)"""
    st.subheader("Submittal Details")
    
    # Ensure we have a selected submittal
    if not st.session_state.get("selected_submittal_id"):
        st.error("No submittal selected. Please select a submittal from the list.")
        # Return to list view
        st.session_state.submittal_view = "list"
        st.rerun()
        return
    
    # Get the selected submittal data
    submittal = st.session_state.get("selected_submittal_data", None)
    
    if not submittal:
        # If somehow we have an ID but no data, try to find it
        submittals = generate_sample_submittals()
        submittal = next((s for s in submittals if s["ID"] == st.session_state.selected_submittal_id), None)
        
        if not submittal:
            st.error(f"Submittal with ID {st.session_state.selected_submittal_id} not found.")
            # Return to list view
            st.session_state.submittal_view = "list"
            st.rerun()
            return
    
    # Display submittal details
    with st.container():
        # Create columns for basic info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Status indicator
            status_color = {
                "Pending": "⚪",
                "Approved": "🟢",
                "Approved as Noted": "🟡",
                "Revise and Resubmit": "🟠",
                "Rejected": "🔴"
            }
            
            status_bg_color = {
                "Pending": "#F3F4F6",      # Light gray
                "Approved": "#D1FAE5",     # Light green
                "Approved as Noted": "#FEF3C7",  # Light yellow
                "Revise and Resubmit": "#FFEDD5",  # Light orange
                "Rejected": "#FEE2E2"     # Light red
            }
            
            st.markdown(
                f"<div style='background-color: {status_bg_color.get(submittal['Status'], '#F3F4F6')}; padding: 8px; border-radius: 4px;'>"
                f"<strong>Status:</strong> {status_color.get(submittal['Status'], '⚪')} {submittal['Status']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"<div style='background-color: #F3F4F6; padding: 8px; border-radius: 4px;'>"
                f"<strong>Category:</strong> {submittal['Category']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"<div style='background-color: #F3F4F6; padding: 8px; border-radius: 4px;'>"
                f"<strong>Spec Section:</strong> {submittal['Spec_Section']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"<div style='background-color: #F3F4F6; padding: 8px; border-radius: 4px;'>"
                f"<strong>ID:</strong> {submittal['ID']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        # Title and description
        st.markdown(f"## {submittal['Title']}")
        
        st.markdown("### Description")
        st.markdown(
            f"<div style='background-color: #F9FAFB; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
            f"{submittal['Description']}"
            f"</div>",
            unsafe_allow_html=True
        )
        
        # Submission details
        st.markdown("### Submission Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Submitted By:** {submittal['Submitted_By']}")
            st.markdown(f"**Submission Date:** {submittal['Submission_Date']}")
        
        with col2:
            if submittal['Reviewed_By']:
                st.markdown(f"**Reviewed By:** {submittal['Reviewed_By']}")
                st.markdown(f"**Review Date:** {submittal['Review_Date']}")
                st.markdown(f"**Review Time:** {submittal['Review_Days']} days")
            else:
                # Calculate days pending
                submission_date = datetime.strptime(submittal['Submission_Date'], "%Y-%m-%d")
                days_pending = (datetime.now() - submission_date).days
                st.markdown(f"**Days Pending:** {days_pending} days")
                st.markdown("**Status:** Awaiting Review")
        
        # Generate random additional details for the submittal
        st.markdown("### Detailed Information")
        
        # Randomly generate shop drawing or product data
        submittal_type = random.choice(["Shop Drawing", "Product Data", "Sample", "Quality Assurance", "Test Report"])
        
        if submittal_type == "Shop Drawing":
            drawing_details = [
                "Shop drawings showing fabrication and installation details.",
                "Detailed drawings with dimensions and connections.",
                "Coordination drawings showing relationship to other work.",
                "Fabrication drawings with material specifications.",
                "Installation sequence and methodology drawings."
            ]
            
            st.markdown(f"**Submittal Type:** Shop Drawing")
            st.markdown(
                f"<div style='background-color: #F9FAFB; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(drawing_details)}"
                f"</div>",
                unsafe_allow_html=True
            )
            
        elif submittal_type == "Product Data":
            product_details = [
                "Manufacturer's product data including performance characteristics and capacities.",
                "Product specifications with material compositions and finishes.",
                "Installation instructions and recommendations.",
                "Standard product data sheet with technical information.",
                "Product certifications and compliance with standards."
            ]
            
            st.markdown(f"**Submittal Type:** Product Data")
            st.markdown(
                f"<div style='background-color: #F9FAFB; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(product_details)}"
                f"</div>",
                unsafe_allow_html=True
            )
            
        elif submittal_type == "Sample":
            sample_details = [
                "Physical sample of material finish and color.",
                "Product sample showing texture and pattern.",
                "Full-size sample of assembled component.",
                "Sample panel showing installation method.",
                "Color and texture selection samples."
            ]
            
            st.markdown(f"**Submittal Type:** Sample")
            st.markdown(
                f"<div style='background-color: #F9FAFB; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(sample_details)}"
                f"</div>",
                unsafe_allow_html=True
            )
            
        elif submittal_type == "Quality Assurance":
            qa_details = [
                "Qualification data for manufacturers and installers.",
                "Certificates showing compliance with standards.",
                "Test reports for material properties.",
                "Manufacturer's quality control procedures.",
                "Field quality-control test procedures."
            ]
            
            st.markdown(f"**Submittal Type:** Quality Assurance")
            st.markdown(
                f"<div style='background-color: #F9FAFB; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(qa_details)}"
                f"</div>",
                unsafe_allow_html=True
            )
            
        else:  # Test Report
            test_details = [
                "Independent testing agency results.",
                "Factory test reports for assembled equipment.",
                "Field test results for installed systems.",
                "Performance test data compared to specifications.",
                "Compliance test results for code requirements."
            ]
            
            st.markdown(f"**Submittal Type:** Test Report")
            st.markdown(
                f"<div style='background-color: #F9FAFB; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(test_details)}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        # Add review comments section
        st.markdown("### Review Comments")
        
        if submittal['Status'] == "Pending":
            st.info("This submittal has not been reviewed yet.")
            
        elif submittal['Status'] == "Approved":
            approved_comments = [
                "Submittal approved as submitted. Proceed with ordering/fabrication.",
                "Submittal meets all requirements of the contract documents.",
                "No exceptions taken. Proceed with work.",
                "Submittal approved. Product/material meets specifications.",
                "Submittal accepted as complying with design intent."
            ]
            
            st.markdown(
                f"<div style='background-color: #D1FAE5; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(approved_comments)}"
                f"</div>",
                unsafe_allow_html=True
            )
            
        elif submittal['Status'] == "Approved as Noted":
            noted_comments = [
                "Submittal approved with minor corrections as noted. Resubmission not required.",
                "Make noted adjustments in field installation. Proceed with work.",
                "Product acceptable with changes indicated on documents.",
                "Incorporate comments in final installation. No resubmission needed.",
                "Approved with comments. Address notes during fabrication/installation."
            ]
            
            st.markdown(
                f"<div style='background-color: #FEF3C7; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(noted_comments)}"
                f"</div>",
                unsafe_allow_html=True
            )
            
        elif submittal['Status'] == "Revise and Resubmit":
            revise_comments = [
                "Submittal does not comply with contract requirements. Revise and resubmit.",
                "Product specified is acceptable but details need revision as noted.",
                "Additional information required. Please address comments and resubmit.",
                "Dimensions/connections not coordinated with other systems. Revise and resubmit.",
                "Performance data does not meet specification requirements. Provide alternate product."
            ]
            
            st.markdown(
                f"<div style='background-color: #FFEDD5; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(revise_comments)}"
                f"</div>",
                unsafe_allow_html=True
            )
            
        elif submittal['Status'] == "Rejected":
            rejected_comments = [
                "Submittal rejected. Does not comply with contract requirements.",
                "Product/material does not meet specifications. Submit alternative product.",
                "Submittal does not demonstrate compliance with performance requirements.",
                "Rejected due to major non-compliance with design intent.",
                "Product not acceptable for this application. See specifications for requirements."
            ]
            
            st.markdown(
                f"<div style='background-color: #FEE2E2; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>"
                f"{random.choice(rejected_comments)}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        # Add attachments section (placeholder)
        st.markdown("### Attachments")
        
        # Simulate some attachments
        has_attachments = True  # Always show some attachments for submittals
        
        if has_attachments:
            attachments = [
                {"name": f"{submittal['ID']}_Specification.pdf", "type": "PDF", "size": "1.2 MB", "date": submittal['Submission_Date']},
                {"name": f"{submittal['ID']}_Product_Data.pdf", "type": "PDF", "size": "3.4 MB", "date": submittal['Submission_Date']}
            ]
            
            # Add shop drawings for certain categories
            if submittal['Category'] in ["Structural", "Mechanical", "Electrical"]:
                attachments.append({"name": f"{submittal['ID']}_Shop_Drawings.pdf", "type": "PDF", "size": "5.6 MB", "date": submittal['Submission_Date']})
            
            # Add samples for certain categories
            if submittal['Category'] in ["Architectural", "Finishes"]:
                attachments.append({"name": f"{submittal['ID']}_Samples.jpg", "type": "Image", "size": "2.3 MB", "date": submittal['Submission_Date']})
            
            # Add review comments if reviewed
            if submittal['Review_Date']:
                attachments.append({"name": f"{submittal['ID']}_Review_Comments.pdf", "type": "PDF", "size": "0.8 MB", "date": submittal['Review_Date']})
            
            # Create a DataFrame for the attachments
            df_attachments = pd.DataFrame(attachments)
            
            # Display the attachments
            st.dataframe(df_attachments, use_container_width=True)
        
        # Add transmittal section
        st.markdown("### Transmittal Information")
        
        transmittal_id = f"TR-{submittal['ID'][4:]}"
        transmittal_date = submittal['Submission_Date']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Transmittal ID:** {transmittal_id}")
            st.markdown(f"**Transmittal Date:** {transmittal_date}")
        
        with col2:
            st.markdown(f"**From:** {submittal['Submitted_By']}")
            st.markdown(f"**To:** {submittal['Reviewed_By'] or 'Design Team'}")
        
        with col3:
            st.markdown(f"**Delivery Method:** Electronic")
            st.markdown(f"**Number of Copies:** 1")
        
        # Action buttons at the bottom
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Edit Submittal", use_container_width=True):
                st.session_state.edit_submittal_id = submittal['ID']
                st.session_state.edit_submittal_data = submittal
                st.session_state.submittal_view = "edit"
                st.rerun()
        
        with col2:
            if st.button("📊 View Analysis", use_container_width=True):
                st.session_state.submittal_view = "analysis"
                st.rerun()

def render_submittal_form(is_edit=False):
    """Render the submittal creation/edit form"""
    if is_edit:
        st.subheader("Edit Submittal")
        # Ensure we have a submittal to edit
        if not st.session_state.get("edit_submittal_id"):
            st.error("No submittal selected for editing. Please select a submittal from the list.")
            # Return to list view
            st.session_state.submittal_view = "list"
            st.rerun()
            return
        
        # Get the submittal data for editing
        submittal = st.session_state.get("edit_submittal_data", {})
    else:
        st.subheader("Create New Submittal")
        # Initialize empty submittal for new entries
        submittal = {
            "ID": f"SUB-{random.randint(100, 999)}",
            "Title": "",
            "Description": "",
            "Category": "",
            "Spec_Section": "",
            "Status": "Pending",
            "Submission_Date": datetime.now().strftime("%Y-%m-%d"),
            "Review_Date": "",
            "Review_Days": None,
            "Submitted_By": "",
            "Reviewed_By": ""
        }
    
    # Create the form
    with st.form(key="submittal_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            # For display only in edit mode
            if is_edit:
                st.text_input("Submittal ID", value=submittal.get("ID", ""), disabled=True)
            
            title = st.text_input("Title *", value=submittal.get("Title", ""))
            
            # Categories
            categories = ["Mechanical", "Electrical", "Structural", "Architectural", "Plumbing", "Civil", "Finishes"]
            
            # Find index of selected category if editing
            category_index = 0
            if is_edit and submittal.get("Category") in categories:
                category_index = categories.index(submittal.get("Category"))
            
            selected_category = st.selectbox(
                "Category *",
                categories,
                index=category_index
            )
        
        with col2:
            spec_section = st.text_input(
                "Specification Section *",
                value=submittal.get("Spec_Section", ""),
                placeholder="e.g., 09 2900"
            )
            
            # Status options
            statuses = ["Pending", "Approved", "Approved as Noted", "Revise and Resubmit", "Rejected"]
            
            # Find index of selected status if editing
            status_index = statuses.index("Pending")  # Default to Pending
            if is_edit and submittal.get("Status") in statuses:
                status_index = statuses.index(submittal.get("Status"))
            
            selected_status = st.selectbox(
                "Status *",
                statuses,
                index=status_index
            )
        
        # Description
        st.subheader("Description")
        description = st.text_area(
            "Description *",
            value=submittal.get("Description", ""),
            height=100,
            placeholder="Provide a description of the submittal..."
        )
        
        # Submittal type
        submittal_types = ["Shop Drawing", "Product Data", "Sample", "Quality Assurance", "Test Report"]
        
        # Find index of selected type if editing
        type_index = 0
        if is_edit and submittal.get("Submittal_Type") in submittal_types:
            type_index = submittal_types.index(submittal.get("Submittal_Type"))
        
        selected_type = st.selectbox(
            "Submittal Type *",
            submittal_types,
            index=type_index
        )
        
        # Submission details
        st.subheader("Submission Details")
        col1, col2 = st.columns(2)
        
        with col1:
            submitted_by = st.text_input(
                "Submitted By *",
                value=submittal.get("Submitted_By", ""),
                placeholder="Name of person/company submitting"
            )
            
            submission_date = st.date_input(
                "Submission Date *",
                value=datetime.strptime(submittal.get("Submission_Date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        with col2:
            # Only show review information if status is not Pending
            if selected_status != "Pending":
                reviewed_by = st.text_input(
                    "Reviewed By *",
                    value=submittal.get("Reviewed_By", ""),
                    placeholder="Name of person/company reviewing"
                )
                
                review_date_value = None
                if submittal.get("Review_Date"):
                    review_date_value = datetime.strptime(submittal.get("Review_Date"), "%Y-%m-%d")
                else:
                    review_date_value = datetime.now()
                
                review_date = st.date_input(
                    "Review Date *",
                    value=review_date_value
                )
            else:
                reviewed_by = ""
                review_date = None
        
        # Review comments (only show if status is not Pending)
        if selected_status != "Pending":
            st.subheader("Review Comments")
            review_comments = st.text_area(
                "Review Comments *",
                value=submittal.get("Review_Comments", ""),
                height=100,
                placeholder="Provide review comments..."
            )
        else:
            review_comments = ""
        
        # Attachments
        st.subheader("Attachments")
        uploaded_files = st.file_uploader("Upload Attachments", accept_multiple_files=True)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "Save Submittal" if is_edit else "Create Submittal",
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
        
        if not spec_section:
            st.error("Please enter a specification section.")
            return
        
        if not submitted_by:
            st.error("Please enter who submitted this submittal.")
            return
        
        # Additional validation for reviewed submittals
        if selected_status != "Pending":
            if not reviewed_by:
                st.error("Please enter who reviewed this submittal.")
                return
            
            if not review_comments:
                st.error("Please enter review comments.")
                return
        
        # Calculate review days if provided
        review_days = None
        if review_date and selected_status != "Pending":
            review_days = (review_date - submission_date).days
        
        # In a real app, this would save to database
        if is_edit:
            st.success(f"Submittal {submittal['ID']} updated successfully!")
        else:
            st.success(f"New submittal created successfully!")
        
        # Return to list view
        st.session_state.submittal_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to previous view
        if is_edit and st.session_state.get("selected_submittal_id") == st.session_state.get("edit_submittal_id"):
            # If editing from detail view, return to detail view
            st.session_state.submittal_view = "view"
        else:
            # Otherwise return to list view
            st.session_state.submittal_view = "list"
        
        st.rerun()

def render_submittal_analysis():
    """Render the submittal analysis view with charts and metrics"""
    st.subheader("Submittal Analysis")
    
    # Get sample data
    submittals = generate_sample_submittals()
    
    # Calculate summary metrics
    total_submittals = len(submittals)
    pending_submittals = sum(1 for submittal in submittals if submittal["Status"] == "Pending")
    approved_submittals = sum(1 for submittal in submittals if submittal["Status"] in ["Approved", "Approved as Noted"])
    rejected_submittals = sum(1 for submittal in submittals if submittal["Status"] in ["Revise and Resubmit", "Rejected"])
    
    # Calculate average review time
    review_times = [submittal["Review_Days"] for submittal in submittals if submittal["Review_Days"] is not None]
    avg_review_time = sum(review_times) / len(review_times) if review_times else 0
    
    # Summary metrics in a nice grid
    st.subheader("Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Submittals", f"{total_submittals}")
    
    with col2:
        st.metric("Pending", f"{pending_submittals}", delta=f"{pending_submittals/total_submittals:.0%}")
    
    with col3:
        st.metric("Approved", f"{approved_submittals}", delta=f"{approved_submittals/total_submittals:.0%}")
    
    with col4:
        st.metric("Avg. Review Time", f"{avg_review_time:.1f} days")
    
    # Create tabs for different analysis views
    tab1, tab2, tab3 = st.tabs(["Status Analysis", "Category Analysis", "Review Times"])
    
    # Tab 1: Status Analysis
    with tab1:
        # Status breakdown
        status_counts = {}
        for submittal in submittals:
            status = submittal["Status"]
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
            title='Submittal Status Distribution',
            color='Status',
            color_discrete_map={
                'Pending': '#9CA3AF',       # Gray
                'Approved': '#10B981',      # Green
                'Approved as Noted': '#FBBF24',  # Yellow
                'Revise and Resubmit': '#F59E0B',  # Amber
                'Rejected': '#EF4444'       # Red
            }
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Status over time
        st.subheader("Submittal Status Over Time")
        
        # Prepare data for status over time
        status_dates = []
        for submittal in submittals:
            status_dates.append({
                'Date': datetime.strptime(submittal['Submission_Date'], "%Y-%m-%d"),
                'Status': submittal['Status']
            })
        
        # Create DataFrame
        status_date_df = pd.DataFrame(status_dates)
        
        # Group by week and status
        status_date_df['Week'] = status_date_df['Date'].dt.isocalendar().week
        status_date_df['Year'] = status_date_df['Date'].dt.isocalendar().year
        
        # Create a week-year string for sorting
        status_date_df['Week_Year'] = status_date_df['Year'].astype(str) + '-' + status_date_df['Week'].astype(str).str.zfill(2)
        
        # Group by week and status
        status_by_week = status_date_df.groupby(['Week_Year', 'Status']).size().reset_index(name='Count')
        
        # Pivot the data for stacked bar chart
        status_pivot = status_by_week.pivot(index='Week_Year', columns='Status', values='Count').fillna(0)
        
        # Reindex to ensure all statuses are included
        all_statuses = ['Pending', 'Approved', 'Approved as Noted', 'Revise and Resubmit', 'Rejected']
        status_pivot = status_pivot.reindex(columns=all_statuses, fill_value=0)
        
        # Create stacked bar chart
        fig = px.bar(
            status_pivot, 
            barmode='stack',
            title='Submittal Status by Week',
            color_discrete_map={
                'Pending': '#9CA3AF',       # Gray
                'Approved': '#10B981',      # Green
                'Approved as Noted': '#FBBF24',  # Yellow
                'Revise and Resubmit': '#F59E0B',  # Amber
                'Rejected': '#EF4444'       # Red
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Category Analysis
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Category breakdown
            category_counts = {}
            for submittal in submittals:
                category = submittal["Category"]
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
                x='Category', 
                y='Count',
                title='Submittal Category Distribution',
                color='Count',
                color_continuous_scale=px.colors.sequential.Viridis
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category by status
            category_status = []
            for submittal in submittals:
                category_status.append({
                    'Category': submittal['Category'],
                    'Status': submittal['Status']
                })
            
            # Create DataFrame
            cs_df = pd.DataFrame(category_status)
            
            # Create a crosstab
            category_status_pivot = pd.crosstab(cs_df['Category'], cs_df['Status'])
            
            # Create stacked bar chart
            fig = px.bar(
                category_status_pivot, 
                barmode='stack',
                title='Submittal Status by Category',
                color_discrete_map={
                    'Pending': '#9CA3AF',       # Gray
                    'Approved': '#10B981',      # Green
                    'Approved as Noted': '#FBBF24',  # Yellow
                    'Revise and Resubmit': '#F59E0B',  # Amber
                    'Rejected': '#EF4444'       # Red
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Calculate approval rates by category
        st.subheader("Approval Rates by Category")
        
        # Prepare data
        approval_rates = []
        for category in category_counts.keys():
            # Filter submittals for this category
            category_submittals = [s for s in submittals if s['Category'] == category]
            total_reviewed = sum(1 for s in category_submittals if s['Status'] != 'Pending')
            
            if total_reviewed > 0:
                approved = sum(1 for s in category_submittals if s['Status'] in ['Approved', 'Approved as Noted'])
                approval_rate = approved / total_reviewed
                
                approval_rates.append({
                    'Category': category,
                    'Approval Rate': approval_rate,
                    'Total Reviewed': total_reviewed
                })
        
        # Create DataFrame
        approval_df = pd.DataFrame(approval_rates)
        
        # Sort by approval rate
        approval_df = approval_df.sort_values('Approval Rate', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            approval_df, 
            x='Category', 
            y='Approval Rate',
            title='Approval Rate by Category',
            color='Approval Rate',
            color_continuous_scale=px.colors.sequential.RdYlGn,
            text_auto='.0%'
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(yaxis_tickformat='.0%')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Review Times Analysis
    with tab3:
        # Prepare data for review time analysis
        review_time_data = []
        for submittal in submittals:
            if submittal["Review_Days"] is not None:
                review_time_data.append({
                    'ID': submittal['ID'],
                    'Category': submittal['Category'],
                    'Status': submittal['Status'],
                    'Review_Days': submittal['Review_Days']
                })
        
        # Convert to DataFrame
        rt_df = pd.DataFrame(review_time_data)
        
        if not rt_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Average review time by category
                avg_by_category = rt_df.groupby('Category')['Review_Days'].mean().reset_index()
                
                # Sort by review time
                avg_by_category = avg_by_category.sort_values('Review_Days', ascending=False)
                
                # Create bar chart
                fig = px.bar(
                    avg_by_category, 
                    x='Category', 
                    y='Review_Days',
                    title='Avg. Review Time by Category (Days)',
                    color='Review_Days',
                    color_continuous_scale=px.colors.sequential.Viridis
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Average review time by status
                avg_by_status = rt_df.groupby('Status')['Review_Days'].mean().reset_index()
                
                # Create bar chart
                fig = px.bar(
                    avg_by_status, 
                    x='Status', 
                    y='Review_Days',
                    title='Avg. Review Time by Status (Days)',
                    color='Status',
                    color_discrete_map={
                        'Approved': '#10B981',      # Green
                        'Approved as Noted': '#FBBF24',  # Yellow
                        'Revise and Resubmit': '#F59E0B',  # Amber
                        'Rejected': '#EF4444'       # Red
                    }
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Review time distribution
            fig = px.histogram(
                rt_df, 
                x='Review_Days',
                nbins=15,
                title='Review Time Distribution (Days)',
                color_discrete_sequence=['#3B82F6']  # Blue
            )
            
            # Add a vertical line for the average
            fig.add_vline(
                x=avg_review_time,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Avg: {avg_review_time:.1f} days",
                annotation_position="top right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No review time data available for analysis.")
    
    # Submittal trends over time
    st.subheader("Submittal Trends")
    
    # Prepare data for trend analysis
    trend_data = []
    for submittal in submittals:
        submission_date = datetime.strptime(submittal["Submission_Date"], "%Y-%m-%d")
        trend_data.append({
            'Date': submission_date,
            'Type': 'Submitted',
            'Count': 1
        })
        
        if submittal["Review_Date"]:
            review_date = datetime.strptime(submittal["Review_Date"], "%Y-%m-%d")
            trend_data.append({
                'Date': review_date,
                'Type': 'Reviewed',
                'Count': 1
            })
    
    # Convert to DataFrame
    trend_df = pd.DataFrame(trend_data)
    
    # Group by date and type
    trend_by_date = trend_df.groupby([pd.Grouper(key='Date', freq='W'), 'Type'])['Count'].sum().reset_index()
    
    # Create cumulative sums
    submitted_cum = trend_by_date[trend_by_date['Type'] == 'Submitted'].sort_values('Date')
    submitted_cum['Cumulative'] = submitted_cum['Count'].cumsum()
    
    reviewed_cum = trend_by_date[trend_by_date['Type'] == 'Reviewed'].sort_values('Date')
    if not reviewed_cum.empty:
        reviewed_cum['Cumulative'] = reviewed_cum['Count'].cumsum()
    
    # Create the figure
    fig = go.Figure()
    
    # Add submitted line
    fig.add_trace(go.Scatter(
        x=submitted_cum['Date'],
        y=submitted_cum['Cumulative'],
        mode='lines+markers',
        name='Submittals Received',
        line=dict(color='#3B82F6', width=2)  # Blue
    ))
    
    # Add reviewed line if we have data
    if not reviewed_cum.empty:
        fig.add_trace(go.Scatter(
            x=reviewed_cum['Date'],
            y=reviewed_cum['Cumulative'],
            mode='lines+markers',
            name='Submittals Reviewed',
            line=dict(color='#10B981', width=2)  # Green
        ))
    
    # Layout
    fig.update_layout(
        title='Cumulative Submittals Over Time',
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