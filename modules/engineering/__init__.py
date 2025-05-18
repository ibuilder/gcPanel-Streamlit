"""
Engineering module for the gcPanel Construction Management Dashboard.

This module provides management for Requests for Information (RFIs) and Submittals,
which are critical for engineering coordination on construction projects.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.express as px
from enum import Enum, auto

# Import form components
from components.engineering_forms import rfi_form, submittal_form

# Enums for status types
class SubmittalStatus(Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    APPROVED_AS_NOTED = "Approved as Noted"
    REVISE_AND_RESUBMIT = "Revise and Resubmit"
    REJECTED = "Rejected"
    
class RfiStatus(Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    ANSWERED = "Answered"
    CLOSED = "Closed"
    OVERDUE = "Overdue"

def render_engineering():
    """Render the engineering module"""
    
    # Header
    st.title("Engineering")
    
    # Tab navigation for engineering sections
    tab1, tab2 = st.tabs(["RFIs", "Submittals"])
    
    # RFIs Tab
    with tab1:
        render_rfis()
    
    # Submittals Tab
    with tab2:
        render_submittals()

def render_rfis():
    """Render the RFIs (Requests for Information) section"""
    
    # Header with Create RFI button at the top
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.header("Requests for Information (RFIs)")
    
    with col3:
        if st.button("Create New RFI", type="primary", key="create_new_rfi_button", use_container_width=True):
            st.session_state.show_rfi_form = True
            st.session_state.edit_rfi_id = None
    
    # RFI creation/edit form
    if st.session_state.get("show_rfi_form", False):
        # Get RFI data if editing
        rfi_to_edit = None
        if st.session_state.get("edit_rfi_id"):
            rfi_to_edit = next((rfi for rfi in rfis if rfi.get("id") == st.session_state.get("edit_rfi_id")), None)
        
        # Use the enhanced form component
        form_submitted, form_data = rfi_form(
            is_edit=st.session_state.get("edit_rfi_id") is not None,
            rfi_data=rfi_to_edit
        )
        
        if form_submitted and form_data:
            # In a real app, this would save to database
            
            # Update or create RFI
            if st.session_state.get("edit_rfi_id"):
                # Update existing RFI
                for i, rfi in enumerate(rfis):
                    if rfi["id"] == st.session_state.get("edit_rfi_id"):
                        # Preserve ID and other metadata
                        form_data["id"] = rfi["id"]
                        form_data["number"] = rfi["number"]
                        form_data["submitted_date"] = datetime.now()
                        rfis[i].update(form_data)
                        break
                st.success("RFI updated successfully!")
            else:
                # Add new RFI to the list
                new_rfi = {
                    "id": f"RFI-{len(rfis) + 1:03d}",
                    "number": len(rfis) + 1,
                    "title": form_data["title"],
                    "description": form_data["description"],
                    "discipline": form_data["discipline"],
                    "location": form_data["location"],
                    "submitted_by": form_data["submitted_by"],
                    "submitted_date": datetime.now(),
                    "due_date": form_data["due_date"],
                    "status": form_data["status"],
                    "responsible": form_data["responsible"],
                    "response": None,
                    "response_date": None,
                    "closed_date": None,
                    "attachments": len(form_data.get("attachments", [])),
                    "cost_impact": form_data["cost_impact"],
                    "schedule_impact": form_data["schedule_impact"],
                    "priority": form_data["priority"]
                }
                rfis.insert(0, new_rfi)  # Add to beginning of list
                st.success(f"RFI {form_data['status'].lower()} successfully!")
            
            # Reset form state
            st.session_state.show_rfi_form = False
            st.session_state.edit_rfi_id = None
            
            # Force rerender
            st.rerun()
            
    # Define sample data
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
    
    # Generate sample RFIs
    rfis = []
    for i in range(1, 31):
        # Generate dates with realistic workflow
        submitted_date = datetime.now() - timedelta(days=random.randint(5, 90))
        
        # Determine status based on realistic workflow and timing
        days_since_submission = (datetime.now() - submitted_date).days
        
        if days_since_submission < 3:
            # Recently submitted
            status = random.choices(
                [RfiStatus.DRAFT.value, RfiStatus.SUBMITTED.value, RfiStatus.UNDER_REVIEW.value],
                weights=[0.2, 0.4, 0.4],
                k=1
            )[0]
            response_date = None
            closed_date = None
        elif days_since_submission < 7:
            # In progress
            status = random.choices(
                [RfiStatus.UNDER_REVIEW.value, RfiStatus.ANSWERED.value, RfiStatus.OVERDUE.value],
                weights=[0.4, 0.4, 0.2],
                k=1
            )[0]
            
            if status == RfiStatus.ANSWERED.value:
                response_date = submitted_date + timedelta(days=random.randint(1, 5))
                closed_date = response_date + timedelta(days=random.randint(0, 2))
            else:
                response_date = None
                closed_date = None
        else:
            # Older RFIs should be mostly resolved
            status = random.choices(
                [RfiStatus.UNDER_REVIEW.value, RfiStatus.ANSWERED.value, RfiStatus.CLOSED.value, RfiStatus.OVERDUE.value],
                weights=[0.1, 0.3, 0.5, 0.1],
                k=1
            )[0]
            
            if status in [RfiStatus.ANSWERED.value, RfiStatus.CLOSED.value]:
                response_date = submitted_date + timedelta(days=random.randint(3, 10))
                
                if status == RfiStatus.CLOSED.value:
                    closed_date = response_date + timedelta(days=random.randint(1, 5))
                else:
                    closed_date = None
            else:
                response_date = None
                closed_date = None
        
        # RFI due date
        due_date = submitted_date + timedelta(days=random.randint(7, 14))
        
        # Calculate if overdue
        if status not in [RfiStatus.ANSWERED.value, RfiStatus.CLOSED.value] and due_date < datetime.now():
            status = RfiStatus.OVERDUE.value
        
        # Create RFI
        rfis.append({
            "id": f"RFI-{i:03d}",
            "number": i,
            "title": f"RFI {i}: {random.choice(['Clarification', 'Conflict', 'Omission', 'Change Request'])} - {random.choice(disciplines)}",
            "description": f"Request for information regarding {random.choice(['details', 'specifications', 'conflicts', 'coordination', 'design intent'])}.",
            "discipline": random.choice(disciplines),
            "location": random.choice(locations),
            "submitted_by": random.choice(["Project Manager", "Site Supervisor", "Project Engineer", "Subcontractor"]),
            "submitted_date": submitted_date,
            "due_date": due_date,
            "status": status,
            "responsible": random.choice(responsibles),
            "response": "Response provided by the design team." if status in [RfiStatus.ANSWERED.value, RfiStatus.CLOSED.value] else None,
            "response_date": response_date,
            "closed_date": closed_date,
            "attachments": random.randint(0, 3),
            "cost_impact": random.choice([True, False]),
            "schedule_impact": random.choice([True, False]),
            "priority": random.choice(["Low", "Medium", "High", "Critical"])
        })
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Status",
            [status.value for status in RfiStatus],
            default=[RfiStatus.DRAFT.value, RfiStatus.SUBMITTED.value, RfiStatus.UNDER_REVIEW.value, RfiStatus.OVERDUE.value],
            key="rfi_status_filter"
        )
    
    with col2:
        discipline_filter = st.multiselect(
            "Discipline",
            disciplines,
            default=[],
            key="rfi_discipline_filter"
        )
    
    with col3:
        priority_filter = st.multiselect(
            "Priority",
            ["Low", "Medium", "High", "Critical"],
            default=["High", "Critical"],
            key="rfi_priority_filter"
        )
    
    # Apply filters
    filtered_rfis = [rfi for rfi in rfis if rfi["status"] in status_filter]
    
    if discipline_filter:
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["discipline"] in discipline_filter]
    
    if priority_filter:
        filtered_rfis = [rfi for rfi in filtered_rfis if rfi["priority"] in priority_filter]
    
    # RFI metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_rfis = len(rfis)
        st.metric("Total RFIs", total_rfis)
    
    with metrics_col2:
        open_rfis = len([rfi for rfi in rfis if rfi["status"] in [RfiStatus.DRAFT.value, RfiStatus.SUBMITTED.value, RfiStatus.UNDER_REVIEW.value, RfiStatus.OVERDUE.value]])
        st.metric("Open RFIs", open_rfis)
    
    with metrics_col3:
        overdue_rfis = len([rfi for rfi in rfis if rfi["status"] == RfiStatus.OVERDUE.value])
        st.metric("Overdue", overdue_rfis)
    
    with metrics_col4:
        avg_response_time = 0
        response_times = []
        
        for rfi in rfis:
            if rfi["response_date"] and rfi["submitted_date"]:
                response_time = (rfi["response_date"] - rfi["submitted_date"]).days
                response_times.append(response_time)
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
        
        st.metric("Avg. Response Time", f"{avg_response_time:.1f} days")
    
    # Visualizations
    st.subheader("RFI Analysis")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Status distribution
        status_counts = {}
        for rfi in rfis:
            status = rfi["status"]
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
        
        # Create data for chart
        status_df = pd.DataFrame({
            "Status": list(status_counts.keys()),
            "Count": list(status_counts.values())
        })
        
        # Color map
        color_map = {
            RfiStatus.DRAFT.value: "#6c757d",      # Gray
            RfiStatus.SUBMITTED.value: "#ffc107",  # Yellow
            RfiStatus.UNDER_REVIEW.value: "#17a2b8", # Cyan
            RfiStatus.ANSWERED.value: "#28a745",   # Green
            RfiStatus.CLOSED.value: "#20c997",     # Teal
            RfiStatus.OVERDUE.value: "#dc3545"     # Red
        }
        
        # Create pie chart
        fig = px.pie(
            status_df,
            values="Count",
            names="Status",
            title="RFI Status Distribution",
            color="Status",
            color_discrete_map=color_map
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with viz_col2:
        # Discipline distribution
        discipline_counts = {}
        for rfi in rfis:
            discipline = rfi["discipline"]
            if discipline not in discipline_counts:
                discipline_counts[discipline] = 0
            discipline_counts[discipline] += 1
        
        # Create data for chart
        discipline_df = pd.DataFrame({
            "Discipline": list(discipline_counts.keys()),
            "Count": list(discipline_counts.values())
        }).sort_values("Count", ascending=False)
        
        # Create bar chart
        fig = px.bar(
            discipline_df,
            x="Discipline",
            y="Count",
            title="RFIs by Discipline",
            color="Count",
            color_continuous_scale="Viridis"
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # RFI List
    st.subheader("RFI List")
    
    # Sort by status priority and due date
    def get_status_priority(status):
        priority_order = {
            RfiStatus.OVERDUE.value: 0,
            RfiStatus.SUBMITTED.value: 1,
            RfiStatus.UNDER_REVIEW.value: 2,
            RfiStatus.DRAFT.value: 3,
            RfiStatus.ANSWERED.value: 4,
            RfiStatus.CLOSED.value: 5
        }
        return priority_order.get(status, 99)
    
    filtered_rfis.sort(key=lambda x: (get_status_priority(x["status"]), x["due_date"]))
    
    for rfi in filtered_rfis:
        # Get status color
        if rfi["status"] == RfiStatus.DRAFT.value:
            status_color = "#6c757d"  # Gray
        elif rfi["status"] == RfiStatus.SUBMITTED.value:
            status_color = "#ffc107"  # Yellow
        elif rfi["status"] == RfiStatus.UNDER_REVIEW.value:
            status_color = "#17a2b8"  # Cyan
        elif rfi["status"] == RfiStatus.ANSWERED.value:
            status_color = "#28a745"  # Green
        elif rfi["status"] == RfiStatus.CLOSED.value:
            status_color = "#20c997"  # Teal
        else:  # OVERDUE
            status_color = "#dc3545"  # Red
        
        # Get priority indicator
        if rfi["priority"] == "Critical":
            priority_color = "#dc3545"  # Red
            priority_icon = "🔴"
        elif rfi["priority"] == "High":
            priority_color = "#fd7e14"  # Orange
            priority_icon = "🟠"
        elif rfi["priority"] == "Medium":
            priority_color = "#ffc107"  # Yellow
            priority_icon = "🟡"
        else:  # Low
            priority_color = "#28a745"  # Green
            priority_icon = "🟢"
        
        # RFI card
        with st.expander(f"{priority_icon} {rfi['id']} - {rfi['title']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{rfi['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Discipline:** {rfi['discipline']}")
                st.markdown(f"**Location:** {rfi['location']}")
                st.markdown(f"**Submitted By:** {rfi['submitted_by']}")
                st.markdown(f"**Submitted Date:** {rfi['submitted_date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Priority:** <span style='color: {priority_color}; font-weight: bold;'>{rfi['priority']}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Due Date:** {rfi['due_date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Responsible:** {rfi['responsible']}")
                
                if rfi["response_date"]:
                    st.markdown(f"**Response Date:** {rfi['response_date'].strftime('%Y-%m-%d')}")
                
                if rfi["closed_date"]:
                    st.markdown(f"**Closed Date:** {rfi['closed_date'].strftime('%Y-%m-%d')}")
                
                st.markdown(f"**Attachments:** {rfi['attachments']}")
                
                if rfi["cost_impact"]:
                    st.markdown("**Cost Impact:** Yes")
                
                if rfi["schedule_impact"]:
                    st.markdown("**Schedule Impact:** Yes")
            
            st.markdown("### Description")
            st.markdown(rfi["description"])
            
            if rfi["response"]:
                st.markdown("### Response")
                st.markdown(rfi["response"])
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)
            
            with buttons_col1:
                if rfi["status"] == RfiStatus.DRAFT.value:
                    st.button("Submit", key=f"submit_rfi_{rfi['id']}")
                elif rfi["status"] in [RfiStatus.SUBMITTED.value, RfiStatus.UNDER_REVIEW.value, RfiStatus.OVERDUE.value]:
                    st.button("Add Response", key=f"respond_rfi_{rfi['id']}")
                elif rfi["status"] == RfiStatus.ANSWERED.value:
                    st.button("Close RFI", key=f"close_rfi_{rfi['id']}")
            
            with buttons_col2:
                if st.button("Edit", key=f"edit_rfi_{rfi['id']}"):
                    st.session_state.edit_rfi_id = rfi["id"]
                    st.session_state.show_rfi_form = True
                    st.rerun()
            
            with buttons_col3:
                st.button("View Attachments", key=f"attach_rfi_{rfi['id']}")
    
    # Create RFI button with action buttons in a row
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Create New RFI", type="primary", key="create_rfi_btn", use_container_width=True):
            # Initialize form state
            st.session_state.show_rfi_form = True
            st.session_state.edit_rfi_id = None
    
    # RFI creation/edit form
    if st.session_state.get("show_rfi_form", False):
        # Get RFI data if editing
        rfi_to_edit = None
        if st.session_state.get("edit_rfi_id"):
            rfi_to_edit = next((rfi for rfi in rfis if rfi.get("id") == st.session_state.get("edit_rfi_id")), None)
        
        # Use the enhanced form component
        form_submitted, form_data = rfi_form(
            is_edit=st.session_state.get("edit_rfi_id") is not None,
            rfi_data=rfi_to_edit
        )
        
        if form_submitted and form_data:
            # In a real app, this would save to database
            
            # Update or create RFI
            if st.session_state.get("edit_rfi_id"):
                # Update existing RFI
                for i, rfi in enumerate(rfis):
                    if rfi["id"] == st.session_state.get("edit_rfi_id"):
                        # Preserve ID and other metadata
                        form_data["id"] = rfi["id"]
                        form_data["number"] = rfi["number"]
                        form_data["submitted_date"] = datetime.now()
                        rfis[i].update(form_data)
                        break
                st.success("RFI updated successfully!")
            else:
                # Add new RFI to the list
                new_rfi = {
                    "id": f"RFI-{len(rfis) + 1:03d}",
                    "number": len(rfis) + 1,
                    "title": form_data["title"],
                    "description": form_data["description"],
                    "discipline": form_data["discipline"],
                    "location": form_data["location"],
                    "submitted_by": form_data["submitted_by"],
                    "submitted_date": datetime.now(),
                    "due_date": form_data["due_date"],
                    "status": form_data["status"],
                    "responsible": form_data["responsible"],
                    "response": None,
                    "response_date": None,
                    "closed_date": None,
                    "attachments": len(form_data.get("attachments", [])),
                    "cost_impact": form_data["cost_impact"],
                    "schedule_impact": form_data["schedule_impact"],
                    "priority": form_data["priority"]
                }
                rfis.insert(0, new_rfi)  # Add to beginning of list
                st.success(f"RFI {form_data['status'].lower()} successfully!")
            
            # Reset form state
            st.session_state.show_rfi_form = False
            st.session_state.edit_rfi_id = None
            
            # Force rerender
            st.rerun()

def render_submittals():
    """Render the submittals section"""
    
    st.header("Submittals")
    
    # Sample data for submittals
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
    
    # Generate sample submittals
    submittals = []
    for i in range(1, 41):
        # Select random section
        section_index = min(i // 3, len(specification_sections) - 1)  # Distribute somewhat evenly
        section = specification_sections[section_index]
        
        # Determine submitting party based on section
        section_discipline = section.split(" - ")[1].split(" ")[0]
        submitting_party = next((party for party in submitting_parties if section_discipline.lower() in party.lower()), submitting_parties[0])
        
        # Submittal type based on section
        if "Concrete" in section or "Masonry" in section or "Steel" in section:
            submittal_type = random.choice(["Product Data", "Shop Drawings", "Material Samples", "Mix Designs"])
        elif "Door" in section or "Hardware" in section or "Fixtures" in section or "Lighting" in section:
            submittal_type = random.choice(["Product Data", "Shop Drawings", "Samples", "Cut Sheets"])
        elif "Insulation" in section or "Roofing" in section or "Gypsum" in section or "Painting" in section:
            submittal_type = random.choice(["Product Data", "Material Samples", "Certificates"])
        else:
            submittal_type = random.choice(["Product Data", "Shop Drawings", "Samples", "Certificates", "Test Reports"])
        
        # Generate dates with realistic workflow
        submission_date = datetime.now() - timedelta(days=random.randint(5, 120))
        
        # Determine status based on age
        days_since_submission = (datetime.now() - submission_date).days
        
        if days_since_submission < 5:
            # Recently submitted
            status = random.choices(
                [SubmittalStatus.DRAFT.value, SubmittalStatus.SUBMITTED.value, SubmittalStatus.UNDER_REVIEW.value],
                weights=[0.2, 0.4, 0.4],
                k=1
            )[0]
            review_date = None
        elif days_since_submission < 15:
            # In progress
            status = random.choices(
                [SubmittalStatus.UNDER_REVIEW.value, SubmittalStatus.APPROVED.value, SubmittalStatus.APPROVED_AS_NOTED.value, SubmittalStatus.REVISE_AND_RESUBMIT.value],
                weights=[0.3, 0.3, 0.3, 0.1],
                k=1
            )[0]
            
            if status != SubmittalStatus.UNDER_REVIEW.value:
                review_date = submission_date + timedelta(days=random.randint(3, 12))
            else:
                review_date = None
        else:
            # Older submittals
            status = random.choices(
                [SubmittalStatus.APPROVED.value, SubmittalStatus.APPROVED_AS_NOTED.value, SubmittalStatus.REVISE_AND_RESUBMIT.value, SubmittalStatus.REJECTED.value],
                weights=[0.5, 0.3, 0.15, 0.05],
                k=1
            )[0]
            review_date = submission_date + timedelta(days=random.randint(5, 15))
        
        # Generate due date
        due_date = submission_date + timedelta(days=random.randint(10, 30))
        
        # Create submittal
        submittals.append({
            "id": f"SUBM-{i:03d}",
            "number": f"{section.split(' ')[0]}-{i:02d}",
            "title": f"Submittal for {section.split(' - ')[1]}",
            "description": f"{submittal_type} for {section.split(' - ')[1]}",
            "spec_section": section,
            "submittal_type": submittal_type,
            "submitting_party": submitting_party,
            "reviewing_party": random.choice(reviewing_parties),
            "submission_date": submission_date,
            "due_date": due_date,
            "review_date": review_date,
            "status": status,
            "revision": random.randint(0, 2),
            "comments": "Review comments from design team." if status in [SubmittalStatus.APPROVED_AS_NOTED.value, SubmittalStatus.REVISE_AND_RESUBMIT.value] else None,
            "attachments": random.randint(1, 5),
            "days_to_respond": (review_date - submission_date).days if review_date else None,
            "priority": random.choice(["Low", "Medium", "High"])
        })
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Status",
            [status.value for status in SubmittalStatus],
            default=[SubmittalStatus.DRAFT.value, SubmittalStatus.SUBMITTED.value, SubmittalStatus.UNDER_REVIEW.value],
            key="submittal_status_filter"
        )
    
    with col2:
        type_filter = st.multiselect(
            "Type",
            ["Product Data", "Shop Drawings", "Samples", "Certificates", "Test Reports", "Mix Designs", "Cut Sheets"],
            default=[],
            key="submittal_type_filter"
        )
    
    with col3:
        priority_filter = st.multiselect(
            "Priority",
            ["Low", "Medium", "High"],
            default=[],
            key="submittal_priority_filter"
        )
    
    # Apply filters
    filtered_submittals = [s for s in submittals if s["status"] in status_filter]
    
    if type_filter:
        filtered_submittals = [s for s in filtered_submittals if s["submittal_type"] in type_filter]
    
    if priority_filter:
        filtered_submittals = [s for s in filtered_submittals if s["priority"] in priority_filter]
    
    # Submittal metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_submittals = len(submittals)
        st.metric("Total Submittals", total_submittals)
    
    with metrics_col2:
        open_submittals = len([s for s in submittals if s["status"] in [SubmittalStatus.DRAFT.value, SubmittalStatus.SUBMITTED.value, SubmittalStatus.UNDER_REVIEW.value]])
        st.metric("Open Submittals", open_submittals)
    
    with metrics_col3:
        approved_submittals = len([s for s in submittals if s["status"] in [SubmittalStatus.APPROVED.value, SubmittalStatus.APPROVED_AS_NOTED.value]])
        approval_rate = (approved_submittals / total_submittals) * 100 if total_submittals > 0 else 0
        st.metric("Approval Rate", f"{approval_rate:.1f}%")
    
    with metrics_col4:
        avg_review_time = 0
        review_times = [s["days_to_respond"] for s in submittals if s["days_to_respond"] is not None]
        
        if review_times:
            avg_review_time = sum(review_times) / len(review_times)
        
        st.metric("Avg. Review Time", f"{avg_review_time:.1f} days")
    
    # Visualizations
    st.subheader("Submittal Analysis")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Status distribution
        status_counts = {}
        for s in submittals:
            status = s["status"]
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
        
        # Create data for chart
        status_df = pd.DataFrame({
            "Status": list(status_counts.keys()),
            "Count": list(status_counts.values())
        })
        
        # Color map
        color_map = {
            SubmittalStatus.DRAFT.value: "#6c757d",      # Gray
            SubmittalStatus.SUBMITTED.value: "#17a2b8",  # Cyan
            SubmittalStatus.UNDER_REVIEW.value: "#ffc107", # Yellow
            SubmittalStatus.APPROVED.value: "#28a745",   # Green
            SubmittalStatus.APPROVED_AS_NOTED.value: "#20c997", # Teal
            SubmittalStatus.REVISE_AND_RESUBMIT.value: "#fd7e14", # Orange
            SubmittalStatus.REJECTED.value: "#dc3545"    # Red
        }
        
        # Create pie chart
        fig = px.pie(
            status_df,
            values="Count",
            names="Status",
            title="Submittal Status Distribution",
            color="Status",
            color_discrete_map=color_map
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with viz_col2:
        # Type distribution
        type_counts = {}
        for s in submittals:
            type_val = s["submittal_type"]
            if type_val not in type_counts:
                type_counts[type_val] = 0
            type_counts[type_val] += 1
        
        # Create data for chart
        type_df = pd.DataFrame({
            "Type": list(type_counts.keys()),
            "Count": list(type_counts.values())
        }).sort_values("Count", ascending=False)
        
        # Create bar chart
        fig = px.bar(
            type_df,
            x="Type",
            y="Count",
            title="Submittals by Type",
            color="Count",
            color_continuous_scale="Viridis"
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Submittal List
    st.subheader("Submittal List")
    
    # Sort by status priority and due date
    def get_status_priority(status):
        priority_order = {
            SubmittalStatus.DRAFT.value: 0,
            SubmittalStatus.SUBMITTED.value: 1,
            SubmittalStatus.UNDER_REVIEW.value: 2,
            SubmittalStatus.REVISE_AND_RESUBMIT.value: 3,
            SubmittalStatus.APPROVED_AS_NOTED.value: 4,
            SubmittalStatus.APPROVED.value: 5,
            SubmittalStatus.REJECTED.value: 6
        }
        return priority_order.get(status, 99)
    
    filtered_submittals.sort(key=lambda x: (get_status_priority(x["status"]), x["due_date"]))
    
    for submittal in filtered_submittals:
        # Get status color
        if submittal["status"] == SubmittalStatus.DRAFT.value:
            status_color = "#6c757d"  # Gray
        elif submittal["status"] == SubmittalStatus.SUBMITTED.value:
            status_color = "#17a2b8"  # Cyan
        elif submittal["status"] == SubmittalStatus.UNDER_REVIEW.value:
            status_color = "#ffc107"  # Yellow
        elif submittal["status"] == SubmittalStatus.APPROVED.value:
            status_color = "#28a745"  # Green
        elif submittal["status"] == SubmittalStatus.APPROVED_AS_NOTED.value:
            status_color = "#20c997"  # Teal
        elif submittal["status"] == SubmittalStatus.REVISE_AND_RESUBMIT.value:
            status_color = "#fd7e14"  # Orange
        else:  # REJECTED
            status_color = "#dc3545"  # Red
        
        # Get priority indicator
        if submittal["priority"] == "High":
            priority_color = "#dc3545"  # Red
            priority_icon = "🔴"
        elif submittal["priority"] == "Medium":
            priority_color = "#fd7e14"  # Orange
            priority_icon = "🟠"
        else:  # Low
            priority_color = "#28a745"  # Green
            priority_icon = "🟢"
        
        # Calculate days remaining
        days_remaining = (submittal["due_date"] - datetime.now()).days
        
        # Submittal card
        with st.expander(f"{priority_icon} {submittal['number']} - {submittal['spec_section']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{submittal['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Title:** {submittal['title']}")
                st.markdown(f"**Spec Section:** {submittal['spec_section']}")
                st.markdown(f"**Type:** {submittal['submittal_type']}")
                st.markdown(f"**Submitting Party:** {submittal['submitting_party']}")
                st.markdown(f"**Reviewing Party:** {submittal['reviewing_party']}")
                st.markdown(f"**Priority:** <span style='color: {priority_color}; font-weight: bold;'>{submittal['priority']}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Submission Date:** {submittal['submission_date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Due Date:** {submittal['due_date'].strftime('%Y-%m-%d')}")
                
                # Display days remaining/overdue
                if days_remaining < 0:
                    st.markdown(f"**Status:** <span style='color: #dc3545; font-weight: bold;'>Overdue by {abs(days_remaining)} days</span>", unsafe_allow_html=True)
                elif days_remaining == 0:
                    st.markdown(f"**Status:** <span style='color: #fd7e14; font-weight: bold;'>Due today</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**Status:** <span style='color: #28a745; font-weight: bold;'>{days_remaining} days remaining</span>", unsafe_allow_html=True)
                
                if submittal["review_date"]:
                    st.markdown(f"**Review Date:** {submittal['review_date'].strftime('%Y-%m-%d')}")
                
                st.markdown(f"**Revision:** {submittal['revision']}")
                st.markdown(f"**Attachments:** {submittal['attachments']}")
            
            st.markdown("### Description")
            st.markdown(submittal["description"])
            
            if submittal["comments"]:
                st.markdown("### Review Comments")
                st.markdown(submittal["comments"])
            
            # Action buttons
            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)
            
            with buttons_col1:
                if submittal["status"] == SubmittalStatus.DRAFT.value:
                    st.button("Submit", key=f"submit_subm_{submittal['id']}")
                elif submittal["status"] in [SubmittalStatus.SUBMITTED.value, SubmittalStatus.UNDER_REVIEW.value]:
                    st.button("Add Review", key=f"review_subm_{submittal['id']}")
                elif submittal["status"] == SubmittalStatus.REVISE_AND_RESUBMIT.value:
                    st.button("Resubmit", key=f"resubmit_subm_{submittal['id']}")
            
            with buttons_col2:
                if st.button("Edit", key=f"edit_subm_{submittal['id']}"):
                    st.session_state.edit_submittal_id = submittal["id"]
                    st.session_state.show_submittal_form = True
                    st.rerun()
            
            with buttons_col3:
                st.button("View Attachments", key=f"attach_subm_{submittal['id']}")
    
    # Create Submittal button with action buttons in a row
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Create New Submittal", type="primary", key="create_submittal_btn", use_container_width=True):
            # Initialize form state
            st.session_state.show_submittal_form = True
            st.session_state.edit_submittal_id = None
    
    # Submittal creation/edit form
    if st.session_state.get("show_submittal_form", False):
        # Get submittal data if editing
        submittal_to_edit = None
        if st.session_state.get("edit_submittal_id"):
            submittal_to_edit = next((s for s in submittals if s.get("id") == st.session_state.get("edit_submittal_id")), None)
        
        # Use the enhanced form component
        form_submitted, form_data = submittal_form(
            is_edit=st.session_state.get("edit_submittal_id") is not None,
            submittal_data=submittal_to_edit
        )
        
        if form_submitted and form_data:
            # In a real app, this would save to database
            
            # Update or create submittal
            if st.session_state.get("edit_submittal_id"):
                # Update existing submittal
                for i, submittal in enumerate(submittals):
                    if submittal["id"] == st.session_state.get("edit_submittal_id"):
                        # Preserve ID and other metadata
                        form_data["id"] = submittal["id"]
                        form_data["number"] = submittal["number"]
                        form_data["submitted_date"] = datetime.now()
                        submittals[i].update(form_data)
                        break
                st.success("Submittal updated successfully!")
            else:
                # Add new submittal to the list
                new_submittal = {
                    "id": f"SUBM-{len(submittals) + 1:03d}",
                    "number": len(submittals) + 1,
                    "spec_section": form_data["spec_section"],
                    "submittal_type": form_data["submittal_type"],
                    "title": form_data["title"],
                    "submitting_party": form_data["submitting_party"],
                    "reviewing_party": form_data["reviewing_party"],
                    "priority": form_data["priority"],
                    "due_date": form_data["due_date"],
                    "description": form_data["description"],
                    "status": form_data["status"],
                    "submitted_date": datetime.now(),
                    "response_date": None,
                    "days_to_respond": None,
                    "attachments": len(form_data.get("attachments", [])),
                    "revision": 0
                }
                submittals.insert(0, new_submittal)  # Add to beginning of list
                st.success(f"Submittal {form_data['status'].lower()} successfully!")
            
            # Reset form state
            st.session_state.show_submittal_form = False
            st.session_state.edit_submittal_id = None
            
            # Force rerender
            st.rerun()