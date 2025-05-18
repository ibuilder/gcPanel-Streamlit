"""
Project Information module for gcPanel Construction Management Dashboard.

This module renders the project information forms and details.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def get_status_color(status):
    """Return the appropriate color for a status value"""
    status_colors = {
        "Active": "green",
        "Planning": "blue",
        "On Hold": "orange",
        "Completed": "violet",
        # Add more statuses as needed
    }
    return status_colors.get(status, "gray")

def render_project_information():
    """Render the project information page."""
    
    st.header("Project Information")
    
    # Current project info
    current_project = st.session_state.get("current_project", "Highland Tower Development")
    
    # Tabs for different project information sections
    tabs = st.tabs(["Overview", "Team", "Schedule", "Location", "Documents", "Contacts"])
    
    with tabs[0]:  # Overview tab
        if st.session_state.get("edit_project", False):
            render_project_edit_form()
        else:
            render_project_details()
            
    with tabs[1]:  # Team tab
        render_project_team()
        
    with tabs[2]:  # Schedule tab
        render_project_schedule()
        
    with tabs[3]:  # Location tab
        render_project_location()
        
    with tabs[4]:  # Documents tab
        render_project_documents()
        
    with tabs[5]:  # Contacts tab
        render_project_contacts()

def render_project_details():
    """Render the project details view."""
    
    # Project data (in a real app, this would come from a database)
    project_data = {
        "name": "Highland Tower Development",
        "code": "HTD-2025",
        "description": "A 15-story high-rise residential tower with retail spaces on the ground floor and underground parking. The project includes 120 residential units, ranging from studios to 3-bedroom apartments, with amenities such as a rooftop garden, fitness center, and community spaces.",
        "type": "Residential / Mixed-Use",
        "status": "Active",
        "owner": "Highland Development Corp.",
        "start_date": "January 15, 2025",
        "end_date": "December 20, 2025",
        "budget": "$45,500,000",
        "location": "123 Highland Ave, Seattle, WA",
        "square_footage": "168,500 sq ft",
        "stories": "15 above ground, 2 below",
        "units": "120 residential, 8 retail"
    }
    
    # Edit button in the top-right corner
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Edit", key="edit_project_btn", type="primary"):
            st.session_state.edit_project = True
            st.rerun()
    
    # Project header card
    st.header(project_data['name'])
    st.caption(f"Project Code: {project_data['code']}")
    
    # Status badge
    st.markdown(f"**Status:** :{get_status_color(project_data['status'])}[{project_data['status']}]")
    
    # Project description
    st.markdown(project_data['description'])
    
    # Key project information in a grid layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Use a native Streamlit container with styling
        with st.container():
            st.markdown("### Project Details")
            
            # Create subcontainers for each detail
            details = [
                {"label": "Project Type", "value": project_data['type']},
                {"label": "Owner", "value": project_data['owner']},
                {"label": "Start Date", "value": project_data['start_date']},
                {"label": "End Date", "value": project_data['end_date']},
                {"label": "Budget", "value": project_data['budget']}
            ]
            
            # Display each detail in a row
            for detail in details:
                cols = st.columns([2, 3])
                with cols[0]:
                    st.markdown(f"**{detail['label']}:**")
                with cols[1]:
                    st.markdown(f"{detail['value']}")
                st.markdown("---")
    
    with col2:
        # Use a native Streamlit container with styling
        with st.container():
            st.markdown("### Building Information")
            
            # Create subcontainers for each detail
            details = [
                {"label": "Location", "value": project_data['location']},
                {"label": "Square Footage", "value": project_data['square_footage']},
                {"label": "Stories", "value": project_data['stories']},
                {"label": "Units", "value": project_data['units']}
            ]
            
            # Display each detail in a row
            for detail in details:
                cols = st.columns([2, 3])
                with cols[0]:
                    st.markdown(f"**{detail['label']}:**")
                with cols[1]:
                    st.markdown(f"{detail['value']}")
                st.markdown("---")

def render_project_edit_form():
    """Render the project edit form."""
    
    # Project data (pre-filled with existing values)
    project_data = {
        "name": "Highland Tower Development",
        "code": "HTD-2025",
        "description": "A 15-story high-rise residential tower with retail spaces on the ground floor and underground parking. The project includes 120 residential units, ranging from studios to 3-bedroom apartments, with amenities such as a rooftop garden, fitness center, and community spaces.",
        "type": "Residential / Mixed-Use",
        "status": "Active",
        "owner": "Highland Development Corp.",
        "start_date": "2025-01-15",
        "end_date": "2025-12-20",
        "budget": 45500000,
        "location": "123 Highland Ave, Seattle, WA",
        "square_footage": 168500,
        "stories": "15 above ground, 2 below",
        "units": "120 residential, 8 retail"
    }
    
    # Edit form
    with st.form(key="edit_project_form"):
        st.markdown("### Project Information")
        
        name = st.text_input("Project Name", value=project_data["name"])
        code = st.text_input("Project Code", value=project_data["code"])
        
        col1, col2 = st.columns(2)
        with col1:
            status = st.selectbox("Status", ["Active", "Planning", "On Hold", "Completed"], index=0)
            type_options = ["Residential", "Commercial", "Industrial", "Mixed-Use", "Infrastructure", "Healthcare", "Education", "Other"]
            type_index = type_options.index("Residential") if "Residential" in type_options else 0
            type = st.selectbox("Project Type", type_options, index=type_index)
            owner = st.text_input("Owner", value=project_data["owner"])
        
        with col2:
            start_date = st.date_input("Start Date", value=datetime.strptime(project_data["start_date"], "%Y-%m-%d"))
            end_date = st.date_input("End Date", value=datetime.strptime(project_data["end_date"], "%Y-%m-%d"))
            budget = st.number_input("Budget ($)", value=project_data["budget"], step=10000)
        
        st.markdown("### Project Description")
        description = st.text_area("Description", value=project_data["description"], height=100)
        
        st.markdown("### Building Information")
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location", value=project_data["location"])
            square_footage = st.number_input("Square Footage (sq ft)", value=project_data["square_footage"], step=100)
        
        with col2:
            stories = st.text_input("Stories", value=project_data["stories"])
            units = st.text_input("Units", value=project_data["units"])
        
        # Form buttons
        col1, col2 = st.columns([1, 4])
        with col1:
            submit = st.form_submit_button("Save", type="primary")
        with col2:
            cancel = st.form_submit_button("Cancel")
        
        # Handle form submission
        if submit:
            # In a real app, save data to database here
            st.success("Project information updated successfully!")
            st.session_state.edit_project = False
            st.rerun()
        
        if cancel:
            st.session_state.edit_project = False
            st.rerun()

def render_project_team():
    """Render the project team information."""
    
    # Team members data
    team_members = [
        {"name": "John Smith", "role": "Project Manager", "email": "john.smith@example.com", "phone": "206-555-1234", "photo": "https://via.placeholder.com/150"},
        {"name": "Sarah Johnson", "role": "Project Engineer", "email": "sarah.johnson@example.com", "phone": "206-555-2345", "photo": "https://via.placeholder.com/150"},
        {"name": "Robert Chen", "role": "Superintendent", "email": "robert.chen@example.com", "phone": "206-555-3456", "photo": "https://via.placeholder.com/150"},
        {"name": "Jessica Williams", "role": "BIM Coordinator", "email": "jessica.williams@example.com", "phone": "206-555-4567", "photo": "https://via.placeholder.com/150"},
        {"name": "Michael Brown", "role": "Safety Manager", "email": "michael.brown@example.com", "phone": "206-555-5678", "photo": "https://via.placeholder.com/150"},
        {"name": "Amanda Martinez", "role": "Project Coordinator", "email": "amanda.martinez@example.com", "phone": "206-555-6789", "photo": "https://via.placeholder.com/150"}
    ]
    
    # Display team
    st.subheader("Project Team")
    
    # Create a layout for team cards
    cols = st.columns(3)
    
    # Display each team member
    for i, member in enumerate(team_members):
        with cols[i % 3]:
            # Create a container for each team member
            with st.container():
                # Create a card-like appearance
                st.markdown("---")
                
                # Team member name and role
                st.markdown(f"### {member['name']}")
                st.markdown(f"**{member['role']}**")
                
                # Contact information
                st.markdown(f"📧 {member['email']}")
                st.markdown(f"📱 {member['phone']}")
                st.markdown("---")

def render_project_schedule():
    """Render the project schedule information."""
    
    # Schedule data
    milestones = [
        {"name": "Project Start", "date": "January 15, 2025", "status": "Completed", "description": "Official project kickoff"},
        {"name": "Design & Permitting", "date": "March 10, 2025", "status": "Completed", "description": "Complete design documents and obtain permits"},
        {"name": "Site Preparation", "date": "April 5, 2025", "status": "Completed", "description": "Site clearing and preparation"},
        {"name": "Foundation Complete", "date": "May 15, 2025", "status": "In Progress", "description": "Complete all foundation work"},
        {"name": "Structure to 8th Floor", "date": "July 20, 2025", "status": "Not Started", "description": "Complete structure up to 8th floor"},
        {"name": "Structure Complete", "date": "September 10, 2025", "status": "Not Started", "description": "Complete all structural elements"},
        {"name": "Building Envelope", "date": "October 15, 2025", "status": "Not Started", "description": "Complete building envelope and weatherproofing"},
        {"name": "Interior Finishes", "date": "November 25, 2025", "status": "Not Started", "description": "Complete all interior finishes"},
        {"name": "Project Completion", "date": "December 20, 2025", "status": "Not Started", "description": "Project handover to owner"}
    ]
    
    # Display schedule
    st.subheader("Project Schedule")
    
    # Show timeline visualization
    chart_data = []
    for i, milestone in enumerate(milestones):
        # Determine status color
        if milestone["status"] == "Completed":
            color = "#38d39f"  # Green
        elif milestone["status"] == "In Progress":
            color = "#f9c851"  # Yellow/amber
        else:
            color = "#6c757d"  # Gray
        
        chart_data.append((milestone["name"], i+1, color))
    
    # Create milestone cards
    for milestone in milestones:
        # Create a container for each milestone
        with st.container():
            # Set up the milestone row with columns for layout
            col_icon, col_details, col_date = st.columns([1, 5, 2])
            
            # Determine status icon and color
            if milestone["status"] == "Completed":
                status_icon = "✅"
                status_color = "green"
            elif milestone["status"] == "In Progress":
                status_icon = "⏳"
                status_color = "orange"
            else:
                status_icon = "📅"
                status_color = "gray"
            
            # Display milestone details
            with col_icon:
                st.markdown(f"### {status_icon}")
            
            with col_details:
                st.markdown(f"### {milestone['name']}")
                st.markdown(f"{milestone['description']}")
            
            with col_date:
                st.markdown(f"**{milestone['date']}**")
                st.markdown(f":{status_color}[{milestone['status']}]")
            
            st.markdown("---")

def render_project_location():
    """Render the project location information."""
    
    st.subheader("Project Location")
    
    # Location data
    location_data = {
        "address": "123 Highland Ave, Seattle, WA 98101",
        "latitude": 47.6062,
        "longitude": -122.3321,
        "zoning": "Mixed-Use Residential (MR)",
        "parcel_number": "123456-7890",
        "lot_size": "42,500 sq ft"
    }
    
    # Display map placeholder with native Streamlit components
    with st.container():
        # Create a card-like container for the map
        st.markdown("### Map View")
        
        # Create a placeholder for the map with some basic styling
        map_container = st.container()
        with map_container:
            # Add a colored background to simulate a map container
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.markdown("#### Map Placeholder")
                st.markdown("Map would appear here in a complete implementation")
                st.markdown(f"**Location:** {location_data['latitude']}, {location_data['longitude']}")
            st.markdown("---")
    
    # Location details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Location Details</h3>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Address:</div>
                    <div>{location_data['address']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Zoning:</div>
                    <div>{location_data['zoning']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Parcel Number:</div>
                    <div>{location_data['parcel_number']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Lot Size:</div>
                    <div>{location_data['lot_size']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="dashboard-card">
                <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Site Conditions</h3>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Soil Type:</div>
                    <div>Type 2 - Stiff Clay</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Elevation:</div>
                    <div>175 ft above sea level</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Water Table:</div>
                    <div>45 ft below grade</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Seismic Zone:</div>
                    <div>Zone 3</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_project_documents():
    """Render the project documents section."""
    
    st.subheader("Project Documents")
    
    # Document categories
    categories = st.tabs(["Contract Documents", "Drawings", "Specifications", "Permits", "Reports"])
    
    with categories[0]:  # Contract Documents
        # Document list
        documents = [
            {"name": "Owner-Contractor Agreement", "type": "PDF", "size": "2.4 MB", "date": "Jan 15, 2025", "author": "Legal Dept"},
            {"name": "General Conditions", "type": "PDF", "size": "3.1 MB", "date": "Jan 15, 2025", "author": "Legal Dept"},
            {"name": "Supplementary Conditions", "type": "PDF", "size": "1.2 MB", "date": "Jan 15, 2025", "author": "Legal Dept"},
            {"name": "Schedule of Values", "type": "Excel", "size": "845 KB", "date": "Jan 20, 2025", "author": "John Smith"}
        ]
        
        # Create document table
        st.markdown(
            """
            <div class="dashboard-card" style="padding: 0; overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background-color: #f8f9fa; border-bottom: 2px solid #eef2f7;">
                            <th style="padding: 0.75rem; text-align: left;">Document Name</th>
                            <th style="padding: 0.75rem; text-align: left;">Type</th>
                            <th style="padding: 0.75rem; text-align: left;">Size</th>
                            <th style="padding: 0.75rem; text-align: left;">Date</th>
                            <th style="padding: 0.75rem; text-align: left;">Author</th>
                            <th style="padding: 0.75rem; text-align: center;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
            """,
            unsafe_allow_html=True
        )
        
        for doc in documents:
            # Determine icon based on document type
            icon = "description"
            if doc["type"] == "Excel":
                icon = "table_chart"
            elif doc["type"] == "Word":
                icon = "article"
            elif doc["type"] == "Image":
                icon = "image"
            
            st.markdown(
                f"""
                <tr style="border-bottom: 1px solid #eef2f7;">
                    <td style="padding: 0.75rem;">
                        <div style="display: flex; align-items: center;">
                            <span class="material-icons" style="color: #3e79f7; margin-right: 0.5rem;">
                                {icon}
                            </span>
                            {doc['name']}
                        </div>
                    </td>
                    <td style="padding: 0.75rem;">{doc['type']}</td>
                    <td style="padding: 0.75rem;">{doc['size']}</td>
                    <td style="padding: 0.75rem;">{doc['date']}</td>
                    <td style="padding: 0.75rem;">{doc['author']}</td>
                    <td style="padding: 0.75rem; text-align: center;">
                        <span class="material-icons" style="color: #3e79f7; cursor: pointer; font-size: 1.1rem; margin-right: 0.5rem;" title="View">
                            visibility
                        </span>
                        <span class="material-icons" style="color: #38d39f; cursor: pointer; font-size: 1.1rem; margin-right: 0.5rem;" title="Download">
                            download
                        </span>
                    </td>
                </tr>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown(
            """
                    </tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Similar implementation for other document categories
    with categories[1]:  # Drawings
        st.info("Drawings section - Implement similar table with drawing documents")
    
    with categories[2]:  # Specifications
        st.info("Specifications section - Implement similar table with specification documents")
    
    with categories[3]:  # Permits
        st.info("Permits section - Implement similar table with permit documents")
    
    with categories[4]:  # Reports
        st.info("Reports section - Implement similar table with report documents")

def render_project_contacts():
    """Render the project contacts section."""
    
    st.subheader("Project Contacts")
    
    # Contact categories
    categories = st.tabs(["Owner", "Design Team", "Subcontractors", "Suppliers", "Agencies"])
    
    with categories[0]:  # Owner
        # Contact list
        contacts = [
            {"name": "Michael Wilson", "company": "Highland Development Corp.", "role": "Owner Representative", "email": "michael.wilson@highland.com", "phone": "206-555-9876"},
            {"name": "Jennifer Lee", "company": "Highland Development Corp.", "role": "Financial Officer", "email": "jennifer.lee@highland.com", "phone": "206-555-8765"},
            {"name": "David Kim", "company": "Highland Development Corp.", "role": "Development Director", "email": "david.kim@highland.com", "phone": "206-555-7654"}
        ]
        
        # Display contacts
        for contact in contacts:
            st.markdown(
                f"""
                <div class="dashboard-card" style="margin-bottom: 0.7rem; padding: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 500; font-size: 1rem;">{contact['name']}</div>
                            <div style="font-size: 0.9rem;">{contact['company']}</div>
                            <div style="color: #3e79f7; font-size: 0.9rem;">{contact['role']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="margin-bottom: 0.3rem;">
                                <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.3rem; color: #6c757d;">
                                    email
                                </span>
                                {contact['email']}
                            </div>
                            <div>
                                <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.3rem; color: #6c757d;">
                                    phone
                                </span>
                                {contact['phone']}
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Similar implementation for other contact categories
    with categories[1]:  # Design Team
        st.info("Design Team section - Implement similar contact cards for design team members")
    
    with categories[2]:  # Subcontractors
        st.info("Subcontractors section - Implement similar contact cards for subcontractors")
    
    with categories[3]:  # Suppliers
        st.info("Suppliers section - Implement similar contact cards for suppliers")
    
    with categories[4]:  # Agencies
        st.info("Agencies section - Implement similar contact cards for agencies")