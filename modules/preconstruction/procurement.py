"""
Procurement Module for Pre-Construction

This module provides comprehensive procurement planning capabilities:
- Procurement strategy development
- Early procurement packages
- Long-lead item tracking
- Vendor/supplier qualification
- Purchase order tracking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def render_procurement():
    """Render the Procurement dashboard"""
    st.header("Procurement Planning")
    
    # Create tabs for different procurement sections
    tabs = st.tabs([
        "Dashboard", 
        "Procurement Strategy", 
        "Long-Lead Items", 
        "Vendor Management", 
        "Purchase Orders"
    ])
    
    # Dashboard tab
    with tabs[0]:
        render_procurement_dashboard()
    
    # Procurement Strategy tab
    with tabs[1]:
        render_procurement_strategy()
    
    # Long-Lead Items tab
    with tabs[2]:
        render_long_lead_items()
    
    # Vendor Management tab
    with tabs[3]:
        render_vendor_management()
    
    # Purchase Orders tab
    with tabs[4]:
        render_purchase_orders()

def render_procurement_dashboard():
    """Render the procurement dashboard"""
    
    # Procurement stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Items",
            value="68",
            help="Total procurement items identified"
        )
    
    with col2:
        st.metric(
            label="Long-Lead Items",
            value="24",
            delta="+3",
            help="Items requiring advanced procurement"
        )
    
    with col3:
        st.metric(
            label="Items Ordered",
            value="16",
            delta="+5",
            help="Items with purchase orders issued"
        )
    
    with col4:
        st.metric(
            label="Approved Vendors",
            value="42",
            delta="+2",
            help="Qualified and approved vendors"
        )
    
    # Procurement schedule
    st.subheader("Procurement Schedule Overview")
    
    # Create gantt chart data
    today = datetime.now()
    
    procurement_data = pd.DataFrame([
        {
            "Task": "MEP Equipment",
            "Category": "Mechanical",
            "Start": today - timedelta(days=30),
            "Finish": today + timedelta(days=90),
            "Status": "In Progress"
        },
        {
            "Task": "Elevators",
            "Category": "Conveying",
            "Start": today - timedelta(days=45),
            "Finish": today + timedelta(days=120),
            "Status": "In Progress"
        },
        {
            "Task": "Curtain Wall",
            "Category": "Envelope",
            "Start": today - timedelta(days=15),
            "Finish": today + timedelta(days=60),
            "Status": "In Progress"
        },
        {
            "Task": "Electrical Distribution",
            "Category": "Electrical",
            "Start": today + timedelta(days=15),
            "Finish": today + timedelta(days=75),
            "Status": "Planned"
        },
        {
            "Task": "Structural Steel",
            "Category": "Structural",
            "Start": today - timedelta(days=60),
            "Finish": today - timedelta(days=10),
            "Status": "Complete"
        },
        {
            "Task": "Roof Materials",
            "Category": "Envelope",
            "Start": today + timedelta(days=30),
            "Finish": today + timedelta(days=60),
            "Status": "Planned"
        },
        {
            "Task": "Bathroom Fixtures",
            "Category": "Plumbing",
            "Start": today + timedelta(days=45),
            "Finish": today + timedelta(days=75),
            "Status": "Planned"
        },
        {
            "Task": "Light Fixtures",
            "Category": "Electrical",
            "Start": today + timedelta(days=60),
            "Finish": today + timedelta(days=90),
            "Status": "Planned"
        }
    ])
    
    # Create color mapping for status
    color_map = {
        "Complete": "#4CAF50",
        "In Progress": "#2196F3",
        "Planned": "#9E9E9E"
    }
    
    procurement_data["Color"] = procurement_data["Status"].map(color_map)
    
    # Draw gantt chart
    fig = px.timeline(
        procurement_data, 
        x_start="Start", 
        x_end="Finish", 
        y="Task",
        color="Status",
        color_discrete_map=color_map,
        title="Procurement Timeline"
    )
    
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Important deadlines
    st.subheader("Critical Procurement Deadlines")
    
    deadlines = [
        {"item": "Elevator Shop Drawings", "deadline": "Jun 15, 2025", "days_left": 24, "responsible": "John D."},
        {"item": "Curtain Wall Release", "deadline": "Jun 30, 2025", "days_left": 39, "responsible": "Sarah T."},
        {"item": "MEP Equipment", "deadline": "Jul 15, 2025", "days_left": 54, "responsible": "Mike R."},
        {"item": "Generators", "deadline": "Jul 22, 2025", "days_left": 61, "responsible": "Robert M."},
        {"item": "Kitchen Equipment", "deadline": "Aug 10, 2025", "days_left": 80, "responsible": "Lisa K."}
    ]
    
    # Create columns for display
    for deadline in deadlines:
        days_color = "#4a90e2"  # Default blue
        
        if deadline["days_left"] < 30:
            days_color = "#f59e0b"  # Orange/yellow for approaching
        if deadline["days_left"] < 15:
            days_color = "#ef4444"  # Red for urgent
            
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 10px;">
            <div>
                <strong>{deadline["item"]}</strong>
                <div style="font-size: 14px; color: #6c757d;">Responsible: {deadline["responsible"]}</div>
            </div>
            <div style="text-align: right;">
                <div>Deadline: {deadline["deadline"]}</div>
                <div style="color: {days_color}; font-weight: 500;">{deadline["days_left"]} days remaining</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_procurement_strategy():
    """Render the procurement strategy section"""
    st.subheader("Procurement Strategy")
    
    # Overview
    st.markdown("""
    The procurement strategy for the Highland Tower Development is designed to optimize cost, 
    schedule, and quality through strategic sourcing, early procurement of long-lead items, 
    and careful vendor selection.
    """)
    
    # Strategy components
    st.markdown("#### Strategy Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        strategy_components = [
            {
                "title": "Early Procurement Packages",
                "description": "Identify and procure long-lead items in advance to prevent schedule delays.",
                "status": "Implemented"
            },
            {
                "title": "Strategic Sourcing",
                "description": "Leverage established relationships and bulk purchasing for major trades.",
                "status": "Implemented"
            },
            {
                "title": "Vendor Prequalification",
                "description": "Establish minimum vendor requirements for quality and capability.",
                "status": "Implemented"
            },
            {
                "title": "Risk Mitigation",
                "description": "Identify supply chain risks and establish contingency plans.",
                "status": "In Progress"
            }
        ]
        
        for component in strategy_components:
            status_color = "#38d39f" if component["status"] == "Implemented" else "#4a90e2"
            
            st.markdown(f"""
            <div style="padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{component["title"]}</strong>
                    <span style="color: {status_color};">{component["status"]}</span>
                </div>
                <div style="font-size: 14px; margin-top: 5px;">{component["description"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Procurement methods
        st.markdown("#### Procurement Methods")
        
        methods = [
            {"method": "Design-Assist", "percentage": 35},
            {"method": "Competitive Bid", "percentage": 45},
            {"method": "Negotiated", "percentage": 15},
            {"method": "Direct Purchase", "percentage": 5}
        ]
        
        fig = px.pie(
            pd.DataFrame(methods), 
            values="percentage", 
            names="method",
            title="Procurement Method Distribution"
        )
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Package types
        st.markdown("#### Package Types")
        
        package_types = [
            {"type": "Trade Packages", "count": 22},
            {"type": "Design-Assist", "count": 8},
            {"type": "Owner Direct Purchase", "count": 4},
            {"type": "Long-Lead Items", "count": 18}
        ]
        
        fig = px.bar(
            pd.DataFrame(package_types),
            x="type",
            y="count",
            title="Package Type Distribution"
        )
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Procurement responsibility matrix
    st.markdown("#### Procurement Responsibility Matrix")
    
    # Create responsibility matrix data
    responsibility_data = {
        "Package Type": ["MEP Systems", "Structural", "Envelope", "Finishes", "Conveying", "Equipment"],
        "Identification": ["PM", "PM/Design", "PM/Design", "PM/CM", "PM", "PM/Owner"],
        "Specification": ["Design", "Design", "Design", "Design", "Design", "Design/Owner"],
        "Vendor Selection": ["PM/CM", "CM", "CM", "CM", "PM/CM", "Owner/PM"],
        "Purchase": ["CM", "CM", "CM", "CM", "CM", "Owner"],
        "Expediting": ["CM", "CM", "CM", "CM", "CM", "PM/CM"],
        "Inspection": ["CM/Design", "CM/Design", "CM/Design", "CM", "CM/Design", "CM/Owner"]
    }
    
    # Create DataFrame
    df_responsibility = pd.DataFrame(responsibility_data)
    
    # Display with styling
    st.dataframe(
        df_responsibility,
        hide_index=True,
        use_container_width=True
    )

def render_long_lead_items():
    """Render the long-lead items section"""
    st.subheader("Long-Lead Item Tracking")
    
    # Long-lead items explanation
    st.markdown("""
    Long-lead items are materials, equipment, or systems that require extended time for procurement,
    fabrication, and delivery. These items must be identified and ordered early to prevent schedule delays.
    """)
    
    # Filter controls
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.text_input("Search Items", placeholder="Enter keywords...")
    
    with col2:
        st.selectbox("Category", ["All Categories", "Mechanical", "Electrical", "Structural", "Envelope", "Conveying", "Plumbing", "Specialty"])
    
    with col3:
        st.selectbox("Status", ["All Status", "Not Started", "In Procurement", "Ordered", "In Fabrication", "Shipped", "Delivered"])
    
    with col4:
        st.button("Add Long-Lead Item", type="primary")
    
    # Long-lead items list
    long_lead_items = [
        {"id": "LL-001", "item": "Elevators (Passenger)", "category": "Conveying", "lead_time": "36 weeks", "order_by": "Jun 15, 2025", "status": "In Procurement", "notes": "Custom cab finishes require additional time"},
        {"id": "LL-002", "item": "Elevators (Service)", "category": "Conveying", "lead_time": "32 weeks", "order_by": "Jul 1, 2025", "status": "Not Started", "notes": "Standard cab specifications"},
        {"id": "LL-003", "item": "Electrical Switchgear", "category": "Electrical", "lead_time": "28 weeks", "order_by": "Jul 15, 2025", "status": "Not Started", "notes": "Coordinating with utility for service requirements"},
        {"id": "LL-004", "item": "Chillers", "category": "Mechanical", "lead_time": "24 weeks", "order_by": "Aug 1, 2025", "status": "Not Started", "notes": "Final load calculations pending"},
        {"id": "LL-005", "item": "Cooling Towers", "category": "Mechanical", "lead_time": "20 weeks", "order_by": "Aug 15, 2025", "status": "Not Started", "notes": "Site placement confirmed"},
        {"id": "LL-006", "item": "Curtain Wall System", "category": "Envelope", "lead_time": "30 weeks", "order_by": "Jun 30, 2025", "status": "In Procurement", "notes": "Custom extrusions required"},
        {"id": "LL-007", "item": "Generators", "category": "Electrical", "lead_time": "22 weeks", "order_by": "Jul 22, 2025", "status": "Not Started", "notes": "Coordinating with electrical engineer for sizing"},
        {"id": "LL-008", "item": "Air Handling Units", "category": "Mechanical", "lead_time": "18 weeks", "order_by": "Sep 1, 2025", "status": "Not Started", "notes": "Custom units for amenity spaces"},
        {"id": "LL-009", "item": "Structural Steel", "category": "Structural", "lead_time": "24 weeks", "order_by": "Mar 1, 2025", "status": "Ordered", "notes": "Mill order placed, fabrication to begin in June"},
        {"id": "LL-010", "item": "Kitchen Equipment", "category": "Specialty", "lead_time": "16 weeks", "order_by": "Aug 10, 2025", "status": "Not Started", "notes": "Awaiting final equipment selections from operator"}
    ]
    
    # Create DataFrame
    df_longlead = pd.DataFrame(long_lead_items)
    
    # Display with styling
    st.dataframe(
        df_longlead,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small"),
            "item": st.column_config.TextColumn("Item Description", width="medium"),
            "category": st.column_config.TextColumn("Category", width="small"),
            "lead_time": st.column_config.TextColumn("Lead Time", width="small"),
            "order_by": st.column_config.TextColumn("Order By", width="small"),
            "status": st.column_config.TextColumn("Status", width="small"),
            "notes": st.column_config.TextColumn("Notes", width="large")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Lead time by category
    st.subheader("Lead Time Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create lead time data
        lead_time_data = {
            "Category": ["Conveying", "Envelope", "Electrical", "Mechanical", "Structural", "Specialty", "Plumbing"],
            "Average Lead Time (weeks)": [34, 30, 25, 20, 24, 16, 14]
        }
        
        # Create DataFrame
        df_leadtime = pd.DataFrame(lead_time_data)
        
        # Create bar chart
        fig = px.bar(
            df_leadtime, 
            x="Category", 
            y="Average Lead Time (weeks)",
            title="Average Lead Time by Category"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Create lead time risk data
        risk_data = {
            "Risk Level": ["High Risk (>30 weeks)", "Medium Risk (20-30 weeks)", "Low Risk (<20 weeks)"],
            "Item Count": [3, 5, 2]
        }
        
        # Create DataFrame
        df_risk = pd.DataFrame(risk_data)
        
        # Create pie chart
        fig = px.pie(
            df_risk, 
            values="Item Count", 
            names="Risk Level",
            color="Risk Level",
            color_discrete_map={
                "High Risk (>30 weeks)": "#ef4444",
                "Medium Risk (20-30 weeks)": "#f59e0b",
                "Low Risk (<20 weeks)": "#38d39f"
            },
            title="Lead Time Risk Distribution"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def render_vendor_management():
    """Render the vendor management section"""
    st.subheader("Vendor Management")
    
    # Vendor management explanation
    st.markdown("""
    Effective vendor management ensures that qualified suppliers are selected for the project
    and performance is monitored throughout the procurement process.
    """)
    
    # Vendor metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Vendors",
            value="68",
            help="Total vendors in database"
        )
    
    with col2:
        st.metric(
            label="Approved",
            value="42",
            delta="+4",
            help="Approved vendors for this project"
        )
    
    with col3:
        st.metric(
            label="Under Review",
            value="15",
            delta="-2",
            help="Vendors currently being evaluated"
        )
    
    with col4:
        st.metric(
            label="Rejected",
            value="11",
            help="Vendors that did not meet qualifications"
        )
    
    # Vendor search and filter
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.text_input("Search Vendors", placeholder="Enter vendor name or category...")
    
    with col2:
        st.selectbox("Trade Category", ["All Categories", "Mechanical", "Electrical", "Structural", "Envelope", "Conveying", "Plumbing", "Specialty"])
    
    with col3:
        st.selectbox("Approval Status", ["All Status", "Approved", "Under Review", "Rejected"])
    
    with col4:
        st.button("Add New Vendor", type="primary")
    
    # Vendor list
    vendors = [
        {"id": "V-001", "name": "Highland Mechanical", "category": "Mechanical", "status": "Approved", "rating": "A", "insurance": "Valid", "performance": "Excellent"},
        {"id": "V-002", "name": "Power City Electric", "category": "Electrical", "status": "Approved", "rating": "A", "insurance": "Valid", "performance": "Excellent"},
        {"id": "V-003", "name": "Structural Steel Inc.", "category": "Structural", "status": "Approved", "rating": "A", "insurance": "Valid", "performance": "Good"},
        {"id": "V-004", "name": "Metro Elevators", "category": "Conveying", "status": "Approved", "rating": "B", "insurance": "Valid", "performance": "Good"},
        {"id": "V-005", "name": "Premium Glass Systems", "category": "Envelope", "status": "Approved", "rating": "A", "insurance": "Valid", "performance": "Excellent"},
        {"id": "V-006", "name": "Quality Plumbing", "category": "Plumbing", "status": "Approved", "rating": "B", "insurance": "Valid", "performance": "Good"},
        {"id": "V-007", "name": "Innovative Kitchen Supply", "category": "Specialty", "status": "Under Review", "rating": "N/A", "insurance": "Pending", "performance": "N/A"},
        {"id": "V-008", "name": "Budget Mechanical", "category": "Mechanical", "status": "Rejected", "rating": "D", "insurance": "Expired", "performance": "Poor"},
        {"id": "V-009", "name": "Advanced Environmental", "category": "Mechanical", "status": "Under Review", "rating": "N/A", "insurance": "Valid", "performance": "N/A"},
        {"id": "V-010", "name": "Steel Fab Express", "category": "Structural", "status": "Under Review", "rating": "N/A", "insurance": "Pending", "performance": "N/A"}
    ]
    
    # Create DataFrame
    df_vendors = pd.DataFrame(vendors)
    
    # Display with styling
    st.dataframe(
        df_vendors,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small"),
            "name": st.column_config.TextColumn("Vendor Name", width="medium"),
            "category": st.column_config.TextColumn("Category", width="small"),
            "status": st.column_config.TextColumn("Status", width="small"),
            "rating": st.column_config.TextColumn("Rating", width="small"),
            "insurance": st.column_config.TextColumn("Insurance", width="small"),
            "performance": st.column_config.TextColumn("Performance", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Vendor qualification criteria
    st.markdown("#### Vendor Qualification Requirements")
    
    criteria = [
        {"criteria": "Financial Stability", "description": "Vendor must demonstrate financial strength commensurate with project size", "verification": "Financial statements, bank references"},
        {"criteria": "Experience", "description": "Minimum 5 years of experience in similar projects", "verification": "Project references, portfolio review"},
        {"criteria": "Insurance", "description": "General liability, workers comp, and professional liability insurance", "verification": "Certificate of insurance review"},
        {"criteria": "Safety Record", "description": "EMR < 1.0, no major OSHA violations", "verification": "Safety records, OSHA logs"},
        {"criteria": "Quality Control", "description": "Documented quality control procedures", "verification": "QC manual review, site visits"},
        {"criteria": "Capacity", "description": "Sufficient staff and resources to execute project", "verification": "Staffing plan, current workload"}
    ]
    
    # Create columns for better display
    col1, col2 = st.columns(2)
    
    # Split the criteria list
    half = len(criteria) // 2
    
    # Display first half
    with col1:
        for item in criteria[:half]:
            st.markdown(f"""
            <div style="padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 10px;">
                <div style="font-weight: 500;">{item["criteria"]}</div>
                <div style="font-size: 14px; margin-top: 5px;">{item["description"]}</div>
                <div style="font-size: 12px; color: #666; margin-top: 3px;">Verification: {item["verification"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Display second half
    with col2:
        for item in criteria[half:]:
            st.markdown(f"""
            <div style="padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; margin-bottom: 10px;">
                <div style="font-weight: 500;">{item["criteria"]}</div>
                <div style="font-size: 14px; margin-top: 5px;">{item["description"]}</div>
                <div style="font-size: 12px; color: #666; margin-top: 3px;">Verification: {item["verification"]}</div>
            </div>
            """, unsafe_allow_html=True)

def render_purchase_orders():
    """Render the purchase orders section"""
    st.subheader("Purchase Order Management")
    
    # Purchase order stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total POs",
            value="28",
            help="Total purchase orders issued"
        )
    
    with col2:
        st.metric(
            label="PO Value",
            value="$12.8M",
            help="Total value of purchase orders"
        )
    
    with col3:
        st.metric(
            label="POs This Month",
            value="5",
            delta="+2",
            help="Purchase orders issued this month"
        )
    
    # Purchase order list
    st.markdown("#### Purchase Orders")
    
    # Purchase order search and filter
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.text_input("Search POs", placeholder="Enter PO number or vendor...")
    
    with col2:
        st.selectbox("PO Status", ["All Status", "Issued", "Acknowledged", "In Production", "Shipped", "Delivered", "Closed"])
    
    with col3:
        st.selectbox("Order By", ["Date (Newest)", "Date (Oldest)", "Value (Highest)", "Value (Lowest)"])
    
    with col4:
        st.button("Create New PO", type="primary")
    
    # Purchase order data
    purchase_orders = [
        {"po": "PO-10045", "vendor": "Structural Steel Inc.", "description": "Structural Steel Package", "date": "Mar 1, 2025", "value": "$4,800,000", "status": "In Production"},
        {"po": "PO-10046", "vendor": "Metro Elevators", "description": "Elevator Package - Phase 1", "date": "Mar 15, 2025", "value": "$950,000", "status": "Acknowledged"},
        {"po": "PO-10047", "vendor": "Premium Glass Systems", "description": "Curtain Wall Deposit", "date": "Apr 1, 2025", "value": "$1,200,000", "status": "Acknowledged"},
        {"po": "PO-10048", "vendor": "Highland Mechanical", "description": "Mechanical Equipment - Chillers", "date": "Apr 15, 2025", "value": "$850,000", "status": "Issued"},
        {"po": "PO-10049", "vendor": "Power City Electric", "description": "Electrical Switchgear", "date": "Apr 20, 2025", "value": "$750,000", "status": "Issued"},
        {"po": "PO-10050", "vendor": "Highland Mechanical", "description": "Cooling Towers", "date": "Apr 25, 2025", "value": "$320,000", "status": "Issued"},
        {"po": "PO-10051", "vendor": "Quality Plumbing", "description": "Plumbing Fixtures Deposit", "date": "May 1, 2025", "value": "$425,000", "status": "Issued"},
        {"po": "PO-10052", "vendor": "Power City Electric", "description": "Generator Package", "date": "May 5, 2025", "value": "$380,000", "status": "Issued"}
    ]
    
    # Create DataFrame
    df_pos = pd.DataFrame(purchase_orders)
    
    # Display with styling
    st.dataframe(
        df_pos,
        column_config={
            "po": st.column_config.TextColumn("PO Number", width="small"),
            "vendor": st.column_config.TextColumn("Vendor", width="medium"),
            "description": st.column_config.TextColumn("Description", width="large"),
            "date": st.column_config.TextColumn("Date", width="small"),
            "value": st.column_config.TextColumn("Value", width="small"),
            "status": st.column_config.TextColumn("Status", width="small")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Purchase orders by category
    st.markdown("#### Purchase Orders by Category")
    
    # Purchase order amount by category data
    po_categories = pd.DataFrame({
        "Category": ["Structural", "Conveying", "Envelope", "Mechanical", "Electrical", "Plumbing"],
        "Value": [4800000, 950000, 1200000, 1170000, 1130000, 425000]
    })
    
    # Create bar chart
    fig = px.bar(
        po_categories, 
        x="Category", 
        y="Value",
        title="PO Value by Category",
        labels={"Value": "Value ($)"}
    )
    
    # Format y-axis as currency
    fig.update_layout(
        height=400,
        yaxis=dict(tickprefix="$", tickformat=",")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Purchase order tracking
    st.markdown("#### Purchase Order Status")
    
    # Create PO status data
    po_status = pd.DataFrame({
        "Status": ["Issued", "Acknowledged", "In Production", "Shipped", "Delivered", "Closed"],
        "Count": [5, 2, 1, 0, 0, 0]
    })
    
    # Create funnel chart
    fig = px.funnel(
        po_status,
        x="Count",
        y="Status",
        title="Purchase Order Status Pipeline"
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)