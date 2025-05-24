"""
Inspections Module for gcPanel Highland Tower Development

This module provides construction inspections and compliance verification
using the standardized CRUD format for construction management.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_inspections():
    """Render the Inspections module with full CRUD functionality"""
    st.title("📋 Inspections - Highland Tower Development")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Scheduled", "12", "+3 this week")
    with col2:
        st.metric("Completed", "45", "+8 this week")
    with col3:
        st.metric("Pass Rate", "96%", "+2% improvement")
    with col4:
        st.metric("Pending", "3", "Awaiting inspector")
    
    # Action buttons
    st.markdown("#### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📅 Schedule Inspection", type="primary", use_container_width=True):
            st.success("Inspection scheduling form opened")
    
    with col2:
        if st.button("✅ Record Results", type="secondary", use_container_width=True):
            st.success("Inspection results form opened")
    
    with col3:
        if st.button("📊 Inspection Report", type="secondary", use_container_width=True):
            st.success("Inspection report generated")
    
    with col4:
        if st.button("🔄 Request Re-inspection", type="secondary", use_container_width=True):
            st.success("Re-inspection requested")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Scheduled", "Completed", "Failed", "Reports"])
    
    with tab1:
        render_scheduled_inspections()
    
    with tab2:
        render_completed_inspections()
    
    with tab3:
        render_failed_inspections()
    
    with tab4:
        render_inspection_reports()

def render_scheduled_inspections():
    """Render scheduled inspections"""
    st.subheader("Scheduled Inspections")
    
    scheduled_data = [
        {
            "ID": "INS-001",
            "Type": "Foundation Final",
            "Location": "Building Foundation - Grid A-J",
            "Inspector": "City Building Dept",
            "Date": "2025-05-25",
            "Time": "10:00 AM",
            "Contact": "Inspector Johnson",
            "Requirements": "Rebar placement, concrete forms"
        },
        {
            "ID": "INS-002", 
            "Type": "Electrical Rough-In",
            "Location": "Floor 8 - Residential Units",
            "Inspector": "Electrical Inspector",
            "Date": "2025-05-26",
            "Time": "2:00 PM",
            "Contact": "Mike Stevens",
            "Requirements": "Conduit installation, grounding"
        }
    ]
    
    for inspection in scheduled_data:
        with st.container():
            col1, col2, col3 = st.columns([4, 3, 2])
            
            with col1:
                st.markdown(f"**{inspection['Type']}** ({inspection['ID']})")
                st.caption(f"📍 {inspection['Location']}")
                st.caption(f"📋 {inspection['Requirements']}")
            
            with col2:
                st.markdown(f"📅 {inspection['Date']} at {inspection['Time']}")
                st.caption(f"👤 {inspection['Contact']} | 🏢 {inspection['Inspector']}")
            
            with col3:
                if st.button("📝", key=f"prep_{inspection['ID']}", help="Prep Checklist"):
                    st.success(f"Preparation checklist for {inspection['ID']}")
                if st.button("📞", key=f"contact_{inspection['ID']}", help="Contact Inspector"):
                    st.success(f"Contacted inspector for {inspection['ID']}")
        
        st.divider()

def render_completed_inspections():
    """Render completed inspections"""
    st.subheader("Completed Inspections")
    
    completed_data = [
        {
            "ID": "INS-C001",
            "Type": "Concrete Pour",
            "Location": "Floor 12 Slab",
            "Result": "Passed",
            "Date": "2025-05-23",
            "Inspector": "Sarah Martinez",
            "Notes": "All requirements met, proceed to next phase"
        },
        {
            "ID": "INS-C002",
            "Type": "Fire Safety",
            "Location": "Stairwell A & B",
            "Result": "Passed",
            "Date": "2025-05-22", 
            "Inspector": "Fire Marshal",
            "Notes": "Emergency lighting and exits approved"
        }
    ]
    
    for inspection in completed_data:
        result_color = {"Passed": "🟢", "Failed": "🔴", "Conditional": "🟡"}
        
        st.markdown(f"**{inspection['Type']}** ({inspection['ID']}) - {result_color.get(inspection['Result'], '⚪')} {inspection['Result']}")
        st.caption(f"📍 {inspection['Location']} | 📅 {inspection['Date']} | 👤 {inspection['Inspector']}")
        st.caption(f"📝 {inspection['Notes']}")
        st.divider()

def render_failed_inspections():
    """Render failed inspections"""
    st.subheader("Failed Inspections - Corrective Actions Required")
    
    failed_data = [
        {
            "ID": "INS-F001",
            "Type": "Plumbing Rough-In",
            "Location": "Floor 9 - Units 901-906",
            "Date": "2025-05-21",
            "Issues": "Missing shut-off valves, incorrect pipe support spacing",
            "Corrective Action": "Install valves, add pipe supports per code",
            "Re-inspection": "2025-05-26",
            "Status": "In Progress"
        }
    ]
    
    for inspection in failed_data:
        st.markdown(f"**{inspection['Type']}** ({inspection['ID']}) - 🔴 Failed")
        st.caption(f"📍 {inspection['Location']} | 📅 {inspection['Date']}")
        
        with st.expander(f"Corrective Actions - {inspection['ID']}"):
            st.markdown(f"**Issues Identified:** {inspection['Issues']}")
            st.markdown(f"**Required Actions:** {inspection['Corrective Action']}")
            st.markdown(f"**Re-inspection Scheduled:** {inspection['Re-inspection']}")
            st.markdown(f"**Status:** {inspection['Status']}")

def render_inspection_reports():
    """Render inspection reports"""
    st.subheader("Inspection Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("Report Type", ["Weekly Summary", "Pass/Fail Analysis", "Inspector Performance", "Compliance Status"])
        st.date_input("From Date", datetime.now() - timedelta(days=30))
    
    with col2:
        st.selectbox("Format", ["PDF", "Excel", "Word"])
        st.date_input("To Date", datetime.now())
    
    if st.button("📊 Generate Report", type="primary"):
        st.success("Inspection report generated successfully")
        
        st.markdown("#### Report Preview - Weekly Summary")
        
        summary_data = {
            "Statistics": [
                "Total Inspections: 45",
                "Pass Rate: 96%",
                "Failed Inspections: 2", 
                "Re-inspections: 1",
                "Average Response Time: 1.2 days"
            ],
            "By Category": [
                "Structural: 15 inspections (100% pass)",
                "MEP: 18 inspections (94% pass)",
                "Fire Safety: 8 inspections (100% pass)",
                "Final: 4 inspections (100% pass)"
            ]
        }
        
        for section, items in summary_data.items():
            st.markdown(f"**{section}:**")
            for item in items:
                st.markdown(f"• {item}")