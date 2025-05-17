"""
Field Operations module for the gcPanel Construction Management Dashboard.

This module provides functionality for managing field operations including
daily reports, inspections, and quality control.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_field_operations():
    """Render the field operations interface."""
    st.header("Field Operations")
    
    # Create tabs for different field operation functions
    tabs = st.tabs(["Daily Reports", "Inspections", "Quality Control", "Safety Observations"])
    
    # Daily Reports Tab
    with tabs[0]:
        render_daily_reports()
    
    # Inspections Tab
    with tabs[1]:
        render_inspections()
    
    # Quality Control Tab
    with tabs[2]:
        render_quality_control()
        
    # Safety Observations Tab
    with tabs[3]:
        render_safety_observations()

def render_daily_reports():
    """Render the daily reports interface."""
    st.subheader("Daily Reports")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("New Report", key="new_daily_report")
    with col2:
        st.button("Export Reports", key="export_daily_reports")
    
    # Add filter options
    with st.expander("Filter Options"):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Project", ["All Projects", "Highland Tower", "City Center", "Riverside Apartments"])
            st.date_input("From Date", datetime.now() - timedelta(days=30))
        with col2:
            st.selectbox("Foreman", ["All Foremen", "John Smith", "Mary Johnson", "Robert Lee"])
            st.date_input("To Date", datetime.now())
    
    # Sample data for daily reports
    daily_reports = [
        {"id": 1, "date": "2025-05-15", "project": "Highland Tower", "foreman": "John Smith", "weather": "Sunny", "temp": "72°F", "workers": 24},
        {"id": 2, "date": "2025-05-14", "project": "Highland Tower", "foreman": "John Smith", "weather": "Cloudy", "temp": "68°F", "workers": 22},
        {"id": 3, "date": "2025-05-13", "project": "City Center", "foreman": "Mary Johnson", "weather": "Rainy", "temp": "65°F", "workers": 18},
        {"id": 4, "date": "2025-05-12", "project": "Riverside Apartments", "foreman": "Robert Lee", "weather": "Sunny", "temp": "75°F", "workers": 15},
        {"id": 5, "date": "2025-05-11", "project": "City Center", "foreman": "Mary Johnson", "weather": "Partly Cloudy", "temp": "70°F", "workers": 20}
    ]
    
    # Convert to DataFrame for display
    df = pd.DataFrame(daily_reports)
    st.dataframe(df, use_container_width=True)
    
    # Display a sample report detail
    if st.button("View Sample Report Details", key="view_daily_report"):
        st.subheader("Daily Report Details - Highland Tower (May 15, 2025)")
        
        # Report sections
        st.markdown("### Weather Conditions")
        st.markdown("**Weather:** Sunny  \n**Temperature:** 72°F  \n**Wind:** 5 mph NW")
        
        st.markdown("### Labor")
        labor_data = {
            "Trade": ["Carpentry", "Electrical", "Plumbing", "Concrete", "Steel"],
            "Workers": [8, 6, 4, 3, 3],
            "Hours": [64, 48, 32, 24, 24]
        }
        st.dataframe(pd.DataFrame(labor_data))
        
        st.markdown("### Equipment")
        equipment_data = {
            "Equipment": ["Excavator", "Crane", "Loader", "Generator", "Concrete Pump"],
            "Hours": [6, 8, 4, 10, 2]
        }
        st.dataframe(pd.DataFrame(equipment_data))
        
        st.markdown("### Work Completed")
        st.markdown("""
        - Completed framing on floors 12-14
        - Installed electrical rough-in on floor 11
        - Poured concrete for east stairwell
        - Inspected structural steel on floors 15-16
        """)
        
        st.markdown("### Materials Received")
        materials_data = {
            "Material": ["Lumber", "Concrete", "Steel Rebar", "Electrical Conduit"],
            "Quantity": ["2,500 board ft", "28 cubic yards", "3 tons", "1,200 linear ft"]
        }
        st.dataframe(pd.DataFrame(materials_data))
        
        st.markdown("### Notes & Issues")
        st.markdown("""
        Delivery of HVAC equipment delayed by 1 day due to transportation issues.
        Water leak discovered on floor 10, plumbing team investigating source.
        """)

def render_inspections():
    """Render the inspections interface."""
    st.subheader("Inspections")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("Schedule Inspection", key="schedule_inspection")
    with col2:
        st.button("Upload Inspection Report", key="upload_inspection")
    
    # Sample data for inspections
    inspections = [
        {"id": 1, "date": "2025-05-18", "project": "Highland Tower", "type": "Structural", "inspector": "City Building Dept", "status": "Scheduled"},
        {"id": 2, "date": "2025-05-14", "project": "Highland Tower", "type": "Electrical", "inspector": "City Building Dept", "status": "Passed"},
        {"id": 3, "date": "2025-05-10", "project": "City Center", "type": "Plumbing", "inspector": "County Inspector", "status": "Failed"},
        {"id": 4, "date": "2025-05-05", "project": "Riverside Apartments", "type": "Foundation", "inspector": "Third Party", "status": "Passed"},
        {"id": 5, "date": "2025-04-30", "project": "City Center", "type": "Mechanical", "inspector": "City Building Dept", "status": "Passed"}
    ]
    
    # Convert to DataFrame for display
    df = pd.DataFrame(inspections)
    
    # Add status styling
    def status_color(val):
        if val == "Passed":
            return 'background-color: #d1fae5; color: #064e3b'
        elif val == "Failed":
            return 'background-color: #fee2e2; color: #7f1d1d'
        else:
            return 'background-color: #e0f2fe; color: #0c4a6e'
    
    # Apply styling
    styled_df = df.style.applymap(status_color, subset=['status'])
    
    # Display the dataframe
    st.dataframe(styled_df, use_container_width=True)

def render_quality_control():
    """Render the quality control interface."""
    st.subheader("Quality Control")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("New QC Checklist", key="new_qc_checklist")
    with col2:
        st.button("Generate QC Report", key="generate_qc_report")
    
    # Sample QC items with progress tracking
    qc_items = [
        {"category": "Concrete", "item": "Formwork Inspection", "project": "Highland Tower", "status": "Completed", "date": "2025-05-10"},
        {"category": "Concrete", "item": "Rebar Placement Verification", "project": "Highland Tower", "status": "Completed", "date": "2025-05-12"},
        {"category": "Concrete", "item": "Post-Pour Inspection", "project": "Highland Tower", "status": "In Progress", "date": "2025-05-16"},
        {"category": "Structural", "item": "Steel Connection Verification", "project": "City Center", "status": "Completed", "date": "2025-05-08"},
        {"category": "Structural", "item": "Bolting Inspection", "project": "City Center", "status": "In Progress", "date": "2025-05-15"},
        {"category": "MEP", "item": "Ductwork Installation Check", "project": "Riverside Apartments", "status": "Pending", "date": "2025-05-20"},
        {"category": "MEP", "item": "Plumbing Pressure Test", "project": "Riverside Apartments", "status": "Pending", "date": "2025-05-22"}
    ]
    
    # Convert to DataFrame
    qc_df = pd.DataFrame(qc_items)
    
    # Add status styling
    def status_color(val):
        if val == "Completed":
            return 'background-color: #d1fae5; color: #064e3b'
        elif val == "In Progress":
            return 'background-color: #e0f2fe; color: #0c4a6e'
        else:
            return 'background-color: #f5f5f4; color: #44403c'
    
    # Apply styling
    styled_qc_df = qc_df.style.applymap(status_color, subset=['status'])
    
    # Display the dataframe
    st.dataframe(styled_qc_df, use_container_width=True)
    
    # QC Statistics
    st.subheader("Quality Metrics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("QC Items Completed", "28", "+4 this week")
    with col2:
        st.metric("QC Issues Identified", "12", "-2 this week")
    with col3:
        st.metric("Quality Rating", "93%", "+2% this month")

def render_safety_observations():
    """Render the safety observations interface."""
    st.subheader("Safety Observations")
    
    # Add actions row with buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.button("Record Observation", key="new_safety_observation")
    with col2:
        st.button("Safety Report", key="safety_report")
    
    # Sample safety observations
    safety_items = [
        {"id": 1, "date": "2025-05-15", "project": "Highland Tower", "observer": "John Smith", "category": "PPE", "description": "Workers not wearing safety glasses", "severity": "Medium", "status": "Resolved"},
        {"id": 2, "date": "2025-05-14", "project": "City Center", "observer": "Mary Johnson", "category": "Fall Protection", "description": "Missing guardrail on 3rd floor", "severity": "High", "status": "In Progress"},
        {"id": 3, "date": "2025-05-12", "project": "Highland Tower", "observer": "Robert Lee", "category": "Housekeeping", "description": "Debris in walkway area", "severity": "Low", "status": "Resolved"},
        {"id": 4, "date": "2025-05-10", "project": "Riverside Apartments", "observer": "Jane Wilson", "category": "Electrical", "description": "Exposed wiring near water", "severity": "High", "status": "Resolved"},
        {"id": 5, "date": "2025-05-08", "project": "City Center", "observer": "Mark Davis", "category": "Equipment", "description": "Crane not properly secured", "severity": "High", "status": "Resolved"}
    ]
    
    # Convert to DataFrame
    safety_df = pd.DataFrame(safety_items)
    
    # Add styling based on severity
    def severity_color(val):
        if val == "High":
            return 'background-color: #fee2e2; color: #7f1d1d'
        elif val == "Medium":
            return 'background-color: #fef3c7; color: #78350f'
        else:
            return 'background-color: #d1fae5; color: #064e3b'
    
    # Apply styling
    styled_safety_df = safety_df.style.applymap(severity_color, subset=['severity'])
    
    # Display the dataframe
    st.dataframe(styled_safety_df, use_container_width=True)
    
    # Safety Statistics
    st.subheader("Safety Statistics")
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Incident Rate", "1.2", "-0.3 vs last month")
    with col2:
        st.metric("Days Since Last Incident", "42", "+5 since last week")
    with col3:
        st.metric("Safety Observations", "24", "+6 this month")