"""
Bid Management Module

This module provides tools for managing the bidding process, including:
- Bid package creation and tracking
- Subcontractor qualification
- Bid analysis and comparison
- Scope clarification and leveling
- Contract award recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_bid_management():
    """Render the Bid Management dashboard"""
    st.header("Bid Management")
    
    # Create tabs for different bid management sections
    tabs = st.tabs([
        "Bid Dashboard", 
        "Bid Packages", 
        "Subcontractor Database", 
        "Bid Analysis"
    ])
    
    # Bid dashboard tab
    with tabs[0]:
        render_bid_dashboard()
    
    # Bid packages tab
    with tabs[1]:
        render_bid_packages()
    
    # Subcontractor database tab
    with tabs[2]:
        render_subcontractor_database()
    
    # Bid analysis tab
    with tabs[3]:
        render_bid_analysis()

def render_bid_dashboard():
    """Render the bid dashboard section"""
    st.subheader("Bid Management Dashboard")
    
    # Create layout columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bid status statistics
        status_col1, status_col2, status_col3, status_col4 = st.columns(4)
        
        with status_col1:
            st.metric(
                label="Total Packages",
                value="28",
                help="Total number of bid packages"
            )
        
        with status_col2:
            st.metric(
                label="Out for Bid",
                value="14",
                delta="+3",
                help="Number of packages currently out for bid"
            )
        
        with status_col3:
            st.metric(
                label="Awarded",
                value="8",
                delta="+2",
                help="Number of awarded contracts"
            )
        
        with status_col4:
            st.metric(
                label="In Analysis",
                value="6",
                delta="+1",
                help="Number of packages under analysis"
            )
        
        # Bid status chart
        st.markdown("#### Bid Package Status")
        
        status_data = pd.DataFrame({
            "Status": ["Not Started", "Out for Bid", "In Analysis", "Awarded"],
            "Count": [0, 14, 6, 8]
        })
        
        fig = px.bar(
            status_data,
            x="Status",
            y="Count",
            color="Status",
            color_discrete_map={
                "Not Started": "#6c757d",
                "Out for Bid": "#4a90e2",
                "In Analysis": "#f59e0b",
                "Awarded": "#38d39f"
            },
            labels={"Count": "Number of Packages"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Upcoming bid deadlines
        st.markdown("#### Upcoming Bid Deadlines")
        
        upcoming_bids = [
            {"package": "BP-12: Drywall & Framing", "deadline": "May 28, 2025", "days_left": 6, "subcontractors": 8},
            {"package": "BP-13: Flooring", "deadline": "May 30, 2025", "days_left": 8, "subcontractors": 6},
            {"package": "BP-14: Painting", "deadline": "Jun 3, 2025", "days_left": 12, "subcontractors": 5},
            {"package": "BP-15: Doors & Hardware", "deadline": "Jun 5, 2025", "days_left": 14, "subcontractors": 4},
            {"package": "BP-16: Specialties", "deadline": "Jun 10, 2025", "days_left": 19, "subcontractors": 3}
        ]
        
        for bid in upcoming_bids:
            days_color = "#ef4444" if bid["days_left"] < 7 else "#f59e0b" if bid["days_left"] < 14 else "#38d39f"
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 10px; margin-bottom: 8px; background-color: #f8f9fa; border-radius: 4px;">
                <div>
                    <div style="font-weight: 500;">{bid["package"]}</div>
                    <div style="font-size: 13px; color: #6c757d;">Due: {bid["deadline"]}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 500; color: {days_color};">{bid["days_left"]} days left</div>
                    <div style="font-size: 13px; color: #6c757d;">{bid["subcontractors"]} bidders</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Bid Package Distribution")
        
        # Package distribution by division
        division_data = pd.DataFrame({
            "Division": ["Div 03-05: Structure", "Div 06-09: Interiors", "Div 21-23: Mechanical", "Div 26-28: Electrical", "Other Divisions"],
            "Count": [5, 8, 6, 4, 5]
        })
        
        fig = px.pie(
            division_data,
            values="Count",
            names="Division",
            hole=0.4,
            labels={"Count": "Number of Packages"}
        )
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        
        # Budget by division
        st.markdown("#### Budget by Division")
        
        budget_data = pd.DataFrame({
            "Division": ["Div 03-05: Structure", "Div 06-09: Interiors", "Div 21-23: Mechanical", "Div 26-28: Electrical", "Other Divisions"],
            "Budget": [12500000, 9800000, 5750000, 4250000, 6200000]
        })
        
        fig = px.bar(
            budget_data,
            y="Division",
            x="Budget",
            orientation="h",
            text_auto='.2s',
            labels={"Budget": "Budget Amount ($)"}
        )
        fig.update_layout(xaxis_title="Budget Amount ($)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent awards
        st.markdown("#### Recent Contract Awards")
        
        recent_awards = [
            {"package": "BP-07: Concrete", "contractor": "Highland Concrete", "amount": "$5,450,000"},
            {"package": "BP-08: Structural Steel", "contractor": "Metro Steel Erectors", "amount": "$4,750,000"},
            {"package": "BP-09: Roofing", "contractor": "Premier Roofing", "amount": "$1,580,000"},
            {"package": "BP-10: Curtain Wall", "contractor": "Skyline Glass", "amount": "$3,825,000"}
        ]
        
        for award in recent_awards:
            st.markdown(f"""
            <div style="padding: 10px; margin-bottom: 8px; background-color: #edf7ed; border-left: 3px solid #38d39f; border-radius: 4px;">
                <div style="font-weight: 500;">{award["package"]}</div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; margin-top: 4px;">
                    <span>{award["contractor"]}</span>
                    <span>{award["amount"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_bid_packages():
    """Render the bid packages section"""
    st.subheader("Bid Packages")
    
    # Filter controls
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([2, 2, 2, 1])
    
    with filter_col1:
        status_filter = st.multiselect(
            "Status",
            options=["Not Started", "Out for Bid", "In Analysis", "Awarded"],
            default=["Out for Bid", "In Analysis"]
        )
    
    with filter_col2:
        division_filter = st.multiselect(
            "Division",
            options=["Div 03-05", "Div 06-09", "Div 21-23", "Div 26-28", "Other"],
            default=[]
        )
    
    with filter_col3:
        sort_by = st.selectbox(
            "Sort By",
            options=["Package #", "Status", "Release Date", "Bid Due Date", "Budget"]
        )
    
    with filter_col4:
        st.markdown("<br>", unsafe_allow_html=True)
        show_all = st.checkbox("Show All", value=False, key="bid_pkg_show_all")
    
    # Create bid package data
    bid_packages = [
        {
            "id": "BP-01",
            "name": "Site Work & Utilities",
            "division": "Div 31-33",
            "status": "Awarded",
            "budget": 2250000,
            "release_date": "Jan 15, 2025",
            "due_date": "Feb 10, 2025",
            "bidders": 6,
            "low_bid": 2180000,
            "high_bid": 2640000
        },
        {
            "id": "BP-02",
            "name": "Deep Foundations",
            "division": "Div 03-05",
            "status": "Awarded",
            "budget": 1850000,
            "release_date": "Jan 20, 2025",
            "due_date": "Feb 15, 2025",
            "bidders": 4,
            "low_bid": 1920000,
            "high_bid": 2240000
        },
        {
            "id": "BP-03",
            "name": "Concrete Superstructure",
            "division": "Div 03-05",
            "status": "Awarded",
            "budget": 3650000,
            "release_date": "Feb 1, 2025",
            "due_date": "Feb 28, 2025",
            "bidders": 5,
            "low_bid": 3450000,
            "high_bid": 3980000
        },
        {
            "id": "BP-04",
            "name": "Masonry",
            "division": "Div 03-05",
            "status": "Awarded",
            "budget": 1250000,
            "release_date": "Feb 10, 2025",
            "due_date": "Mar 5, 2025",
            "bidders": 7,
            "low_bid": 1180000,
            "high_bid": 1460000
        },
        {
            "id": "BP-05",
            "name": "Structural Steel",
            "division": "Div 03-05",
            "status": "Awarded",
            "budget": 4850000,
            "release_date": "Feb 15, 2025",
            "due_date": "Mar 15, 2025",
            "bidders": 3,
            "low_bid": 4750000,
            "high_bid": 5320000
        },
        {
            "id": "BP-06",
            "name": "Miscellaneous Metals",
            "division": "Div 03-05",
            "status": "Awarded",
            "budget": 950000,
            "release_date": "Mar 1, 2025",
            "due_date": "Mar 25, 2025",
            "bidders": 6,
            "low_bid": 920000,
            "high_bid": 1150000
        },
        {
            "id": "BP-07",
            "name": "Waterproofing & Dampproofing",
            "division": "Div 06-09",
            "status": "Awarded",
            "budget": 750000,
            "release_date": "Mar 10, 2025",
            "due_date": "Apr 5, 2025",
            "bidders": 5,
            "low_bid": 720000,
            "high_bid": 840000
        },
        {
            "id": "BP-08",
            "name": "Roofing",
            "division": "Div 06-09",
            "status": "Awarded",
            "budget": 1650000,
            "release_date": "Mar 15, 2025",
            "due_date": "Apr 10, 2025",
            "bidders": 4,
            "low_bid": 1580000,
            "high_bid": 1840000
        },
        {
            "id": "BP-09",
            "name": "Curtain Wall & Storefront",
            "division": "Div 06-09",
            "status": "In Analysis",
            "budget": 3950000,
            "release_date": "Apr 1, 2025",
            "due_date": "Apr 25, 2025",
            "bidders": 3,
            "low_bid": 3825000,
            "high_bid": 4250000
        },
        {
            "id": "BP-10",
            "name": "Metal Panels",
            "division": "Div 06-09",
            "status": "In Analysis",
            "budget": 1250000,
            "release_date": "Apr 5, 2025",
            "due_date": "Apr 30, 2025",
            "bidders": 4,
            "low_bid": 1180000,
            "high_bid": 1360000
        },
        {
            "id": "BP-11",
            "name": "Doors & Hardware",
            "division": "Div 06-09",
            "status": "In Analysis",
            "budget": 850000,
            "release_date": "Apr 10, 2025",
            "due_date": "May 5, 2025",
            "bidders": 5,
            "low_bid": 820000,
            "high_bid": 980000
        },
        {
            "id": "BP-12",
            "name": "Drywall & Framing",
            "division": "Div 06-09",
            "status": "Out for Bid",
            "budget": 2650000,
            "release_date": "Apr 15, 2025",
            "due_date": "May 28, 2025",
            "bidders": 8,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-13",
            "name": "Flooring",
            "division": "Div 06-09",
            "status": "Out for Bid",
            "budget": 1350000,
            "release_date": "Apr 20, 2025",
            "due_date": "May 30, 2025",
            "bidders": 6,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-14",
            "name": "Painting",
            "division": "Div 06-09",
            "status": "Out for Bid",
            "budget": 950000,
            "release_date": "Apr 25, 2025",
            "due_date": "Jun 3, 2025",
            "bidders": 5,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-15",
            "name": "Acoustic Ceilings",
            "division": "Div 06-09",
            "status": "Out for Bid",
            "budget": 750000,
            "release_date": "Apr 30, 2025",
            "due_date": "Jun 5, 2025",
            "bidders": 4,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-16",
            "name": "Specialties",
            "division": "Other",
            "status": "Out for Bid",
            "budget": 550000,
            "release_date": "May 5, 2025",
            "due_date": "Jun 10, 2025",
            "bidders": 3,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-17",
            "name": "Elevators",
            "division": "Other",
            "status": "Out for Bid",
            "budget": 1250000,
            "release_date": "May 10, 2025",
            "due_date": "Jun 15, 2025",
            "bidders": 2,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-18",
            "name": "Fire Protection",
            "division": "Div 21-23",
            "status": "Out for Bid",
            "budget": 850000,
            "release_date": "May 15, 2025",
            "due_date": "Jun 20, 2025",
            "bidders": 4,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-19",
            "name": "Plumbing",
            "division": "Div 21-23",
            "status": "Out for Bid",
            "budget": 1850000,
            "release_date": "May 20, 2025",
            "due_date": "Jun 25, 2025",
            "bidders": 5,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-20",
            "name": "HVAC",
            "division": "Div 21-23",
            "status": "Out for Bid",
            "budget": 3050000,
            "release_date": "May 25, 2025",
            "due_date": "Jun 30, 2025",
            "bidders": 4,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-21",
            "name": "Building Controls",
            "division": "Div 21-23",
            "status": "Out for Bid",
            "budget": 850000,
            "release_date": "Jun 1, 2025",
            "due_date": "Jul 5, 2025",
            "bidders": 3,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-22",
            "name": "Testing & Balancing",
            "division": "Div 21-23",
            "status": "Out for Bid",
            "budget": 250000,
            "release_date": "Jun 5, 2025",
            "due_date": "Jul 10, 2025",
            "bidders": 3,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-23",
            "name": "Electrical",
            "division": "Div 26-28",
            "status": "Out for Bid",
            "budget": 2950000,
            "release_date": "Jun 10, 2025",
            "due_date": "Jul 15, 2025",
            "bidders": 5,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-24",
            "name": "Low Voltage Systems",
            "division": "Div 26-28",
            "status": "In Analysis",
            "budget": 850000,
            "release_date": "Apr 15, 2025",
            "due_date": "May 10, 2025",
            "bidders": 4,
            "low_bid": 820000,
            "high_bid": 920000
        },
        {
            "id": "BP-25",
            "name": "Fire Alarm",
            "division": "Div 26-28",
            "status": "In Analysis",
            "budget": 450000,
            "release_date": "Apr 20, 2025",
            "due_date": "May 15, 2025",
            "bidders": 3,
            "low_bid": 430000,
            "high_bid": 520000
        },
        {
            "id": "BP-26",
            "name": "Landscaping",
            "division": "Other",
            "status": "In Analysis",
            "budget": 750000,
            "release_date": "Apr 25, 2025",
            "due_date": "May 20, 2025",
            "bidders": 6,
            "low_bid": 720000,
            "high_bid": 840000
        },
        {
            "id": "BP-27",
            "name": "Signage",
            "division": "Other",
            "status": "Out for Bid",
            "budget": 350000,
            "release_date": "Jun 15, 2025",
            "due_date": "Jul 20, 2025",
            "bidders": 4,
            "low_bid": None,
            "high_bid": None
        },
        {
            "id": "BP-28",
            "name": "Final Cleaning",
            "division": "Other",
            "status": "Out for Bid",
            "budget": 150000,
            "release_date": "Jun 20, 2025",
            "due_date": "Jul 25, 2025",
            "bidders": 5,
            "low_bid": None,
            "high_bid": None
        }
    ]
    
    # Apply filters
    filtered_packages = bid_packages
    if not show_all:
        if status_filter:
            filtered_packages = [p for p in filtered_packages if p["status"] in status_filter]
        if division_filter:
            filtered_packages = [p for p in filtered_packages if any(d in p["division"] for d in division_filter)]
    
    # Sort packages
    if sort_by == "Package #":
        filtered_packages = sorted(filtered_packages, key=lambda x: x["id"])
    elif sort_by == "Status":
        status_order = {"Awarded": 0, "In Analysis": 1, "Out for Bid": 2, "Not Started": 3}
        filtered_packages = sorted(filtered_packages, key=lambda x: status_order.get(x["status"], 4))
    elif sort_by == "Release Date":
        # Simple string sort - in a real app, would parse dates
        filtered_packages = sorted(filtered_packages, key=lambda x: x["release_date"])
    elif sort_by == "Bid Due Date":
        # Simple string sort - in a real app, would parse dates
        filtered_packages = sorted(filtered_packages, key=lambda x: x["due_date"])
    elif sort_by == "Budget":
        filtered_packages = sorted(filtered_packages, key=lambda x: x["budget"], reverse=True)
    
    # Display packages as cards
    st.write(f"Showing {len(filtered_packages)} of {len(bid_packages)} bid packages")
    
    # Create 2 columns for cards
    col1, col2 = st.columns(2)
    
    # Distribute cards between columns
    for i, package in enumerate(filtered_packages):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            # Set colors based on status
            status_color = "#6c757d"  # Default gray
            if package["status"] == "Awarded":
                status_color = "#38d39f"  # Green
            elif package["status"] == "In Analysis":
                status_color = "#f59e0b"  # Orange
            elif package["status"] == "Out for Bid":
                status_color = "#4a90e2"  # Blue
            
            # Create bid variance info if available
            bid_info = ""
            if package["low_bid"] is not None:
                variance = ((package["low_bid"] - package["budget"]) / package["budget"]) * 100
                variance_color = "#38d39f" if variance <= 0 else "#ef4444"
                bid_info = f"""
                <div style="display: flex; justify-content: space-between; margin-top: 8px;">
                    <span>Low Bid: ${package["low_bid"]:,}</span>
                    <span style="color: {variance_color};">{variance:+.1f}% variance</span>
                </div>
                """
            
            # Create the card
            st.markdown(f"""
            <div style="margin-bottom: 15px; padding: 15px; background-color: #f8f9fa; border-left: 3px solid {status_color}; border-radius: 5px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 500;">{package["id"]}: {package["name"]}</span>
                    <span style="color: {status_color};">{package["status"]}</span>
                </div>
                <div style="font-size: 14px; margin-top: 8px;">
                    <span><strong>Division:</strong> {package["division"]}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 4px;">
                    <span><strong>Budget:</strong> ${package["budget"]:,}</span>
                    <span><strong>Bidders:</strong> {package["bidders"]}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 4px;">
                    <span><strong>Released:</strong> {package["release_date"]}</span>
                    <span><strong>Due:</strong> {package["due_date"]}</span>
                </div>
                {bid_info}
            </div>
            """, unsafe_allow_html=True)
    
    # Add new package button
    st.button("Create New Bid Package", key="new_bid_package")

def render_subcontractor_database():
    """Render the subcontractor database section"""
    st.subheader("Subcontractor Database")
    
    # Filter controls
    filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 1])
    
    with filter_col1:
        trade_filter = st.multiselect(
            "Trade",
            options=["Concrete", "Steel", "Masonry", "Drywall", "Electrical", "Mechanical", "Plumbing", "Roofing", "Other"],
            default=[]
        )
    
    with filter_col2:
        status_filter = st.multiselect(
            "Status",
            options=["Approved", "Pending Review", "Not Approved"],
            default=["Approved"]
        )
    
    with filter_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        show_all = st.checkbox("Show All", value=False, key="sub_show_all")
    
    # Create subcontractor data
    subcontractors = [
        {
            "name": "Highland Concrete",
            "trade": "Concrete",
            "status": "Approved",
            "safety_rating": "A",
            "quality_rating": "A",
            "financial_strength": "Strong",
            "notes": "Previous excellent work on similar projects"
        },
        {
            "name": "Metro Steel Erectors",
            "trade": "Steel",
            "status": "Approved",
            "safety_rating": "A",
            "quality_rating": "A",
            "financial_strength": "Strong",
            "notes": "Long-standing relationship, consistently good performance"
        },
        {
            "name": "Quality Masonry",
            "trade": "Masonry",
            "status": "Approved",
            "safety_rating": "B+",
            "quality_rating": "A",
            "financial_strength": "Good",
            "notes": "Strong craftsmen, occasionally slow on paperwork"
        },
        {
            "name": "Premier Drywall",
            "trade": "Drywall",
            "status": "Approved",
            "safety_rating": "A-",
            "quality_rating": "B+",
            "financial_strength": "Good",
            "notes": "Reliable performance on previous projects"
        },
        {
            "name": "Alliance Electric",
            "trade": "Electrical",
            "status": "Approved",
            "safety_rating": "A",
            "quality_rating": "A-",
            "financial_strength": "Strong",
            "notes": "Good BIM/coordination capabilities"
        },
        {
            "name": "Modern Mechanical",
            "trade": "Mechanical",
            "status": "Approved",
            "safety_rating": "A",
            "quality_rating": "A",
            "financial_strength": "Strong",
            "notes": "Excellent technical capabilities and coordination"
        },
        {
            "name": "Citywide Plumbing",
            "trade": "Plumbing",
            "status": "Approved",
            "safety_rating": "B+",
            "quality_rating": "B+",
            "financial_strength": "Good",
            "notes": "Reliable, good value contractor"
        },
        {
            "name": "Premier Roofing",
            "trade": "Roofing",
            "status": "Approved",
            "safety_rating": "A",
            "quality_rating": "A",
            "financial_strength": "Good",
            "notes": "Excellent warranty support and follow-up"
        },
        {
            "name": "Skyline Glass",
            "trade": "Curtain Wall",
            "status": "Approved",
            "safety_rating": "A",
            "quality_rating": "A-",
            "financial_strength": "Strong",
            "notes": "Strong technical capabilities, good engineering support"
        },
        {
            "name": "Regional Metalworks",
            "trade": "Steel",
            "status": "Pending Review",
            "safety_rating": "B",
            "quality_rating": "B+",
            "financial_strength": "Moderate",
            "notes": "New to our projects, good references from peers"
        },
        {
            "name": "Value Electrical",
            "trade": "Electrical",
            "status": "Pending Review",
            "safety_rating": "B",
            "quality_rating": "B",
            "financial_strength": "Moderate",
            "notes": "Smaller contractor, limited high-rise experience"
        },
        {
            "name": "Economy Drywall",
            "trade": "Drywall",
            "status": "Not Approved",
            "safety_rating": "C",
            "quality_rating": "C+",
            "financial_strength": "Weak",
            "notes": "Issues on past projects, safety concerns"
        }
    ]
    
    # Apply filters
    filtered_subs = subcontractors
    if not show_all:
        if trade_filter:
            filtered_subs = [s for s in filtered_subs if s["trade"] in trade_filter]
        if status_filter:
            filtered_subs = [s for s in filtered_subs if s["status"] in status_filter]
    
    # Display subcontractors
    st.write(f"Showing {len(filtered_subs)} of {len(subcontractors)} subcontractors")
    
    for sub in filtered_subs:
        # Set colors based on status
        status_color = "#6c757d"  # Default gray
        if sub["status"] == "Approved":
            status_color = "#38d39f"  # Green
        elif sub["status"] == "Pending Review":
            status_color = "#f59e0b"  # Orange
        elif sub["status"] == "Not Approved":
            status_color = "#ef4444"  # Red
        
        # Create rating display
        safety_color = "#ef4444" if sub["safety_rating"][0] == "C" else "#f59e0b" if sub["safety_rating"][0] == "B" else "#38d39f"
        quality_color = "#ef4444" if sub["quality_rating"][0] == "C" else "#f59e0b" if sub["quality_rating"][0] == "B" else "#38d39f"
        
        # Create financial strength display
        fin_color = "#ef4444"
        if sub["financial_strength"] == "Strong":
            fin_color = "#38d39f"
        elif sub["financial_strength"] == "Good":
            fin_color = "#4a90e2"
        elif sub["financial_strength"] == "Moderate":
            fin_color = "#f59e0b"
        
        with st.expander(f"{sub['name']} - {sub['trade']} ({sub['status']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <span style="font-weight: 500; font-size: 16px;">{sub['name']}</span>
                    <span style="margin-left: 10px; color: {status_color};">{sub['status']}</span>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong>Trade:</strong> {sub['trade']}
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong>Notes:</strong> {sub['notes']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 8px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 8px;">
                    <div style="font-size: 12px; color: #6c757d;">Safety Rating</div>
                    <div style="font-size: 18px; font-weight: 500; color: {safety_color};">{sub['safety_rating']}</div>
                </div>
                
                <div style="text-align: center; padding: 8px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 8px;">
                    <div style="font-size: 12px; color: #6c757d;">Quality Rating</div>
                    <div style="font-size: 18px; font-weight: 500; color: {quality_color};">{sub['quality_rating']}</div>
                </div>
                
                <div style="text-align: center; padding: 8px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 8px;">
                    <div style="font-size: 12px; color: #6c757d;">Financial</div>
                    <div style="font-size: 18px; font-weight: 500; color: {fin_color};">{sub['financial_strength']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Action buttons
            if sub["status"] == "Pending Review":
                approve_col, reject_col = st.columns(2)
                with approve_col:
                    st.button(f"Approve {sub['name']}", key=f"approve_{sub['name'].replace(' ', '_')}")
                with reject_col:
                    st.button(f"Reject {sub['name']}", key=f"reject_{sub['name'].replace(' ', '_')}")
    
    # Add new subcontractor button
    st.button("Add New Subcontractor", key="new_subcontractor")

def render_bid_analysis():
    """Render the bid analysis section"""
    st.subheader("Bid Analysis")
    
    # Select package for analysis
    package = st.selectbox(
        "Select Bid Package for Analysis",
        options=[
            "BP-09: Curtain Wall & Storefront", 
            "BP-10: Metal Panels", 
            "BP-11: Doors & Hardware",
            "BP-24: Low Voltage Systems",
            "BP-25: Fire Alarm",
            "BP-26: Landscaping"
        ]
    )
    
    # Create sample bid analysis data
    if package == "BP-09: Curtain Wall & Storefront":
        analysis_data = {
            "budget": 3950000,
            "bidders": [
                {"company": "Skyline Glass", "base_bid": 3825000, "alternates": 145000, "exclusions": "None significant", "clarifications": "Includes engineering, shop drawings, testing"},
                {"company": "Metro Glazing", "base_bid": 3950000, "alternates": 180000, "exclusions": "Testing by others", "clarifications": "Schedule contingent on timely steel completion"},
                {"company": "City Glass & Aluminum", "base_bid": 4250000, "alternates": 210000, "exclusions": "None", "clarifications": "Includes premium for accelerated delivery"}
            ]
        }
    elif package == "BP-10: Metal Panels":
        analysis_data = {
            "budget": 1250000,
            "bidders": [
                {"company": "Precision Panels", "base_bid": 1180000, "alternates": 65000, "exclusions": "None", "clarifications": "Standard panel system as specified"},
                {"company": "Architectural Metals", "base_bid": 1250000, "alternates": 85000, "exclusions": "Waterproofing by others", "clarifications": "Premium finish option included"},
                {"company": "Metro Exteriors", "base_bid": 1280000, "alternates": 72000, "exclusions": "None", "clarifications": "Includes premium for color matching"},
                {"company": "City Facades", "base_bid": 1360000, "alternates": 90000, "exclusions": "None", "clarifications": "Includes 5-year weather warranty"}
            ]
        }
    else:
        # Default data for other packages
        analysis_data = {
            "budget": 850000,
            "bidders": [
                {"company": "Vendor A", "base_bid": 820000, "alternates": 45000, "exclusions": "None", "clarifications": "Standard package"},
                {"company": "Vendor B", "base_bid": 855000, "alternates": 55000, "exclusions": "Excludes X", "clarifications": "Includes Y"},
                {"company": "Vendor C", "base_bid": 880000, "alternates": 60000, "exclusions": "None", "clarifications": "Premium service"}
            ]
        }
    
    # Create layout columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Bid comparison table
        st.markdown("#### Bid Comparison")
        
        # Create a dataframe for comparison
        bids_df = pd.DataFrame([
            {"Bidder": b["company"], "Base Bid": b["base_bid"], "Variance": b["base_bid"] - analysis_data["budget"]} 
            for b in analysis_data["bidders"]
        ])
        
        # Add variance percentage
        bids_df["Variance %"] = (bids_df["Variance"] / analysis_data["budget"]) * 100
        
        # Format for display
        display_df = bids_df.copy()
        display_df["Base Bid"] = display_df["Base Bid"].apply(lambda x: f"${x:,.0f}")
        display_df["Variance"] = display_df["Variance"].apply(lambda x: f"${x:,.0f}" if x >= 0 else f"-${abs(x):,.0f}")
        display_df["Variance %"] = display_df["Variance %"].apply(lambda x: f"{x:+.2f}%")
        
        st.table(display_df)
        
        # Show budget for reference
        st.info(f"Package Budget: ${analysis_data['budget']:,}")
        
        # Create bid analysis chart
        bid_values = [b["base_bid"] for b in analysis_data["bidders"]]
        bidders = [b["company"] for b in analysis_data["bidders"]]
        
        fig = px.bar(
            x=bidders,
            y=bid_values,
            labels={"x": "Bidder", "y": "Bid Amount ($)"},
            title="Bid Amount Comparison"
        )
        
        # Add budget line
        fig.add_hline(
            y=analysis_data["budget"],
            line_dash="dash",
            line_color="red",
            annotation_text="Budget",
            annotation_position="top right"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Bid detail comparison
        st.markdown("#### Detailed Comparison")
        
        for i, bidder in enumerate(analysis_data["bidders"]):
            variance = bidder["base_bid"] - analysis_data["budget"]
            variance_pct = (variance / analysis_data["budget"]) * 100
            variance_color = "#38d39f" if variance <= 0 else "#ef4444"
            
            with st.expander(f"{bidder['company']} - ${bidder['base_bid']:,} ({variance_pct:+.2f}%)"):
                st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <strong>Base Bid:</strong> ${bidder['base_bid']:,}
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Variance from Budget:</strong> <span style="color: {variance_color};">{variance_pct:+.2f}% (${variance:+,})</span>
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Alternates Value:</strong> ${bidder['alternates']:,}
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Exclusions:</strong> {bidder['exclusions']}
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Clarifications:</strong> {bidder['clarifications']}
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button(f"Send Scope Questions {i}", key=f"scope_{i}")
                with col2:
                    st.button(f"Request Interview {i}", key=f"interview_{i}")
                with col3:
                    st.button(f"Recommend Award {i}", key=f"award_{i}")
    
    with col2:
        # Bid statistics
        st.markdown("#### Bid Statistics")
        
        # Calculate statistics
        bids = [b["base_bid"] for b in analysis_data["bidders"]]
        avg_bid = sum(bids) / len(bids)
        low_bid = min(bids)
        high_bid = max(bids)
        spread = high_bid - low_bid
        spread_pct = (spread / low_bid) * 100
        
        st.markdown(f"""
        <div style="padding: 15px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 15px;">
            <div style="font-size: 14px; margin-bottom: 8px;">
                <strong>Low Bid:</strong> ${low_bid:,.0f}
            </div>
            <div style="font-size: 14px; margin-bottom: 8px;">
                <strong>Average Bid:</strong> ${avg_bid:,.0f}
            </div>
            <div style="font-size: 14px; margin-bottom: 8px;">
                <strong>High Bid:</strong> ${high_bid:,.0f}
            </div>
            <div style="font-size: 14px; margin-bottom: 8px;">
                <strong>Spread:</strong> ${spread:,.0f} ({spread_pct:.1f}%)
            </div>
            <div style="font-size: 14px;">
                <strong>Number of Bidders:</strong> {len(bids)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Distribution chart
        fig = go.Figure()
        
        # Add budget marker
        fig.add_trace(go.Scatter(
            x=["Budget"],
            y=[analysis_data["budget"]],
            mode="markers",
            marker=dict(color="red", size=12, symbol="diamond"),
            name="Budget"
        ))
        
        # Add bid markers
        fig.add_trace(go.Scatter(
            x=["Bids"] * len(bids),
            y=bids,
            mode="markers",
            marker=dict(color="blue", size=10),
            name="Bids"
        ))
        
        # Add average marker
        fig.add_trace(go.Scatter(
            x=["Average"],
            y=[avg_bid],
            mode="markers",
            marker=dict(color="green", size=12, symbol="star"),
            name="Average"
        ))
        
        # Update layout
        fig.update_layout(
            title="Bid Distribution",
            yaxis_title="Amount ($)",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendation
        st.markdown("#### Analysis & Recommendation")
        
        # Automatic recommendation based on lowest bid
        low_bidder = analysis_data["bidders"][bids.index(low_bid)]["company"]
        budget_variance = (low_bid - analysis_data["budget"]) / analysis_data["budget"] * 100
        status = "Under Budget" if budget_variance <= 0 else "Over Budget"
        status_color = "#38d39f" if budget_variance <= 0 else "#ef4444"
        
        st.markdown(f"""
        <div style="padding: 15px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 15px;">
            <div style="font-size: 14px; margin-bottom: 10px;">
                <strong>Lowest Bidder:</strong> {low_bidder}
            </div>
            <div style="font-size: 14px; margin-bottom: 10px;">
                <strong>Amount:</strong> ${low_bid:,.0f}
            </div>
            <div style="font-size: 14px; margin-bottom: 10px;">
                <strong>Budget Variance:</strong> <span style="color: {status_color};">{budget_variance:+.2f}% (${low_bid-analysis_data["budget"]:+,.0f})</span>
            </div>
            <div style="font-size: 14px; margin-bottom: 10px;">
                <strong>Status:</strong> <span style="color: {status_color};">{status}</span>
            </div>
            <div style="font-size: 14px;">
                <strong>Recommendation:</strong> Proceed with {low_bidder} pending scope verification
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Next steps
        st.markdown("#### Next Steps")
        
        next_steps = [
            "Schedule scope review meeting with lowest bidder",
            "Verify schedule compliance and key milestones",
            "Confirm no exclusions or qualifications that change bid ranking",
            "Check references and current workload",
            "Prepare award recommendation for owner approval"
        ]
        
        for step in next_steps:
            st.markdown(f"- {step}")
        
        # Award button
        st.button("Prepare Award Recommendation", key="prepare_award")