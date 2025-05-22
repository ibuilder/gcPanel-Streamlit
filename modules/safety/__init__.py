"""
Safety Management Module for gcPanel

This module provides comprehensive safety management functionality including:
- Safety Incidents tracking
- Safety Inspections management
- Hazard identification and mitigation
- Safety metrics and reporting

The module follows the standardized CRUD styling for consistent user experience.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import json

from assets.crud_styler import apply_crud_styles
from modules.crud_template import CrudModule

# Import submodules
from modules.safety.incidents import SafetyIncidentModule
from modules.safety.inspections import SafetyInspectionModule
from modules.safety.hazards import HazardModule

def render_safety_dashboard():
    """Render the safety dashboard with key metrics and charts."""
    st.subheader("Safety Performance Dashboard")
    
    # Apply styling
    apply_crud_styles()
    
    # Create container with white background
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    # Key safety metrics
    st.markdown("### Key Safety Metrics")
    
    # Row 1 Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        days_without_incident = random.randint(25, 45)
        st.metric("Days Without Incident", days_without_incident)
    
    with col2:
        recordable_incidents = random.randint(2, 4)
        st.metric("Recordable Incidents", recordable_incidents, "-1 vs Last Year")
    
    with col3:
        incident_rate = round(recordable_incidents * 200000 / 250000, 2)  # Assuming 250,000 work hours
        st.metric("Incident Rate", incident_rate, "-0.5 vs Target")
    
    with col4:
        safety_training = random.randint(92, 98)
        st.metric("Safety Training", f"{safety_training}%", "+2% vs Last Month")
    
    # Safety incident trend chart
    st.markdown("### Incident Trend")
    
    # Generate sample data for past 12 months
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    incident_counts = [random.randint(0, 3) for _ in range(12)]
    
    # Create pandas DataFrame
    df_incidents = pd.DataFrame({
        'Month': months,
        'Incidents': incident_counts
    })
    
    # Display bar chart
    st.bar_chart(df_incidents.set_index('Month')['Incidents'])
    
    # Safety inspection compliance chart
    st.markdown("### Inspection Compliance")
    
    # Generate sample data for different inspection types
    inspection_types = ["Daily Site Walk", "Weekly Safety Audit", "Monthly Equipment", "Quarterly Compliance"]
    planned_inspections = [20, 4, 2, 1]
    completed_inspections = [random.randint(max(1, planned - 2), planned) for planned in planned_inspections]
    
    # Calculate compliance percentage
    compliance_pct = [round(completed / planned * 100) for completed, planned in zip(completed_inspections, planned_inspections)]
    
    # Create pandas DataFrame
    df_inspections = pd.DataFrame({
        'Type': inspection_types,
        'Planned': planned_inspections,
        'Completed': completed_inspections,
        'Compliance': compliance_pct
    })
    
    # Display as a table
    st.table(df_inspections.style.background_gradient(subset=['Compliance'], cmap='RdYlGn'))
    
    # Close the white container
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Recent hazards container
    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    
    st.markdown("### Recent Hazards")
    
    # Generate sample hazard data
    recent_hazards = [
        {
            "id": "HAZ-001",
            "description": "Exposed electrical wiring near water source",
            "location": "Level 3 - East Wing",
            "severity": "High",
            "status": "Open"
        },
        {
            "id": "HAZ-002",
            "description": "Trip hazard from construction debris",
            "location": "Main Entrance",
            "severity": "Medium",
            "status": "Mitigated"
        },
        {
            "id": "HAZ-003",
            "description": "Missing guardrails on scaffolding",
            "location": "West Facade",
            "severity": "High",
            "status": "Open"
        },
        {
            "id": "HAZ-004",
            "description": "Inadequate ventilation in painting area",
            "location": "Basement - Room B12",
            "severity": "Medium",
            "status": "In Progress"
        }
    ]
    
    # Display hazards with severity indicators
    for hazard in recent_hazards:
        # Determine severity color
        severity_color = {
            "High": "red",
            "Medium": "orange",
            "Low": "blue"
        }.get(hazard["severity"], "gray")
        
        # Determine status color
        status_color = {
            "Open": "red",
            "In Progress": "blue",
            "Mitigated": "green",
            "Closed": "gray"
        }.get(hazard["status"], "gray")
        
        # Create hazard card
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 10px; border: 1px solid #eee; 
                 border-radius: 5px; margin-bottom: 10px; background-color: #f9f9f9;">
            <div style="width: 80px; text-align: center; margin-right: 15px;">
                <div style="padding: 5px; background-color: {severity_color}; color: white; 
                         border-radius: 4px; font-weight: bold;">
                    {hazard["severity"]}
                </div>
            </div>
            <div style="flex-grow: 1;">
                <div><strong>{hazard["id"]}: {hazard["description"]}</strong></div>
                <div>Location: {hazard["location"]}</div>
                <div>Status: <span style="color: {status_color};">{hazard["status"]}</span></div>
            </div>
            <div>
                <button style="background-color: #2196F3; color: white; border: none; 
                         padding: 5px 10px; text-align: center; text-decoration: none; 
                         display: inline-block; font-size: 12px; margin: 4px 2px; 
                         cursor: pointer; border-radius: 4px;">
                    View
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Close the white container
    st.markdown("</div>", unsafe_allow_html=True)

def render():
    """Render the Safety Management module."""
    st.title("Safety Management")
    
    # Create tabs for different safety functions
    tabs = st.tabs(["Dashboard", "Incidents", "Inspections", "Hazards"])
    
    # Dashboard tab
    with tabs[0]:
        render_safety_dashboard()
    
    # Incidents tab
    with tabs[1]:
        incidents_module = SafetyIncidentModule()
        incidents_module.render()
    
    # Inspections tab
    with tabs[2]:
        inspections_module = SafetyInspectionModule()
        inspections_module.render()
    
    # Hazards tab
    with tabs[3]:
        hazards_module = HazardModule()
        hazards_module.render()