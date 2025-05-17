"""
Safety module for the gcPanel Construction Management Dashboard.

This module provides safety management functionality including incident tracking,
safety training, compliance monitoring, and safety reports.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def render_safety():
    """Render the safety management interface."""
    st.header("Safety Management")
    
    # Create tabs for different safety functions
    tabs = st.tabs(["Dashboard", "Incidents", "Training", "Compliance"])
    
    # Safety Dashboard Tab
    with tabs[0]:
        render_safety_dashboard()
    
    # Incidents Tab
    with tabs[1]:
        render_incidents()
    
    # Training Tab
    with tabs[2]:
        render_training()
        
    # Compliance Tab
    with tabs[3]:
        render_compliance()

def render_safety_dashboard():
    """Render the safety dashboard with metrics and charts."""
    st.subheader("Safety Dashboard")
    
    # Key Safety Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Recordable Incident Rate", "1.2", "-0.3 vs Industry Avg")
    with col2:
        st.metric("Days Without Lost Time Incident", "42", "+5 since last week")
    with col3:
        st.metric("Safety Compliance Score", "94%", "+2% this month")
    
    # Create columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Incidents by Type")
        incident_types = {
            'Type': ['Near Miss', 'First Aid', 'Medical Treatment', 'Lost Time', 'Property Damage'],
            'Count': [12, 8, 3, 1, 5]
        }
        incident_df = pd.DataFrame(incident_types)
        st.bar_chart(incident_df.set_index('Type'), color='#1e3a8a')
    
    with col2:
        st.subheader("Safety Observations by Project")
        projects = {
            'Project': ['Highland Tower', 'City Center', 'Riverside Apartments', 'Metro Office'],
            'Observations': [24, 18, 15, 10]
        }
        projects_df = pd.DataFrame(projects)
        st.bar_chart(projects_df.set_index('Project'), color='#1e3a8a')
    
    # Safety Trends
    st.subheader("Safety Trends (Last 12 Months)")
    
    # Generate some trend data
    months = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr']
    trend_data = pd.DataFrame({
        'Month': months,
        'TRIR': [1.8, 1.7, 1.6, 1.5, 1.5, 1.4, 1.3, 1.3, 1.3, 1.2, 1.2, 1.2],
        'Industry Avg': [2.0, 2.0, 2.0, 2.0, 2.0, 1.9, 1.9, 1.9, 1.9, 1.9, 1.9, 1.9]
    })
    
    # Plot the trend
    st.line_chart(trend_data.set_index('Month'))
    
    # Recent Safety Activities
    st.subheader("Recent Safety Activities")
    
    activities = [
        {"date": "2025-05-15", "project": "Highland Tower", "activity": "Toolbox Talk: Fall Protection", "participants": 24},
        {"date": "2025-05-14", "project": "City Center", "activity": "Safety Committee Meeting", "participants": 8},
        {"date": "2025-05-12", "project": "Highland Tower", "activity": "PPE Inspection", "participants": 32},
        {"date": "2025-05-10", "project": "Riverside Apartments", "activity": "Fire Drill", "participants": 18},
        {"date": "2025-05-08", "project": "Metro Office", "activity": "Hazard Assessment", "participants": 6}
    ]
    
    activities_df = pd.DataFrame(activities)
    st.dataframe(activities_df, use_container_width=True)

def render_incidents():
    """Render the incident management interface."""
    st.subheader("Incident Management")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("Report Incident", key="report_incident")
    with col2:
        st.button("Generate OSHA Report", key="generate_osha_report")
    
    # Add filter options
    with st.expander("Filter Options"):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Project", ["All Projects", "Highland Tower", "City Center", "Riverside Apartments"])
            st.selectbox("Incident Type", ["All Types", "Near Miss", "First Aid", "Medical Treatment", "Lost Time", "Property Damage"])
        with col2:
            st.date_input("From Date", datetime.now() - timedelta(days=90))
            st.date_input("To Date", datetime.now())
    
    # Sample incident data
    incidents = [
        {"id": 1, "date": "2025-05-10", "project": "Highland Tower", "type": "Near Miss", "description": "Worker almost struck by falling material", "status": "Investigated"},
        {"id": 2, "date": "2025-05-05", "project": "City Center", "type": "First Aid", "description": "Minor cut on hand", "status": "Closed"},
        {"id": 3, "date": "2025-04-28", "project": "Highland Tower", "type": "Medical Treatment", "description": "Sprained ankle from trip", "status": "Open"},
        {"id": 4, "date": "2025-04-15", "project": "Riverside Apartments", "type": "Lost Time", "description": "Back injury from lifting", "status": "Open"},
        {"id": 5, "date": "2025-04-10", "project": "City Center", "type": "Property Damage", "description": "Forklift damaged wall", "status": "Closed"}
    ]
    
    # Convert to DataFrame
    incidents_df = pd.DataFrame(incidents)
    
    # Add status styling
    def status_color(val):
        if val == "Open":
            return 'background-color: #fee2e2; color: #7f1d1d'
        elif val == "Investigated":
            return 'background-color: #fef3c7; color: #78350f'
        else:
            return 'background-color: #d1fae5; color: #064e3b'
    
    # Apply styling
    styled_df = incidents_df.style.applymap(status_color, subset=['status'])
    
    # Display the dataframe
    st.dataframe(styled_df, use_container_width=True)
    
    # Sample incident detail
    if st.button("View Sample Incident Details", key="view_incident"):
        st.subheader("Incident #4: Back injury from lifting")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Project:** Riverside Apartments")
            st.markdown("**Date:** April 15, 2025")
            st.markdown("**Type:** Lost Time Incident")
        with col2:
            st.markdown("**Reported By:** John Smith")
            st.markdown("**Status:** Open")
            st.markdown("**OSHA Recordable:** Yes")
        
        st.markdown("### Incident Description")
        st.markdown("""
        Worker was attempting to lift a 75 lb box of materials without assistance.
        Experienced acute lower back pain and was unable to continue working.
        Transported to urgent care facility for evaluation.
        """)
        
        st.markdown("### Medical Treatment")
        st.markdown("""
        - Evaluated at City Urgent Care
        - Diagnosed with lumbar strain
        - Prescribed pain medication and muscle relaxers
        - Restricted duty for 2 weeks
        """)
        
        st.markdown("### Root Cause Analysis")
        st.markdown("""
        1. Primary Cause: Improper lifting technique
        2. Contributing Factors:
           - Material was improperly packaged with no clear weight label
           - Worker had not completed refresher training on proper lifting
           - No mechanical assistance (hand truck) was readily available
        """)
        
        st.markdown("### Corrective Actions")
        corrective_actions = {
            "Action": ["Refresher training on proper lifting", "Label all materials over 50 lbs", "Purchase additional hand trucks", "Update safety procedures"],
            "Assigned To": ["Safety Manager", "Warehouse Supervisor", "Project Manager", "Safety Committee"],
            "Due Date": ["2025-04-25", "2025-04-30", "2025-05-15", "2025-05-10"],
            "Status": ["Completed", "In Progress", "Not Started", "In Progress"]
        }
        
        st.dataframe(pd.DataFrame(corrective_actions), use_container_width=True)

def render_training():
    """Render the safety training interface."""
    st.subheader("Safety Training")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("Schedule Training", key="schedule_training")
    with col2:
        st.button("Training Report", key="training_report")
    
    # Training calendar
    st.subheader("Upcoming Training Sessions")
    
    training_sessions = [
        {"date": "2025-05-20", "title": "Fall Protection Certification", "location": "Highland Tower Jobsite", "trainer": "John Smith", "duration": "8 hours", "seats": "15/20"},
        {"date": "2025-05-22", "title": "Confined Space Entry", "location": "Main Office Training Room", "trainer": "Mary Johnson", "duration": "4 hours", "seats": "12/15"},
        {"date": "2025-05-27", "title": "First Aid/CPR", "location": "City Center Jobsite", "trainer": "Red Cross", "duration": "6 hours", "seats": "8/12"},
        {"date": "2025-06-03", "title": "OSHA 10-Hour", "location": "Main Office Training Room", "trainer": "Robert Lee", "duration": "2 days", "seats": "20/25"},
        {"date": "2025-06-10", "title": "Equipment Safety", "location": "Riverside Apartments Jobsite", "trainer": "Equipment Supplier", "duration": "3 hours", "seats": "6/10"}
    ]
    
    # Convert to DataFrame
    training_df = pd.DataFrame(training_sessions)
    st.dataframe(training_df, use_container_width=True)
    
    # Training compliance
    st.subheader("Training Compliance")
    
    # Generate sample compliance data
    compliance_data = {
        'Training Type': ['Fall Protection', 'First Aid/CPR', 'OSHA 10-Hour', 'Equipment Safety', 'Hazard Communication'],
        'Required': [35, 40, 45, 30, 50],
        'Completed': [33, 37, 45, 28, 48],
        'Compliance %': [94, 92, 100, 93, 96]
    }
    
    compliance_df = pd.DataFrame(compliance_data)
    
    # Add status styling
    def compliance_color(val):
        if val < 90:
            return 'background-color: #fee2e2; color: #7f1d1d'
        elif val < 95:
            return 'background-color: #fef3c7; color: #78350f'
        else:
            return 'background-color: #d1fae5; color: #064e3b'
    
    # Apply styling
    styled_compliance_df = compliance_df.style.applymap(compliance_color, subset=['Compliance %'])
    
    # Display the dataframe
    st.dataframe(styled_compliance_df, use_container_width=True)
    
    # Training metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Training Hours YTD", "1,245", "+215 since last month")
    with col2:
        st.metric("Average Completion Rate", "95%", "+2% vs target")
    with col3:
        st.metric("Certifications Expiring Soon", "12", "-3 since last week")

def render_compliance():
    """Render the safety compliance interface."""
    st.subheader("Safety Compliance")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("New Inspection", key="new_inspection")
    with col2:
        st.button("Compliance Report", key="compliance_report")
    
    # Safety inspection results
    st.subheader("Recent Safety Inspections")
    
    inspections = [
        {"date": "2025-05-14", "project": "Highland Tower", "inspector": "Safety Manager", "score": "96%", "findings": 2, "critical": 0},
        {"date": "2025-05-12", "project": "City Center", "inspector": "Project Manager", "score": "88%", "findings": 6, "critical": 1},
        {"date": "2025-05-10", "project": "Riverside Apartments", "inspector": "Safety Consultant", "score": "94%", "findings": 3, "critical": 0},
        {"date": "2025-05-05", "project": "Metro Office", "inspector": "Safety Manager", "score": "92%", "findings": 4, "critical": 0},
        {"date": "2025-05-01", "project": "Highland Tower", "inspector": "OSHA", "score": "90%", "findings": 5, "critical": 1}
    ]
    
    # Convert to DataFrame
    inspections_df = pd.DataFrame(inspections)
    
    # Add score styling
    def score_color(val):
        score = int(val.strip('%'))
        if score < 90:
            return 'background-color: #fee2e2; color: #7f1d1d'
        elif score < 95:
            return 'background-color: #fef3c7; color: #78350f'
        else:
            return 'background-color: #d1fae5; color: #064e3b'
    
    # Apply styling
    styled_inspections_df = inspections_df.style.applymap(score_color, subset=['score'])
    
    # Display the dataframe
    st.dataframe(styled_inspections_df, use_container_width=True)
    
    # Compliance items tracking
    st.subheader("Open Compliance Items")
    
    compliance_items = [
        {"id": 1, "date_identified": "2025-05-12", "project": "City Center", "description": "Missing guardrails on 3rd floor scaffold", "priority": "High", "assigned_to": "John Smith", "due_date": "2025-05-15"},
        {"id": 2, "date_identified": "2025-05-10", "project": "Riverside Apartments", "description": "Improper storage of flammable materials", "priority": "Medium", "assigned_to": "Mary Johnson", "due_date": "2025-05-17"},
        {"id": 3, "date_identified": "2025-05-05", "project": "Metro Office", "description": "Unmarked exits in temporary office", "priority": "Medium", "assigned_to": "Robert Lee", "due_date": "2025-05-12"},
        {"id": 4, "date_identified": "2025-05-01", "project": "Highland Tower", "description": "Exposed electrical wiring", "priority": "High", "assigned_to": "Jane Wilson", "due_date": "2025-05-08"},
        {"id": 5, "date_identified": "2025-04-28", "project": "City Center", "description": "Incomplete confined space permits", "priority": "Low", "assigned_to": "Mark Davis", "due_date": "2025-05-15"}
    ]
    
    # Convert to DataFrame
    compliance_items_df = pd.DataFrame(compliance_items)
    
    # Add priority styling
    def priority_color(val):
        if val == "High":
            return 'background-color: #fee2e2; color: #7f1d1d'
        elif val == "Medium":
            return 'background-color: #fef3c7; color: #78350f'
        else:
            return 'background-color: #d1fae5; color: #064e3b'
    
    # Apply styling
    styled_compliance_items_df = compliance_items_df.style.applymap(priority_color, subset=['priority'])
    
    # Display the dataframe
    st.dataframe(styled_compliance_items_df, use_container_width=True)