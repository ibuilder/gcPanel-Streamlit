"""
Resource Management Module for gcPanel Highland Tower Development

This module provides team coordination, equipment, and material management
using the standardized CRUD format for construction management.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_resource_management():
    """Render the Resource Management module with full CRUD functionality"""
    st.title("👥 Resource Management - Highland Tower Development")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Workers", "127", "+8 this week")
    with col2:
        st.metric("Equipment Utilization", "89%", "+5% efficiency")
    with col3:
        st.metric("Material Orders", "15", "3 pending delivery")
    with col4:
        st.metric("Budget Utilization", "74%", "On track")
    
    # Action buttons
    st.markdown("#### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👷 Add Worker", type="primary", use_container_width=True):
            st.session_state['show_worker_form'] = True
    
    with col2:
        if st.button("🚜 Schedule Equipment", type="secondary", use_container_width=True):
            st.session_state['show_equipment_form'] = True
    
    with col3:
        if st.button("📦 Order Materials", type="secondary", use_container_width=True):
            st.session_state['show_material_form'] = True
    
    with col4:
        if st.button("📊 Resource Report", type="secondary", use_container_width=True):
            st.success("Resource utilization report generated")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Personnel", "Equipment", "Materials", "Analytics"])
    
    with tab1:
        render_personnel_management()
    
    with tab2:
        render_equipment_management()
    
    with tab3:
        render_material_management()
    
    with tab4:
        render_resource_analytics()

def render_personnel_management():
    """Render personnel management with CRUD operations"""
    st.subheader("Personnel Management")
    
    # Filter options
    with st.expander("Filter Personnel"):
        col1, col2, col3 = st.columns(3)
        with col1:
            trade_filter = st.selectbox("Trade", ["All", "Carpentry", "Electrical", "Plumbing", "Concrete", "Steel"])
        with col2:
            status_filter = st.selectbox("Status", ["All", "Active", "On Leave", "Training"])
        with col3:
            crew_filter = st.selectbox("Crew", ["All", "Crew A", "Crew B", "Crew C", "Management"])
    
    # Personnel data
    personnel_data = [
        {
            "ID": "W-001",
            "Name": "John Smith",
            "Trade": "Carpentry",
            "Crew": "Crew A",
            "Status": "Active",
            "Hours This Week": "42",
            "Certification": "Valid",
            "Safety Rating": "A+",
            "Contact": "(555) 123-4567"
        },
        {
            "ID": "W-002",
            "Name": "Sarah Johnson", 
            "Trade": "Electrical",
            "Crew": "Crew B",
            "Status": "Active",
            "Hours This Week": "40",
            "Certification": "Valid",
            "Safety Rating": "A",
            "Contact": "(555) 234-5678"
        },
        {
            "ID": "W-003",
            "Name": "Mike Wilson",
            "Trade": "Plumbing",
            "Crew": "Crew A", 
            "Status": "Training",
            "Hours This Week": "38",
            "Certification": "Pending",
            "Safety Rating": "B+",
            "Contact": "(555) 345-6789"
        }
    ]
    
    # Display personnel
    for person in personnel_data:
        with st.container():
            col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
            
            with col1:
                st.markdown(f"**{person['Name']}** ({person['ID']})")
                st.caption(f"🔧 {person['Trade']} | 👥 {person['Crew']} | 📞 {person['Contact']}")
            
            with col2:
                status_color = {"Active": "🟢", "On Leave": "🟡", "Training": "🔵"}
                st.markdown(f"{status_color.get(person['Status'], '⚪')} {person['Status']}")
                st.caption(f"Hours: {person['Hours This Week']}")
            
            with col3:
                st.markdown(f"Safety: {person['Safety Rating']}")
                st.caption(f"Cert: {person['Certification']}")
            
            with col4:
                if st.button("👁️", key=f"view_person_{person['ID']}", help="View Details"):
                    st.session_state[f"view_person_{person['ID']}"] = True
                if st.button("✏️", key=f"edit_person_{person['ID']}", help="Edit"):
                    st.session_state[f"edit_person_{person['ID']}"] = True
        
        st.divider()

def render_equipment_management():
    """Render equipment management"""
    st.subheader("Equipment Management")
    
    # Equipment data
    equipment_data = [
        {
            "ID": "EQ-001",
            "Equipment": "Tower Crane TC-1",
            "Type": "Heavy Machinery",
            "Status": "In Use",
            "Location": "Floor 12-15",
            "Operator": "David Chen",
            "Hours Today": "8.5",
            "Maintenance Due": "2025-06-01",
            "Utilization": "92%"
        },
        {
            "ID": "EQ-002", 
            "Equipment": "Concrete Pump CP-2",
            "Type": "Concrete Equipment",
            "Status": "Available",
            "Location": "Ground Level",
            "Operator": "Unassigned",
            "Hours Today": "0",
            "Maintenance Due": "2025-05-30",
            "Utilization": "76%"
        },
        {
            "ID": "EQ-003",
            "Equipment": "Generator G-3",
            "Type": "Power Equipment",
            "Status": "Maintenance",
            "Location": "Equipment Yard",
            "Operator": "N/A",
            "Hours Today": "0",
            "Maintenance Due": "In Progress",
            "Utilization": "0%"
        }
    ]
    
    for equipment in equipment_data:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{equipment['Equipment']}** ({equipment['ID']})")
                st.caption(f"📍 {equipment['Location']} | 👤 {equipment['Operator']}")
            
            with col2:
                status_color = {"In Use": "🟢", "Available": "🟡", "Maintenance": "🔴"}
                st.markdown(f"{status_color.get(equipment['Status'], '⚪')} {equipment['Status']}")
                st.caption(f"Utilization: {equipment['Utilization']}")
            
            with col3:
                st.markdown(f"Hours: {equipment['Hours Today']}")
                st.caption(f"Maint Due: {equipment['Maintenance Due']}")
            
            with col4:
                if st.button("📅", key=f"schedule_{equipment['ID']}", help="Schedule"):
                    st.success(f"Equipment {equipment['ID']} scheduled")
                if st.button("🔧", key=f"maintain_{equipment['ID']}", help="Maintenance"):
                    st.success(f"Maintenance logged for {equipment['ID']}")
        
        st.divider()

def render_material_management():
    """Render material management"""
    st.subheader("Material Management")
    
    # Material data
    material_data = [
        {
            "ID": "MAT-001",
            "Material": "Concrete (Ready Mix)",
            "Quantity": "45 cubic yards",
            "Status": "Delivered",
            "Supplier": "Highland Concrete Co.",
            "Delivery Date": "2025-05-24",
            "Location": "Floor 12 Pour",
            "Cost": "$4,950",
            "Quality Check": "Passed"
        },
        {
            "ID": "MAT-002",
            "Material": "Steel Rebar #5",
            "Quantity": "2,500 linear feet", 
            "Status": "In Transit",
            "Supplier": "Metro Steel Supply",
            "Delivery Date": "2025-05-25",
            "Location": "TBD",
            "Cost": "$3,200",
            "Quality Check": "Pending"
        },
        {
            "ID": "MAT-003",
            "Material": "Electrical Conduit",
            "Quantity": "1,800 feet",
            "Status": "Ordered",
            "Supplier": "City Electric Supply",
            "Delivery Date": "2025-05-27",
            "Location": "TBD", 
            "Cost": "$1,875",
            "Quality Check": "N/A"
        }
    ]
    
    for material in material_data:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{material['Material']}** ({material['ID']})")
                st.caption(f"Qty: {material['Quantity']} | 💰 {material['Cost']}")
            
            with col2:
                status_color = {"Delivered": "🟢", "In Transit": "🟡", "Ordered": "🔵"}
                st.markdown(f"{status_color.get(material['Status'], '⚪')} {material['Status']}")
                st.caption(f"📅 {material['Delivery Date']}")
            
            with col3:
                st.markdown(f"📍 {material['Location']}")
                st.caption(f"QC: {material['Quality Check']}")
            
            with col4:
                if st.button("📦", key=f"receive_{material['ID']}", help="Mark Received"):
                    st.success(f"Material {material['ID']} marked as received")
                if st.button("✅", key=f"qc_{material['ID']}", help="Quality Check"):
                    st.success(f"Quality check completed for {material['ID']}")
        
        st.divider()

def render_resource_analytics():
    """Render resource analytics and reports"""
    st.subheader("Resource Analytics")
    
    # Analytics tabs
    tab1, tab2, tab3 = st.tabs(["Utilization", "Costs", "Performance"])
    
    with tab1:
        st.markdown("#### Resource Utilization")
        
        # Sample utilization data
        util_data = {
            "Resource Type": ["Personnel", "Equipment", "Materials"],
            "Current Utilization": [89, 76, 94],
            "Target Utilization": [85, 80, 90],
            "Variance": ["+4%", "-4%", "+4%"]
        }
        
        df_util = pd.DataFrame(util_data)
        st.dataframe(df_util, use_container_width=True)
        
        # Weekly trend
        st.markdown("#### Weekly Utilization Trend")
        trend_data = {
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "Personnel": [82, 85, 87, 89],
            "Equipment": [78, 74, 76, 76],
            "Materials": [90, 92, 93, 94]
        }
        
        df_trend = pd.DataFrame(trend_data)
        st.line_chart(df_trend.set_index("Week"))
    
    with tab2:
        st.markdown("#### Cost Analysis")
        
        cost_data = {
            "Category": ["Labor", "Equipment Rental", "Materials", "Overhead"],
            "Budgeted": [185000, 125000, 275000, 65000],
            "Actual": [178000, 132000, 267000, 61000],
            "Variance": [-7000, 7000, -8000, -4000]
        }
        
        df_cost = pd.DataFrame(cost_data)
        st.dataframe(df_cost, use_container_width=True)
        
        # Cost breakdown chart
        st.bar_chart(df_cost.set_index("Category")[["Budgeted", "Actual"]])
    
    with tab3:
        st.markdown("#### Performance Metrics")
        
        perf_data = {
            "Metric": ["Productivity Index", "Safety Score", "Quality Rating", "Schedule Adherence"],
            "Current": ["112%", "98%", "94%", "102%"],
            "Target": ["100%", "95%", "90%", "100%"],
            "Trend": ["↗️", "→", "↗️", "↗️"]
        }
        
        df_perf = pd.DataFrame(perf_data)
        st.dataframe(df_perf, use_container_width=True)