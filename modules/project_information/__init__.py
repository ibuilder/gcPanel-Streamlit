"""
Project Information module for gcPanel Construction Management Dashboard.

This module renders the project information forms and details.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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
    st.markdown(
        f"""
        <div class="dashboard-card" style="padding: 1.5rem; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h2 style="margin-bottom: 0.3rem; font-size: 1.5rem;">{project_data['name']}</h2>
                    <p style="margin-bottom: 1rem; color: #6c757d; font-size: 0.9rem;">Project Code: {project_data['code']}</p>
                    <p style="margin-bottom: 0.5rem;">{project_data['description']}</p>
                </div>
                <div>
                    <span class="status-pill status-active">{project_data['status']}</span>
                </div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Key project information in a grid layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Project Details</h3>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Project Type:</div>
                    <div>{project_data['type']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Owner:</div>
                    <div>{project_data['owner']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Start Date:</div>
                    <div>{project_data['start_date']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">End Date:</div>
                    <div>{project_data['end_date']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Budget:</div>
                    <div>{project_data['budget']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Building Information</h3>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Location:</div>
                    <div>{project_data['location']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Square Footage:</div>
                    <div>{project_data['square_footage']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Stories:</div>
                    <div>{project_data['stories']}</div>
                </div>
                
                <div style="display: flex; margin-bottom: 0.7rem;">
                    <div style="width: 40%; font-weight: 500; color: #6c757d;">Units:</div>
                    <div>{project_data['units']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

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
            st.markdown(
                f"""
                <div class="dashboard-card" style="margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.7rem;">
                        <div style="width: 50px; height: 50px; border-radius: 50%; background-color: #f0f0f0; 
                                 display: flex; justify-content: center; align-items: center; margin-right: 1rem;">
                            <span class="material-icons">person</span>
                        </div>
                        <div>
                            <div style="font-weight: 500; font-size: 1rem;">{member['name']}</div>
                            <div style="color: #3e79f7; font-size: 0.9rem;">{member['role']}</div>
                        </div>
                    </div>
                    <div style="margin-bottom: 0.5rem; font-size: 0.9rem;">
                        <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.5rem; color: #6c757d;">
                            email
                        </span>
                        {member['email']}
                    </div>
                    <div style="font-size: 0.9rem;">
                        <span class="material-icons" style="font-size: 0.9rem; vertical-align: middle; margin-right: 0.5rem; color: #6c757d;">
                            phone
                        </span>
                        {member['phone']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

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
        # Determine status style
        if milestone["status"] == "Completed":
            status_class = "status-active"
            icon = "check_circle"
        elif milestone["status"] == "In Progress":
            status_class = "status-pending"
            icon = "hourglass_top"
        else:
            status_class = ""
            icon = "calendar_today"
        
        st.markdown(
            f"""
            <div class="dashboard-card" style="margin-bottom: 0.7rem; padding: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center;">
                        <span class="material-icons" style="margin-right: 0.7rem; color: {
                            "#38d39f" if milestone["status"] == "Completed" else 
                            "#f9c851" if milestone["status"] == "In Progress" else "#6c757d"
                        };">
                            {icon}
                        </span>
                        <div>
                            <div style="font-weight: 500; font-size: 1rem;">{milestone["name"]}</div>
                            <div style="color: #6c757d; font-size: 0.9rem;">{milestone["description"]}</div>
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: flex-end;">
                        <div style="font-size: 0.9rem; margin-bottom: 0.3rem;">{milestone["date"]}</div>
                        <span class="status-pill {status_class}" style="font-size: 0.8rem;">{milestone["status"]}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

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
    
    # Display map
    st.markdown(
        f"""
        <div class="dashboard-card" style="margin-bottom: 1.5rem; padding: 0;">
            <div style="height: 400px; background-color: #f7f7f7; display: flex; justify-content: center; align-items: center;">
                <div style="text-align: center;">
                    <span class="material-icons" style="font-size: 3rem; color: #6c757d; margin-bottom: 1rem;">map</span>
                    <div>Map would appear here in a complete implementation</div>
                    <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #6c757d;">
                        Location: {location_data["latitude"]}, {location_data["longitude"]}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
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