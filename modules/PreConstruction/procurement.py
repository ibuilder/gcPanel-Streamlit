"""
Procurement Module

This module provides tools for procurement management, including:
- Purchase order tracking
- Material procurement planning
- Vendor management
- Lead time tracking
- Delivery scheduling
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_procurement():
    """Render the Procurement dashboard"""
    st.header("Procurement Management")
    
    # Create tabs for different procurement sections
    tabs = st.tabs([
        "Procurement Dashboard", 
        "Purchase Orders", 
        "Material Tracking", 
        "Vendor Management"
    ])
    
    # Procurement dashboard tab
    with tabs[0]:
        render_procurement_dashboard()
    
    # Purchase orders tab
    with tabs[1]:
        render_purchase_orders()
    
    # Material tracking tab
    with tabs[2]:
        render_material_tracking()
    
    # Vendor management tab
    with tabs[3]:
        render_vendor_management()

def render_procurement_dashboard():
    """Render the procurement dashboard section"""
    # Create layout columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Procurement status metrics
        status_col1, status_col2, status_col3, status_col4 = st.columns(4)
        
        with status_col1:
            st.metric(
                label="Open POs",
                value="42",
                help="Number of open purchase orders"
            )
        
        with status_col2:
            st.metric(
                label="Total Value",
                value="$12.5M",
                help="Total value of all purchase orders"
            )
        
        with status_col3:
            st.metric(
                label="Critical Items",
                value="8",
                delta="-2",
                delta_color="inverse",
                help="Number of critical procurement items"
            )
        
        with status_col4:
            st.metric(
                label="Avg Lead Time",
                value="12.5 wks",
                delta="-1.2 wks",
                delta_color="inverse",
                help="Average lead time across all procurement items"
            )
        
        # Procurement status chart
        st.markdown("#### Procurement Status")
        
        status_data = pd.DataFrame({
            "Status": ["Not Started", "In Progress", "Ordered", "In Fabrication", "Ready to Ship", "Delivered"],
            "Count": [8, 12, 15, 6, 4, 5]
        })
        
        fig = px.bar(
            status_data,
            x="Status",
            y="Count",
            color="Status",
            color_discrete_map={
                "Not Started": "#6c757d",
                "In Progress": "#4a90e2",
                "Ordered": "#f59e0b", 
                "In Fabrication": "#9c27b0",
                "Ready to Ship": "#3f51b5",
                "Delivered": "#38d39f"
            },
            labels={"Count": "Number of Items"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Upcoming deliveries
        st.markdown("#### Upcoming Deliveries")
        
        upcoming_deliveries = [
            {"item": "Curtain Wall - North Elevation", "vendor": "Skyline Glass", "delivery_date": "May 28, 2025", "days_away": 6, "status": "In Fabrication"},
            {"item": "Electrical Switchgear", "vendor": "Alliance Electric", "delivery_date": "Jun 3, 2025", "days_away": 12, "status": "Ordered"},
            {"item": "Air Handling Units", "vendor": "Modern Mechanical", "delivery_date": "Jun 10, 2025", "days_away": 19, "status": "In Fabrication"},
            {"item": "Elevator Equipment", "vendor": "Otis Elevator", "delivery_date": "Jun 15, 2025", "days_away": 24, "status": "In Fabrication"},
            {"item": "Fire Pump System", "vendor": "Fire Systems Inc", "delivery_date": "Jun 22, 2025", "days_away": 31, "status": "Ordered"}
        ]
        
        for delivery in upcoming_deliveries:
            days_color = "#ef4444" if delivery["days_away"] < 7 else "#f59e0b" if delivery["days_away"] < 14 else "#38d39f"
            status_color = "#6c757d"
            if delivery["status"] == "In Fabrication":
                status_color = "#9c27b0"
            elif delivery["status"] == "Ordered":
                status_color = "#f59e0b"
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 10px; margin-bottom: 8px; background-color: #f8f9fa; border-radius: 4px;">
                <div>
                    <div style="font-weight: 500;">{delivery["item"]}</div>
                    <div style="font-size: 13px; color: #6c757d;">{delivery["vendor"]} • Due: {delivery["delivery_date"]}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 500; color: {days_color};">{delivery["days_away"]} days away</div>
                    <div style="font-size: 13px; color: {status_color};">{delivery["status"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Procurement by Division")
        
        # Package distribution by division
        division_data = pd.DataFrame({
            "Division": ["Div 03-05: Structure", "Div 06-09: Interiors", "Div 21-23: Mechanical", "Div 26-28: Electrical", "Other Divisions"],
            "Value": [4200000, 2800000, 3100000, 1950000, 450000]
        })
        
        fig = px.pie(
            division_data,
            values="Value",
            names="Division",
            hole=0.4,
            labels={"Value": "Procurement Value ($)"}
        )
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        
        # Lead time by division
        st.markdown("#### Average Lead Times")
        
        lead_times = pd.DataFrame({
            "Division": ["Div 03-05: Structure", "Div 06-09: Interiors", "Div 21-23: Mechanical", "Div 26-28: Electrical", "Other Divisions"],
            "Weeks": [8, 6, 16, 14, 10]
        })
        
        fig = px.bar(
            lead_times,
            y="Division",
            x="Weeks",
            orientation="h",
            labels={"Weeks": "Lead Time (weeks)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Critical items
        st.markdown("#### Critical Procurement Items")
        
        critical_items = [
            {"item": "Custom Curtain Wall System", "lead_time": "20 weeks", "impact": "Envelope closure critical path"},
            {"item": "Main Electrical Switchgear", "lead_time": "24 weeks", "impact": "Impacts MEP rough-in start"},
            {"item": "Elevators", "lead_time": "30 weeks", "impact": "Affects construction transportation"},
            {"item": "Roof Top Units (HVAC)", "lead_time": "18 weeks", "impact": "Required for HVAC system testing"}
        ]
        
        for item in critical_items:
            st.markdown(f"""
            <div style="padding: 10px; margin-bottom: 8px; background-color: #feecf0; border-left: 3px solid #ef4444; border-radius: 4px;">
                <div style="font-weight: 500;">{item["item"]}</div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 4px;">
                    <span>Lead Time: {item["lead_time"]}</span>
                </div>
                <div style="font-size: 13px; color: #6c757d; margin-top: 4px;">
                    {item["impact"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_purchase_orders():
    """Render the purchase orders section"""
    st.subheader("Purchase Orders")
    
    # Filter controls
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([2, 2, 2, 1])
    
    with filter_col1:
        status_filter = st.multiselect(
            "Status",
            options=["Draft", "Issued", "Acknowledged", "In Progress", "Complete"],
            default=["Issued", "Acknowledged", "In Progress"],
            key="procurement_status_filter"
        )
    
    with filter_col2:
        division_filter = st.multiselect(
            "Division",
            options=["Div 03-05", "Div 06-09", "Div 21-23", "Div 26-28", "Other"],
            default=[],
            key="procurement_division_filter"
        )
    
    with filter_col3:
        sort_by = st.selectbox(
            "Sort By",
            options=["PO Number", "Issue Date", "Vendor", "Value", "Status"]
        )
    
    with filter_col4:
        st.markdown("<br>", unsafe_allow_html=True)
        show_all = st.checkbox("Show All", value=False, key="procurement_show_all")
    
    # Create purchase order data
    purchase_orders = [
        {
            "po_number": "PO-2025-001",
            "vendor": "Highland Concrete",
            "description": "Concrete Supply for Foundations",
            "division": "Div 03-05",
            "value": 980000,
            "issue_date": "Feb 10, 2025",
            "delivery_date": "Mar 15, 2025",
            "status": "Complete"
        },
        {
            "po_number": "PO-2025-002",
            "vendor": "Metro Steel Erectors",
            "description": "Structural Steel Package",
            "division": "Div 03-05",
            "value": 4750000,
            "issue_date": "Feb 25, 2025",
            "delivery_date": "May 10, 2025",
            "status": "In Progress"
        },
        {
            "po_number": "PO-2025-003",
            "vendor": "Quality Masonry",
            "description": "Masonry Materials & Labor",
            "division": "Div 03-05",
            "value": 1180000,
            "issue_date": "Mar 5, 2025",
            "delivery_date": "Apr 20, 2025",
            "status": "Complete"
        },
        {
            "po_number": "PO-2025-004",
            "vendor": "Premier Roofing",
            "description": "Roofing System",
            "division": "Div 06-09",
            "value": 1580000,
            "issue_date": "Mar 25, 2025",
            "delivery_date": "May 15, 2025",
            "status": "In Progress"
        },
        {
            "po_number": "PO-2025-005",
            "vendor": "Skyline Glass",
            "description": "Curtain Wall Package",
            "division": "Div 06-09",
            "value": 3825000,
            "issue_date": "Apr 10, 2025",
            "delivery_date": "Aug 15, 2025",
            "status": "Acknowledged"
        },
        {
            "po_number": "PO-2025-006",
            "vendor": "Alliance Electric",
            "description": "Electrical Package",
            "division": "Div 26-28",
            "value": 2950000,
            "issue_date": "Apr 15, 2025",
            "delivery_date": "Jul 30, 2025",
            "status": "Issued"
        },
        {
            "po_number": "PO-2025-007",
            "vendor": "Modern Mechanical",
            "description": "HVAC Equipment",
            "division": "Div 21-23",
            "value": 1850000,
            "issue_date": "Apr 20, 2025",
            "delivery_date": "Aug 10, 2025",
            "status": "Acknowledged"
        },
        {
            "po_number": "PO-2025-008",
            "vendor": "Citywide Plumbing",
            "description": "Plumbing Package",
            "division": "Div 21-23",
            "value": 1450000,
            "issue_date": "Apr 25, 2025",
            "delivery_date": "Jul 20, 2025",
            "status": "Issued"
        },
        {
            "po_number": "PO-2025-009",
            "vendor": "Fire Systems Inc",
            "description": "Fire Protection System",
            "division": "Div 21-23",
            "value": 850000,
            "issue_date": "Apr 30, 2025",
            "delivery_date": "Jul 15, 2025",
            "status": "Issued"
        },
        {
            "po_number": "PO-2025-010",
            "vendor": "Otis Elevator",
            "description": "Elevator Package",
            "division": "Other",
            "value": 1250000,
            "issue_date": "May 5, 2025",
            "delivery_date": "Dec 10, 2025",
            "status": "Acknowledged"
        },
        {
            "po_number": "PO-2025-011",
            "vendor": "Precision Panels",
            "description": "Metal Panel System",
            "division": "Div 06-09",
            "value": 1180000,
            "issue_date": "May 10, 2025",
            "delivery_date": "Aug 5, 2025",
            "status": "Draft"
        },
        {
            "po_number": "PO-2025-012",
            "vendor": "Premier Drywall",
            "description": "Drywall Package",
            "division": "Div 06-09",
            "value": 2250000,
            "issue_date": "May 15, 2025",
            "delivery_date": "Aug 20, 2025",
            "status": "Draft"
        }
    ]
    
    # Apply filters
    filtered_pos = purchase_orders
    if not show_all:
        if status_filter:
            filtered_pos = [p for p in filtered_pos if p["status"] in status_filter]
        if division_filter:
            filtered_pos = [p for p in filtered_pos if any(d in p["division"] for d in division_filter)]
    
    # Sort purchase orders
    if sort_by == "PO Number":
        filtered_pos = sorted(filtered_pos, key=lambda x: x["po_number"])
    elif sort_by == "Issue Date":
        # Simple string sort - in a real app, would parse dates
        filtered_pos = sorted(filtered_pos, key=lambda x: x["issue_date"])
    elif sort_by == "Vendor":
        filtered_pos = sorted(filtered_pos, key=lambda x: x["vendor"])
    elif sort_by == "Value":
        filtered_pos = sorted(filtered_pos, key=lambda x: x["value"], reverse=True)
    elif sort_by == "Status":
        status_order = {"Complete": 0, "In Progress": 1, "Acknowledged": 2, "Issued": 3, "Draft": 4}
        filtered_pos = sorted(filtered_pos, key=lambda x: status_order.get(x["status"], 5))
    
    # Display purchase orders
    st.write(f"Showing {len(filtered_pos)} of {len(purchase_orders)} purchase orders")
    
    for po in filtered_pos:
        # Set colors based on status
        status_color = "#6c757d"  # Default gray
        if po["status"] == "Complete":
            status_color = "#38d39f"  # Green
        elif po["status"] == "In Progress":
            status_color = "#9c27b0"  # Purple
        elif po["status"] == "Acknowledged":
            status_color = "#4a90e2"  # Blue
        elif po["status"] == "Issued":
            status_color = "#f59e0b"  # Orange
        elif po["status"] == "Draft":
            status_color = "#6c757d"  # Gray
        
        with st.expander(f"{po['po_number']} - {po['description']} (${po['value']:,})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <span style="font-weight: 500; font-size: 16px;">{po['po_number']}: {po['description']}</span>
                    <span style="margin-left: 10px; color: {status_color};">{po['status']}</span>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong>Vendor:</strong> {po['vendor']}
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong>Division:</strong> {po['division']}
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span><strong>Issue Date:</strong> {po['issue_date']}</span>
                    <span><strong>Delivery Date:</strong> {po['delivery_date']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 10px;">
                    <div style="font-size: 14px; color: #6c757d;">PO Value</div>
                    <div style="font-size: 18px; font-weight: 500;">${po['value']:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Action buttons based on status
            if po["status"] == "Draft":
                col1, col2 = st.columns(2)
                with col1:
                    st.button(f"Edit {po['po_number']}", key=f"edit_{po['po_number']}")
                with col2:
                    st.button(f"Issue {po['po_number']}", key=f"issue_{po['po_number']}")
            
            elif po["status"] == "Issued":
                col1, col2 = st.columns(2)
                with col1:
                    st.button(f"Mark Acknowledged {po['po_number']}", key=f"ack_{po['po_number']}")
                with col2:
                    st.button(f"View PDF {po['po_number']}", key=f"pdf_{po['po_number']}")
            
            else:
                st.button(f"View Details {po['po_number']}", key=f"view_{po['po_number']}")
    
    # Create new PO button
    st.button("Create New Purchase Order", key="new_po")

def render_material_tracking():
    """Render the material tracking section"""
    st.subheader("Material Tracking")
    
    # Create tabs for different material tracking views
    tabs = st.tabs([
        "Material Status", 
        "Lead Time Analysis", 
        "Delivery Schedule"
    ])
    
    # Material status tab
    with tabs[0]:
        st.markdown("#### Material Status Overview")
        
        # Filter controls
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            status_filter = st.multiselect(
                "Status",
                options=["Not Started", "On Order", "In Fabrication", "Ready to Ship", "In Transit", "Delivered", "Installed"],
                default=["On Order", "In Fabrication", "Ready to Ship", "In Transit"]
            )
        
        with filter_col2:
            type_filter = st.multiselect(
                "Material Type",
                options=["Structural", "Envelope", "MEP", "Finishes", "Equipment"],
                default=[]
            )
        
        # Create material tracking data
        materials = [
            {
                "id": "MAT-001",
                "name": "Structural Steel - Main Frame",
                "type": "Structural",
                "vendor": "Metro Steel Erectors",
                "po_number": "PO-2025-002",
                "order_date": "Feb 25, 2025",
                "required_date": "May 10, 2025",
                "estimated_delivery": "May 5, 2025",
                "status": "In Fabrication",
                "critical": True
            },
            {
                "id": "MAT-002",
                "name": "Concrete - 5000 PSI Mix",
                "type": "Structural",
                "vendor": "Highland Concrete",
                "po_number": "PO-2025-001",
                "order_date": "Feb 10, 2025",
                "required_date": "Mar 15, 2025",
                "estimated_delivery": "Mar 15, 2025",
                "status": "Delivered",
                "critical": False
            },
            {
                "id": "MAT-003",
                "name": "Curtain Wall System - North/East",
                "type": "Envelope",
                "vendor": "Skyline Glass",
                "po_number": "PO-2025-005",
                "order_date": "Apr 10, 2025",
                "required_date": "Aug 15, 2025",
                "estimated_delivery": "Aug 10, 2025",
                "status": "In Fabrication",
                "critical": True
            },
            {
                "id": "MAT-004",
                "name": "Curtain Wall System - South/West",
                "type": "Envelope",
                "vendor": "Skyline Glass",
                "po_number": "PO-2025-005",
                "order_date": "Apr 10, 2025",
                "required_date": "Sep 5, 2025",
                "estimated_delivery": "Aug 25, 2025",
                "status": "On Order",
                "critical": True
            },
            {
                "id": "MAT-005",
                "name": "Roofing System - TPO",
                "type": "Envelope",
                "vendor": "Premier Roofing",
                "po_number": "PO-2025-004",
                "order_date": "Mar 25, 2025",
                "required_date": "May 15, 2025",
                "estimated_delivery": "May 12, 2025",
                "status": "Ready to Ship",
                "critical": False
            },
            {
                "id": "MAT-006",
                "name": "Air Handling Units",
                "type": "MEP",
                "vendor": "Modern Mechanical",
                "po_number": "PO-2025-007",
                "order_date": "Apr 20, 2025",
                "required_date": "Aug 10, 2025",
                "estimated_delivery": "Aug 5, 2025",
                "status": "In Fabrication",
                "critical": True
            },
            {
                "id": "MAT-007",
                "name": "Main Electrical Switchgear",
                "type": "MEP",
                "vendor": "Alliance Electric",
                "po_number": "PO-2025-006",
                "order_date": "Apr 15, 2025",
                "required_date": "Jul 30, 2025",
                "estimated_delivery": "Jul 25, 2025",
                "status": "On Order",
                "critical": True
            },
            {
                "id": "MAT-008",
                "name": "Plumbing Fixtures",
                "type": "MEP",
                "vendor": "Citywide Plumbing",
                "po_number": "PO-2025-008",
                "order_date": "Apr 25, 2025",
                "required_date": "Jul 20, 2025",
                "estimated_delivery": "Jul 15, 2025",
                "status": "On Order",
                "critical": False
            },
            {
                "id": "MAT-009",
                "name": "Fire Suppression System",
                "type": "MEP",
                "vendor": "Fire Systems Inc",
                "po_number": "PO-2025-009",
                "order_date": "Apr 30, 2025",
                "required_date": "Jul 15, 2025",
                "estimated_delivery": "Jul 10, 2025",
                "status": "On Order",
                "critical": False
            },
            {
                "id": "MAT-010",
                "name": "Elevators",
                "type": "Equipment",
                "vendor": "Otis Elevator",
                "po_number": "PO-2025-010",
                "order_date": "May 5, 2025",
                "required_date": "Dec 10, 2025",
                "estimated_delivery": "Dec 5, 2025",
                "status": "On Order",
                "critical": True
            },
            {
                "id": "MAT-011",
                "name": "Metal Panels",
                "type": "Envelope",
                "vendor": "Precision Panels",
                "po_number": "PO-2025-011",
                "order_date": "May 10, 2025",
                "required_date": "Aug 5, 2025",
                "estimated_delivery": "Aug 1, 2025",
                "status": "Not Started",
                "critical": False
            },
            {
                "id": "MAT-012",
                "name": "Interior Doors",
                "type": "Finishes",
                "vendor": "TBD",
                "po_number": "TBD",
                "order_date": "TBD",
                "required_date": "Sep 15, 2025",
                "estimated_delivery": "TBD",
                "status": "Not Started",
                "critical": False
            }
        ]
        
        # Apply filters
        filtered_materials = materials
        if status_filter:
            filtered_materials = [m for m in filtered_materials if m["status"] in status_filter]
        if type_filter:
            filtered_materials = [m for m in filtered_materials if m["type"] in type_filter]
        
        # Display materials as cards
        col1, col2 = st.columns(2)
        
        # Distribute cards between columns
        for i, material in enumerate(filtered_materials):
            col = col1 if i % 2 == 0 else col2
            
            with col:
                # Set colors based on status
                status_color = "#6c757d"  # Default gray
                if material["status"] == "Delivered":
                    status_color = "#38d39f"  # Green
                elif material["status"] == "In Transit":
                    status_color = "#3f51b5"  # Indigo
                elif material["status"] == "Ready to Ship":
                    status_color = "#4a90e2"  # Blue
                elif material["status"] == "In Fabrication":
                    status_color = "#9c27b0"  # Purple
                elif material["status"] == "On Order":
                    status_color = "#f59e0b"  # Orange
                elif material["status"] == "Not Started":
                    status_color = "#6c757d"  # Gray
                
                # Set critical flag
                critical_badge = ""
                if material["critical"]:
                    critical_badge = '<span style="background-color: #ef4444; color: white; padding: 2px 6px; border-radius: 10px; font-size: 11px; margin-left: 10px;">CRITICAL</span>'
                
                # Create the card
                st.markdown(f"""
                <div style="margin-bottom: 15px; padding: 15px; background-color: #f8f9fa; border-left: 3px solid {status_color}; border-radius: 5px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: 500;">{material['id']}: {material['name']}{critical_badge}</span>
                        <span style="color: {status_color};">{material['status']}</span>
                    </div>
                    <div style="font-size: 14px; margin-top: 8px;">
                        <span><strong>Vendor:</strong> {material['vendor']}</span>
                    </div>
                    <div style="font-size: 14px; margin-top: 4px;">
                        <span><strong>Type:</strong> {material['type']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 4px;">
                        <span><strong>PO:</strong> {material['po_number']}</span>
                        <span><strong>Order Date:</strong> {material['order_date']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 4px;">
                        <span><strong>Required:</strong> {material['required_date']}</span>
                        <span><strong>Est. Delivery:</strong> {material['estimated_delivery']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Material status summary
        st.markdown("#### Material Status Summary")
        
        # Count materials by status
        status_counts = {}
        for material in materials:
            if material["status"] in status_counts:
                status_counts[material["status"]] += 1
            else:
                status_counts[material["status"]] = 1
        
        status_df = pd.DataFrame({
            "Status": list(status_counts.keys()),
            "Count": list(status_counts.values())
        })
        
        fig = px.pie(
            status_df,
            values="Count",
            names="Status",
            hole=0.4
        )
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
    
    # Lead time analysis tab
    with tabs[1]:
        st.markdown("#### Lead Time Analysis")
        
        # Create lead time data
        lead_time_data = [
            {"category": "Structural Steel", "lead_time": 10, "trend": -1},
            {"category": "Concrete", "lead_time": 2, "trend": 0},
            {"category": "Curtain Wall", "lead_time": 18, "trend": 2},
            {"category": "Roofing", "lead_time": 8, "trend": 0},
            {"category": "HVAC Equipment", "lead_time": 16, "trend": 1},
            {"category": "Electrical Equipment", "lead_time": 14, "trend": 2},
            {"category": "Plumbing Fixtures", "lead_time": 10, "trend": 0},
            {"category": "Elevators", "lead_time": 30, "trend": 4},
            {"category": "Metal Panels", "lead_time": 12, "trend": 0},
            {"category": "Interior Finishes", "lead_time": 6, "trend": -1}
        ]
        
        lead_time_df = pd.DataFrame(lead_time_data)
        
        # Sort by lead time
        lead_time_df = lead_time_df.sort_values("lead_time", ascending=False)
        
        # Create a horizontal bar chart
        fig = px.bar(
            lead_time_df,
            y="category",
            x="lead_time",
            orientation="h",
            labels={"category": "Material Category", "lead_time": "Lead Time (weeks)"},
            color="trend",
            color_continuous_scale=["green", "yellow", "red"],
            range_color=[-2, 4]
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Trend explanation
        st.info("""
        **Lead Time Trend Legend:**
        
        * **Negative Values (Green)**: Lead times are decreasing
        * **Zero (Yellow)**: Lead times are stable
        * **Positive Values (Red)**: Lead times are increasing
        
        Industry analysis shows that MEP equipment and elevator lead times continue to
        increase due to high demand and supply chain constraints.
        """)
        
        # Lead time factors
        st.markdown("#### Lead Time Factors")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Increasing Lead Times**")
            
            increasing_items = [
                {"item": "Elevators", "factor": "High industry demand, component shortages"},
                {"item": "Curtain Wall", "factor": "Material shortages, labor limitations"},
                {"item": "Electrical Equipment", "factor": "Semiconductor shortages"},
                {"item": "HVAC Equipment", "factor": "Manufacturing constraints, high demand"}
            ]
            
            for item in increasing_items:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                    <span><strong>{item['item']}</strong></span>
                    <span style="color: #6c757d; text-align: right;">{item['factor']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Decreasing Lead Times**")
            
            decreasing_items = [
                {"item": "Structural Steel", "factor": "Improving supply chains, lower demand"},
                {"item": "Interior Finishes", "factor": "Increased production capacity"}
            ]
            
            for item in decreasing_items:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                    <span><strong>{item['item']}</strong></span>
                    <span style="color: #6c757d; text-align: right;">{item['factor']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Critical path impact
        st.markdown("#### Critical Path Impact Analysis")
        
        critical_path_items = [
            {
                "item": "Curtain Wall System",
                "impact": "Dictates building envelope completion and interior fitout start",
                "mitigation": "Early PO, fabrication slots reserved, transport fast-tracked"
            },
            {
                "item": "Main Electrical Switchgear",
                "impact": "Required for permanent power and MEP system testing",
                "mitigation": "Early order placement, expedited engineering reviews, temp solutions prepared"
            },
            {
                "item": "Elevators",
                "impact": "Affects construction material movement and final occupancy",
                "mitigation": "Order placed with 30-week lead time, temporary hoists planned for construction"
            }
        ]
        
        for item in critical_path_items:
            st.markdown(f"""
            <div style="margin-bottom: 15px; padding: 15px; background-color: #feecf0; border-left: 3px solid #ef4444; border-radius: 5px;">
                <div style="font-weight: 500;">{item['item']}</div>
                <div style="font-size: 14px; margin-top: 8px;">
                    <strong>Impact:</strong> {item['impact']}
                </div>
                <div style="font-size: 14px; margin-top: 5px;">
                    <strong>Mitigation Strategy:</strong> {item['mitigation']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Delivery schedule tab
    with tabs[2]:
        st.markdown("#### Delivery Schedule")
        
        # Simple date control
        view_month = st.selectbox(
            "View Month",
            options=["May 2025", "June 2025", "July 2025", "August 2025", "September 2025", "Later"]
        )
        
        # Create delivery schedule data
        deliveries = []
        
        if view_month == "May 2025":
            deliveries = [
                {"date": "May 5, 2025", "item": "Structural Steel - Level 5-8", "vendor": "Metro Steel Erectors", "status": "Confirmed"},
                {"date": "May 12, 2025", "item": "Roofing System - TPO", "vendor": "Premier Roofing", "status": "Confirmed"},
                {"date": "May 20, 2025", "item": "Concrete - Final Pour", "vendor": "Highland Concrete", "status": "Tentative"}
            ]
        elif view_month == "June 2025":
            deliveries = [
                {"date": "Jun 5, 2025", "item": "Fire Pump System", "vendor": "Fire Systems Inc", "status": "Tentative"},
                {"date": "Jun 15, 2025", "item": "Mechanical Equipment - Phase 1", "vendor": "Modern Mechanical", "status": "Tentative"}
            ]
        elif view_month == "July 2025":
            deliveries = [
                {"date": "Jul 10, 2025", "item": "Fire Suppression System", "vendor": "Fire Systems Inc", "status": "Tentative"},
                {"date": "Jul 15, 2025", "item": "Plumbing Fixtures - Batch 1", "vendor": "Citywide Plumbing", "status": "Tentative"},
                {"date": "Jul 25, 2025", "item": "Main Electrical Switchgear", "vendor": "Alliance Electric", "status": "Tentative"}
            ]
        elif view_month == "August 2025":
            deliveries = [
                {"date": "Aug 1, 2025", "item": "Metal Panels", "vendor": "Precision Panels", "status": "Tentative"},
                {"date": "Aug 5, 2025", "item": "Air Handling Units", "vendor": "Modern Mechanical", "status": "Tentative"},
                {"date": "Aug 10, 2025", "item": "Curtain Wall - North/East", "vendor": "Skyline Glass", "status": "Tentative"},
                {"date": "Aug 25, 2025", "item": "Curtain Wall - South/West", "vendor": "Skyline Glass", "status": "Tentative"}
            ]
        elif view_month == "Later":
            deliveries = [
                {"date": "Sep 15, 2025", "item": "Interior Doors", "vendor": "TBD", "status": "Planning"},
                {"date": "Dec 5, 2025", "item": "Elevators", "vendor": "Otis Elevator", "status": "Tentative"}
            ]
        
        # Create a table view of deliveries
        if deliveries:
            for delivery in deliveries:
                status_color = "#4a90e2" if delivery["status"] == "Confirmed" else "#f59e0b" if delivery["status"] == "Tentative" else "#6c757d"
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 10px; margin-bottom: 8px; background-color: #f8f9fa; border-radius: 4px;">
                    <div>
                        <div style="font-weight: 500;">{delivery['item']}</div>
                        <div style="font-size: 13px; color: #6c757d;">{delivery['vendor']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 500;">{delivery['date']}</div>
                        <div style="font-size: 13px; color: {status_color};">{delivery['status']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No deliveries scheduled for this month.")
        
        # Gantt chart for deliveries
        st.markdown("#### Delivery Timeline")
        
        # Create a simplified timeline view using a scatter plot
        timeline_data = [
            {"item": "Structural Steel", "start_date": "2025-05-05", "delivery_date": "2025-05-05"},
            {"item": "Roofing System", "start_date": "2025-05-12", "delivery_date": "2025-05-12"},
            {"item": "Fire Pump System", "start_date": "2025-06-05", "delivery_date": "2025-06-05"},
            {"item": "Mechanical Equipment", "start_date": "2025-06-15", "delivery_date": "2025-06-15"},
            {"item": "Fire Suppression", "start_date": "2025-07-10", "delivery_date": "2025-07-10"},
            {"item": "Plumbing Fixtures", "start_date": "2025-07-15", "delivery_date": "2025-07-15"},
            {"item": "Electrical Switchgear", "start_date": "2025-07-25", "delivery_date": "2025-07-25"},
            {"item": "Metal Panels", "start_date": "2025-08-01", "delivery_date": "2025-08-01"},
            {"item": "Air Handling Units", "start_date": "2025-08-05", "delivery_date": "2025-08-05"},
            {"item": "Curtain Wall - N/E", "start_date": "2025-08-10", "delivery_date": "2025-08-10"},
            {"item": "Curtain Wall - S/W", "start_date": "2025-08-25", "delivery_date": "2025-08-25"},
            {"item": "Interior Doors", "start_date": "2025-09-15", "delivery_date": "2025-09-15"},
            {"item": "Elevators", "start_date": "2025-12-05", "delivery_date": "2025-12-05"}
        ]
        
        # Convert to pandas DataFrame
        timeline_df = pd.DataFrame(timeline_data)
        
        # Create figure
        fig = px.scatter(
            timeline_df,
            y="item",
            x="delivery_date",
            labels={"item": "Material", "delivery_date": "Delivery Date"},
            title="Material Delivery Schedule",
            height=400
        )
        
        # Update marker style
        fig.update_traces(marker=dict(size=12, symbol="diamond"))
        
        # Add vertical line for today
        fig.add_vline(
            x="2025-05-22",
            line_dash="dash",
            line_color="red",
            annotation_text="Today",
            annotation_position="top"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Delivery coordination
        st.markdown("#### Delivery Coordination Notes")
        
        st.markdown("""
        **Coordination Requirements:**
        
        * All deliveries must be scheduled at least 48 hours in advance
        * Large deliveries (trucks requiring street closure) must be scheduled 1 week in advance
        * Delivery hours: Monday-Friday, 7:00 AM - 3:00 PM
        * Weekend deliveries require special approval and coordination
        * Tower crane coordination required for all large material lifts
        
        **Material Storage Notes:**
        
        * Limited on-site storage available - just-in-time delivery preferred
        * Level 3 designated as material staging area for interior finishes
        * Coordinate with Superintendent for all material storage requirements
        """)

def render_vendor_management():
    """Render the vendor management section"""
    st.subheader("Vendor Management")
    
    # Create tabs for vendor management
    tabs = st.tabs([
        "Vendor Directory", 
        "Performance Metrics", 
        "Communication Log"
    ])
    
    # Vendor directory tab
    with tabs[0]:
        st.markdown("#### Vendor Directory")
        
        # Filter controls
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            category_filter = st.multiselect(
                "Category",
                options=["Structural", "Envelope", "MEP", "Finishes", "Equipment", "Services"],
                default=[]
            )
        
        with filter_col2:
            search_term = st.text_input("Search Vendors", "")
        
        # Create vendor data
        vendors = [
            {
                "name": "Highland Concrete",
                "category": "Structural",
                "contact": "John Smith",
                "phone": "555-123-4567",
                "email": "john.smith@highlandconcrete.com",
                "performance_rating": 4.8,
                "current_pos": 1
            },
            {
                "name": "Metro Steel Erectors",
                "category": "Structural",
                "contact": "Michael Johnson",
                "phone": "555-234-5678",
                "email": "michael.j@metrosteel.com",
                "performance_rating": 4.7,
                "current_pos": 1
            },
            {
                "name": "Quality Masonry",
                "category": "Structural",
                "contact": "Robert Davis",
                "phone": "555-345-6789",
                "email": "rdavis@qualitymasonry.com",
                "performance_rating": 4.5,
                "current_pos": 1
            },
            {
                "name": "Skyline Glass",
                "category": "Envelope",
                "contact": "Sarah Wilson",
                "phone": "555-456-7890",
                "email": "swilson@skylineglass.com",
                "performance_rating": 4.6,
                "current_pos": 1
            },
            {
                "name": "Premier Roofing",
                "category": "Envelope",
                "contact": "David Martinez",
                "phone": "555-567-8901",
                "email": "dmartinez@premierroofing.com",
                "performance_rating": 4.7,
                "current_pos": 1
            },
            {
                "name": "Precision Panels",
                "category": "Envelope",
                "contact": "Emily Taylor",
                "phone": "555-678-9012",
                "email": "etaylor@precisionpanels.com",
                "performance_rating": 4.4,
                "current_pos": 1
            },
            {
                "name": "Alliance Electric",
                "category": "MEP",
                "contact": "Thomas Brown",
                "phone": "555-789-0123",
                "email": "tbrown@allianceelectric.com",
                "performance_rating": 4.9,
                "current_pos": 1
            },
            {
                "name": "Modern Mechanical",
                "category": "MEP",
                "contact": "Jennifer Lee",
                "phone": "555-890-1234",
                "email": "jlee@modernmech.com",
                "performance_rating": 4.8,
                "current_pos": 1
            },
            {
                "name": "Citywide Plumbing",
                "category": "MEP",
                "contact": "Brian White",
                "phone": "555-901-2345",
                "email": "bwhite@citywideplumbing.com",
                "performance_rating": 4.5,
                "current_pos": 1
            },
            {
                "name": "Fire Systems Inc",
                "category": "MEP",
                "contact": "Laura Miller",
                "phone": "555-012-3456",
                "email": "lmiller@firesystems.com",
                "performance_rating": 4.6,
                "current_pos": 1
            },
            {
                "name": "Premier Drywall",
                "category": "Finishes",
                "contact": "Kevin Chen",
                "phone": "555-123-4567",
                "email": "kchen@premierdrywall.com",
                "performance_rating": 4.3,
                "current_pos": 1
            },
            {
                "name": "Otis Elevator",
                "category": "Equipment",
                "contact": "Rachel Adams",
                "phone": "555-234-5678",
                "email": "radams@otis.com",
                "performance_rating": 4.7,
                "current_pos": 1
            },
            {
                "name": "Quality Inspections",
                "category": "Services",
                "contact": "Daniel Wilson",
                "phone": "555-345-6789",
                "email": "dwilson@qualityinspections.com",
                "performance_rating": 4.5,
                "current_pos": 0
            }
        ]
        
        # Apply filters
        filtered_vendors = vendors
        if category_filter:
            filtered_vendors = [v for v in filtered_vendors if v["category"] in category_filter]
        if search_term:
            search_term_lower = search_term.lower()
            filtered_vendors = [v for v in filtered_vendors if (
                search_term_lower in v["name"].lower() or 
                search_term_lower in v["contact"].lower() or
                search_term_lower in v["category"].lower()
            )]
        
        # Display vendors
        st.write(f"Showing {len(filtered_vendors)} of {len(vendors)} vendors")
        
        for vendor in filtered_vendors:
            with st.expander(f"{vendor['name']} - {vendor['category']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="margin-bottom: 10px;">
                        <span style="font-weight: 500; font-size: 16px;">{vendor['name']}</span>
                    </div>
                    
                    <div style="margin-bottom: 10px;">
                        <strong>Category:</strong> {vendor['category']}
                    </div>
                    
                    <div style="margin-bottom: 10px;">
                        <strong>Contact:</strong> {vendor['contact']}
                    </div>
                    
                    <div style="margin-bottom: 10px;">
                        <strong>Phone:</strong> {vendor['phone']}
                    </div>
                    
                    <div style="margin-bottom: 10px;">
                        <strong>Email:</strong> {vendor['email']}
                    </div>
                    
                    <div style="margin-bottom: 10px;">
                        <strong>Current POs:</strong> {vendor['current_pos']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Performance rating display
                    rating_color = "#6c757d"
                    if vendor["performance_rating"] >= 4.7:
                        rating_color = "#38d39f"  # Green
                    elif vendor["performance_rating"] >= 4.3:
                        rating_color = "#4a90e2"  # Blue
                    else:
                        rating_color = "#f59e0b"  # Orange
                        
                    st.markdown(f"""
                    <div style="text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 10px;">
                        <div style="font-size: 14px; color: #6c757d;">Performance Rating</div>
                        <div style="font-size: 24px; font-weight: 500; color: {rating_color};">{vendor['performance_rating']}</div>
                        <div style="font-size: 12px; color: #6c757d;">out of 5.0</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Action buttons
                contact_col, po_col = st.columns(2)
                with contact_col:
                    st.button(f"Contact {vendor['name']}", key=f"contact_{vendor['name'].replace(' ', '_')}")
                with po_col:
                    st.button(f"View POs for {vendor['name']}", key=f"view_pos_{vendor['name'].replace(' ', '_')}")
        
        # Add vendor button
        st.button("Add New Vendor", key="add_vendor")
    
    # Performance metrics tab
    with tabs[1]:
        st.markdown("#### Vendor Performance Metrics")
        
        # Select vendor for detailed metrics
        selected_vendor = st.selectbox(
            "Select Vendor",
            options=[v["name"] for v in vendors]
        )
        
        # Create performance data for the selected vendor
        performance_data = {
            "metrics": {
                "Overall Rating": 4.6,
                "Delivery Performance": 4.5,
                "Quality": 4.7,
                "Responsiveness": 4.8,
                "Documentation": 4.5,
                "Issue Resolution": 4.7
            },
            "delivery_history": [
                {"po": "PO-2024-042", "item": "Structural Steel - Foundation", "due_date": "Dec 15, 2024", "actual_date": "Dec 10, 2024", "variance": -5},
                {"po": "PO-2025-002", "item": "Structural Steel - Main Frame", "due_date": "May 10, 2025", "actual_date": "Pending", "variance": None}
            ],
            "quality_issues": [
                {"date": "Dec 12, 2024", "issue": "Minor dimensional variances in steel components", "resolution": "Corrected in field, vendor provided support", "impact": "Minor"},
                {"date": "Jan 5, 2025", "issue": "Surface finish inconsistencies", "resolution": "Vendor replaced affected materials", "impact": "Minor"}
            ]
        }
        
        # Display overall metrics
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown(f"**{selected_vendor} Performance Overview**")
            
            metrics = performance_data["metrics"]
            
            for metric, value in metrics.items():
                # Set metric color based on value
                metric_color = "#6c757d"
                if value >= 4.7:
                    metric_color = "#38d39f"  # Green
                elif value >= 4.3:
                    metric_color = "#4a90e2"  # Blue
                else:
                    metric_color = "#f59e0b"  # Orange
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #eee;">
                    <span>{metric}</span>
                    <div style="background-color: #f8f9fa; padding: 4px 8px; border-radius: 4px; color: {metric_color}; font-weight: 500;">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Radar chart for performance metrics
            categories = list(metrics.keys())
            values = list(metrics.values())
            
            # Close the loop for the radar chart
            categories.append(categories[0])
            values.append(values[0])
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                line_color='#4a90e2'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )
                ),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Delivery performance
        st.markdown("#### Delivery Performance")
        
        delivery_history = performance_data["delivery_history"]
        
        for delivery in delivery_history:
            variance_text = f"{delivery['variance']} days" if delivery['variance'] is not None else "Pending"
            variance_color = "#38d39f" if delivery['variance'] is not None and delivery['variance'] <= 0 else "#ef4444" if delivery['variance'] is not None and delivery['variance'] > 0 else "#6c757d"
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 10px; margin-bottom: 8px; background-color: #f8f9fa; border-radius: 4px;">
                <div>
                    <div style="font-weight: 500;">{delivery['item']}</div>
                    <div style="font-size: 13px; color: #6c757d;">{delivery['po']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="display: flex; font-size: 14px;">
                        <span style="margin-right: 15px;"><strong>Due:</strong> {delivery['due_date']}</span>
                        <span><strong>Actual:</strong> {delivery['actual_date']}</span>
                    </div>
                    <div style="font-size: 13px; color: {variance_color}; margin-top: 4px;">
                        Variance: {variance_text}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Quality issues
        st.markdown("#### Quality Issues")
        
        quality_issues = performance_data["quality_issues"]
        
        if quality_issues:
            for issue in quality_issues:
                impact_color = "#38d39f" if issue["impact"] == "Minor" else "#f59e0b" if issue["impact"] == "Moderate" else "#ef4444"
                
                st.markdown(f"""
                <div style="padding: 10px; margin-bottom: 8px; background-color: #f8f9fa; border-radius: 4px;">
                    <div style="display: flex; justify-content: space-between;">
                        <div style="font-weight: 500;">{issue['date']}</div>
                        <div style="color: {impact_color};">{issue['impact']} Impact</div>
                    </div>
                    <div style="font-size: 14px; margin-top: 5px;">
                        <strong>Issue:</strong> {issue['issue']}
                    </div>
                    <div style="font-size: 14px; margin-top: 5px;">
                        <strong>Resolution:</strong> {issue['resolution']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No quality issues reported.")
        
        # Recommendations
        st.markdown("#### Recommendations")
        
        st.markdown("""
        * Continue relationship with preferred status
        * Schedule regular coordination meetings for upcoming deliveries
        * Maintain clear communication about project schedule changes
        * Request early notification of potential delivery delays
        """)
    
    # Communication log tab
    with tabs[2]:
        st.markdown("#### Vendor Communication Log")
        
        # Select vendor for communication log
        selected_vendor = st.selectbox(
            "Select Vendor",
            options=[v["name"] for v in vendors],
            key="comm_vendor"
        )
        
        # Create sample communication data
        communications = [
            {
                "date": "May 15, 2025",
                "type": "Email",
                "subject": "PO-2025-002 Status Update",
                "from": "Michael Johnson (Metro Steel)",
                "to": "Project Manager",
                "content": "Confirming fabrication progress is on schedule for May 10 delivery. Shop drawings approved with minor comments addressed."
            },
            {
                "date": "May 10, 2025",
                "type": "Phone",
                "subject": "Delivery Logistics Discussion",
                "from": "Superintendent",
                "to": "Michael Johnson (Metro Steel)",
                "content": "Discussed delivery logistics for structural steel. Confirmed crane availability and staging area requirements."
            },
            {
                "date": "May 5, 2025",
                "type": "Meeting",
                "subject": "Pre-fabrication Meeting",
                "from": "Project Team",
                "to": "Metro Steel Team",
                "content": "Held pre-fabrication meeting to review critical dimensions, connection details, and delivery sequence. Action items documented in separate minutes."
            },
            {
                "date": "Apr 28, 2025",
                "type": "Email",
                "subject": "Shop Drawing Review",
                "from": "Project Engineer",
                "to": "Michael Johnson (Metro Steel)",
                "content": "Returned shop drawings with comments. Please revise and resubmit sections 3.5 and 4.2 with the requested changes."
            },
            {
                "date": "Apr 15, 2025",
                "type": "Email",
                "subject": "PO-2025-002 Acknowledgment",
                "from": "Michael Johnson (Metro Steel)",
                "to": "Procurement Manager",
                "content": "Acknowledging receipt of PO-2025-002 for structural steel package. Will proceed with engineering and shop drawings."
            }
        ]
        
        # Display communications
        for comm in communications:
            # Set type color
            type_color = "#6c757d"
            if comm["type"] == "Email":
                type_color = "#4a90e2"
            elif comm["type"] == "Phone":
                type_color = "#f59e0b"
            elif comm["type"] == "Meeting":
                type_color = "#9c27b0"
            
            with st.expander(f"{comm['date']} - {comm['subject']} ({comm['type']})"):
                st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: 500; font-size: 16px;">{comm['subject']}</span>
                        <span style="color: {type_color};">{comm['type']}</span>
                    </div>
                    <div style="font-size: 14px; color: #6c757d; margin-top: 4px;">
                        {comm['date']}
                    </div>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong>From:</strong> {comm['from']}
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong>To:</strong> {comm['to']}
                </div>
                
                <div style="margin-bottom: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 4px;">
                    {comm['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # New communication form
        st.markdown("#### Add New Communication")
        
        comm_type = st.selectbox("Communication Type", options=["Email", "Phone", "Meeting", "Other"])
        subject = st.text_input("Subject")
        from_person = st.text_input("From")
        to_person = st.text_input("To")
        content = st.text_area("Content")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Save Communication", key="save_comm")
        with col2:
            st.button("Cancel", key="cancel_comm")