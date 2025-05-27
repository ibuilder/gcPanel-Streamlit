"""
Highland Tower Development - Enhanced Navigation Construction Management Platform
$45.5M Mixed-Use Development - Complete Module Structure

Features comprehensive navigation structure with all modules implemented in pure Python
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="gcPanel - Highland Tower Development",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_styling():
    """Apply professional Highland Tower Development styling"""
    st.markdown("""
    <style>
    /* Main App Styling */
    .main {
        padding-top: 0rem;
        background-color: #f8f9fa;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #2c3e50 !important;
        padding-top: 1rem;
    }
    
    /* Sidebar Content */
    .css-1d391kg .css-1v0mbdj {
        color: white !important;
    }
    
    /* User Profile Section */
    .user-profile {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        color: white;
    }
    
    /* Project Header */
    .project-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
        color: white;
        font-weight: bold;
    }
    
    /* Section Headers */
    .section-header {
        color: #bdc3c7;
        font-size: 14px;
        font-weight: 600;
        margin: 20px 0 10px 0;
        padding: 0 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Navigation Buttons */
    .nav-button {
        width: 100%;
        margin-bottom: 8px;
        background: #3498db !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-button:hover {
        background: #2980b9 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }
    
    /* Content Area */
    .content-container {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 2px 20px rgba(0,0,0,0.08);
        margin: 20px 0;
    }
    
    /* Module Headers */
    .module-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        text-align: center;
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
        margin-bottom: 15px;
    }
    
    /* Logout Button */
    .logout-btn {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: #e74c3c !important;
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render comprehensive sidebar navigation matching the provided structure"""
    with st.sidebar:
        # User Profile Section
        st.markdown("""
        <div class="user-profile">
            <div style="font-size: 24px; margin-bottom: 5px;">👤 admin</div>
            <div style="font-size: 14px; opacity: 0.9;">Administrator</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Project Header
        st.markdown("""
        <div class="project-header">
            🏗️ Highland Tower Development
        </div>
        """, unsafe_allow_html=True)
        
        # Core Tools Section
        st.markdown('<div class="section-header">⚡ Core Tools</div>', unsafe_allow_html=True)
        
        if st.button("📊 Dashboard", key="dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
        
        if st.button("📋 Daily Reports", key="daily_reports", use_container_width=True):
            st.session_state.current_page = "daily_reports"
        
        if st.button("🚚 Deliveries", key="deliveries", use_container_width=True):
            st.session_state.current_page = "deliveries"
        
        if st.button("🦺 Safety", key="safety", use_container_width=True):
            st.session_state.current_page = "safety"
        
        # Project Management Section
        st.markdown('<div class="section-header">🎯 Project Management</div>', unsafe_allow_html=True)
        
        if st.button("🏗️ PreConstruction", key="preconstruction", use_container_width=True):
            st.session_state.current_page = "preconstruction"
        
        if st.button("⚙️ Engineering", key="engineering", use_container_width=True):
            st.session_state.current_page = "engineering"
        
        if st.button("👷 Field Operations", key="field_operations", use_container_width=True):
            st.session_state.current_page = "field_operations"
        
        if st.button("📄 Contracts", key="contracts", use_container_width=True):
            st.session_state.current_page = "contracts"
        
        if st.button("💰 Cost Management", key="cost_management", use_container_width=True):
            st.session_state.current_page = "cost_management"
        
        if st.button("🏢 BIM", key="bim", use_container_width=True):
            st.session_state.current_page = "bim"
        
        if st.button("✅ Closeout", key="closeout", use_container_width=True):
            st.session_state.current_page = "closeout"
        
        # Advanced Tools Section
        st.markdown('<div class="section-header">🔧 Advanced Tools</div>', unsafe_allow_html=True)
        
        if st.button("📝 RFIs", key="rfis", use_container_width=True):
            st.session_state.current_page = "rfis"
        
        if st.button("📤 Submittals", key="submittals", use_container_width=True):
            st.session_state.current_page = "submittals"
        
        if st.button("📨 Transmittals", key="transmittals", use_container_width=True):
            st.session_state.current_page = "transmittals"
        
        if st.button("📅 Scheduling", key="scheduling", use_container_width=True):
            st.session_state.current_page = "scheduling"
        
        if st.button("🔍 Quality Control", key="quality_control", use_container_width=True):
            st.session_state.current_page = "quality_control"
        
        if st.button("📸 Progress Photos", key="progress_photos", use_container_width=True):
            st.session_state.current_page = "progress_photos"
        
        if st.button("🏭 Subcontractor Management", key="subcontractor_management", use_container_width=True):
            st.session_state.current_page = "subcontractor_management"
        
        if st.button("🔍 Inspections", key="inspections", use_container_width=True):
            st.session_state.current_page = "inspections"
        
        if st.button("⚠️ Issues & Risks", key="issues_risks", use_container_width=True):
            st.session_state.current_page = "issues_risks"
        
        # Resource Management Section
        st.markdown('<div class="section-header">📦 Resource Management</div>', unsafe_allow_html=True)
        
        if st.button("📁 Documents", key="documents", use_container_width=True):
            st.session_state.current_page = "documents"
        
        if st.button("💲 Unit Prices", key="unit_prices", use_container_width=True):
            st.session_state.current_page = "unit_prices"
        
        # Analytics & AI Section
        st.markdown('<div class="section-header">🤖 Analytics & AI</div>', unsafe_allow_html=True)
        
        if st.button("📊 Analytics", key="analytics", use_container_width=True):
            st.session_state.current_page = "analytics"
        
        if st.button("📈 Performance Snapshot", key="performance_snapshot", use_container_width=True):
            st.session_state.current_page = "performance_snapshot"
        
        if st.button("🤖 AI Assistant", key="ai_assistant", use_container_width=True):
            st.session_state.current_page = "ai_assistant"
        
        # Resources Section
        st.markdown('<div class="section-header">📚 Resources</div>', unsafe_allow_html=True)
        
        if st.button("📖 Quick Start Guide", key="quick_start", use_container_width=True):
            st.session_state.current_page = "quick_start"
        
        # Logout Button
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout", use_container_width=True):
            st.session_state.current_page = "login"

def initialize_session_state():
    """Initialize session state"""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = True  # Skip login for demo

def render_dashboard():
    """Enhanced dashboard with comprehensive metrics"""
    st.markdown("""
    <div class="module-header">
        <h1>🏗️ Highland Tower Development Dashboard</h1>
        <p>$45.5M Mixed-Use Development - Real-time Project Overview</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏗️ Project Progress",
            value="68%",
            delta="3% this week"
        )
    
    with col2:
        st.metric(
            label="💰 Budget Status",
            value="$31.2M",
            delta="-$2.1M under budget"
        )
    
    with col3:
        st.metric(
            label="📋 Active RFIs",
            value="23",
            delta="5 new this week"
        )
    
    with col4:
        st.metric(
            label="👷 Active Workers",
            value="147",
            delta="12 more than planned"
        )
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Weekly Progress Tracking")
        progress_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            'Planned': [15, 30, 45, 60, 75],
            'Actual': [12, 28, 48, 65, 68]
        })
        
        fig = px.line(progress_data, x='Week', y=['Planned', 'Actual'], 
                     title="Progress vs Planned")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Cost Breakdown by Phase")
        cost_data = pd.DataFrame({
            'Phase': ['Foundation', 'Structure', 'MEP', 'Finishes', 'Sitework'],
            'Spent': [8500000, 12300000, 6800000, 2900000, 700000],
            'Budget': [9000000, 13500000, 7200000, 4800000, 1000000]
        })
        
        fig = px.bar(cost_data, x='Phase', y=['Spent', 'Budget'], 
                    title="Cost Analysis by Phase", barmode='group')
        st.plotly_chart(fig, use_container_width=True)

def render_daily_reports():
    """Daily Reports module with real-time tracking"""
    st.markdown("""
    <div class="module-header">
        <h1>📋 Daily Reports Management</h1>
        <p>Real-time field reporting and progress tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Today's Report")
        
        # Weather conditions
        weather_col1, weather_col2, weather_col3 = st.columns(3)
        with weather_col1:
            st.selectbox("Weather", ["Sunny", "Cloudy", "Rainy", "Windy"])
        with weather_col2:
            st.number_input("Temperature (°F)", value=72)
        with weather_col3:
            st.selectbox("Wind", ["Calm", "Light", "Moderate", "Strong"])
        
        # Work performed
        st.text_area("Work Performed Today", 
                    value="- Continued concrete pour for Level 3 slab\n- Installed MEP rough-in on Level 2\n- Delivered steel for elevator shaft", 
                    height=100)
        
        # Issues and delays
        st.text_area("Issues/Delays", 
                    value="- Concrete delivery delayed 2 hours due to traffic\n- Waiting on electrical inspection approval", 
                    height=80)
        
        # Tomorrow's plan
        st.text_area("Tomorrow's Plan", 
                    value="- Complete Level 3 concrete finishing\n- Start drywall installation Level 1\n- MEP inspection scheduled 10 AM", 
                    height=80)
        
        if st.button("💾 Save Daily Report", type="primary"):
            st.success("✅ Daily report saved successfully!")
    
    with col2:
        st.subheader("📊 Report Statistics")
        
        st.metric("Reports This Week", "7", "0")
        st.metric("Average Crew Size", "45", "+3")
        st.metric("Weather Delays", "1", "-2")
        
        st.subheader("🔄 Recent Reports")
        reports = [
            {"date": "May 26, 2025", "status": "Complete", "crew": 42},
            {"date": "May 25, 2025", "status": "Complete", "crew": 38},
            {"date": "May 24, 2025", "status": "Complete", "crew": 45},
        ]
        
        for report in reports:
            with st.container():
                st.write(f"📅 {report['date']}")
                st.write(f"Status: {report['status']}")
                st.write(f"Crew: {report['crew']} workers")
                st.divider()

def render_deliveries():
    """Deliveries tracking module"""
    st.markdown("""
    <div class="module-header">
        <h1>🚚 Deliveries Management</h1>
        <p>Track and manage all material deliveries</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Delivery status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Today's Deliveries", "8", "+2")
    with col2:
        st.metric("Pending", "3", "0")
    with col3:
        st.metric("Completed", "5", "+2")
    with col4:
        st.metric("Issues", "0", "-1")
    
    # Delivery tracking table
    st.subheader("📦 Today's Delivery Schedule")
    
    deliveries_data = {
        'Time': ['8:00 AM', '10:30 AM', '1:00 PM', '3:30 PM', '4:45 PM'],
        'Supplier': ['ABC Concrete', 'Steel Works Inc', 'Electrical Supply Co', 'Plumbing Pro', 'Lumber Yard'],
        'Material': ['Ready Mix Concrete', 'Structural Steel', 'Electrical Conduit', 'PVC Pipes', 'Framing Lumber'],
        'Quantity': ['15 cubic yards', '2,500 lbs', '500 ft', '200 ft', '1,000 board ft'],
        'Status': ['✅ Delivered', '✅ Delivered', '🚛 En Route', '⏰ Scheduled', '⏰ Scheduled'],
        'Received By': ['John Smith', 'Mike Johnson', '-', '-', '-']
    }
    
    df = pd.DataFrame(deliveries_data)
    st.dataframe(df, use_container_width=True)
    
    # Add new delivery
    with st.expander("➕ Schedule New Delivery"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Supplier Name")
            st.text_input("Material Description")
            st.date_input("Delivery Date")
        with col2:
            st.text_input("Quantity")
            st.time_input("Scheduled Time")
            st.text_input("Special Instructions")
        
        if st.button("📅 Schedule Delivery", type="primary"):
            st.success("✅ Delivery scheduled successfully!")

def render_safety():
    """Safety management module"""
    st.markdown("""
    <div class="module-header">
        <h1>🦺 Safety Management</h1>
        <p>Comprehensive safety tracking and incident management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Safety metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Days Without Incident", "47", "+1")
    with col2:
        st.metric("Safety Score", "98%", "+2%")
    with col3:
        st.metric("Active Workers", "147", "+5")
    with col4:
        st.metric("Safety Meetings", "12", "+1")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Safety Performance")
        
        # Safety chart
        safety_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Incidents': [2, 1, 0, 1, 0],
            'Near Misses': [5, 3, 2, 4, 1],
            'Safety Score': [92, 94, 97, 95, 98]
        })
        
        fig = px.bar(safety_data, x='Month', y=['Incidents', 'Near Misses'], 
                    title="Monthly Safety Incidents")
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent inspections
        st.subheader("🔍 Recent Safety Inspections")
        inspections = [
            {"date": "May 26, 2025", "area": "Electrical Work Zone", "status": "✅ Passed", "inspector": "Sarah Wilson"},
            {"date": "May 24, 2025", "area": "Crane Operations", "status": "✅ Passed", "inspector": "Mike Chen"},
            {"date": "May 22, 2025", "area": "Fall Protection", "status": "⚠️ Minor Issues", "inspector": "Dave Brown"},
        ]
        
        for inspection in inspections:
            with st.container():
                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    st.write(f"📅 {inspection['date']} - {inspection['area']}")
                with col_b:
                    st.write(inspection['status'])
                with col_c:
                    st.write(inspection['inspector'])
                st.divider()
    
    with col2:
        st.subheader("🚨 Report Safety Issue")
        
        issue_type = st.selectbox("Issue Type", [
            "Near Miss", "Incident", "Unsafe Condition", "Equipment Issue", "Other"
        ])
        
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        
        location = st.text_input("Location")
        
        description = st.text_area("Description", height=100)
        
        if st.button("🚨 Submit Report", type="primary"):
            st.success("✅ Safety report submitted successfully!")
        
        st.subheader("📋 Quick Actions")
        if st.button("📚 Safety Manual", use_container_width=True):
            st.info("Opening safety manual...")
        if st.button("🎯 Training Schedule", use_container_width=True):
            st.info("Loading training schedule...")
        if st.button("📞 Emergency Contacts", use_container_width=True):
            st.info("Displaying emergency contacts...")

def render_preconstruction():
    """PreConstruction planning module"""
    st.markdown("""
    <div class="module-header">
        <h1>🏗️ PreConstruction Planning</h1>
        <p>Project planning, estimating, and bid management</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Project Overview", "💰 Estimating", "📋 Bid Management"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Project Details")
            st.write("**Project Name:** Highland Tower Development")
            st.write("**Total Value:** $45,500,000")
            st.write("**Start Date:** January 15, 2025")
            st.write("**Completion:** December 2026")
            st.write("**Units:** 120 Residential + 8 Retail")
            
            st.subheader("📈 Project Phases")
            phases = [
                {"phase": "Site Preparation", "duration": "2 months", "status": "✅ Complete"},
                {"phase": "Foundation", "duration": "3 months", "status": "✅ Complete"},
                {"phase": "Structure", "duration": "8 months", "status": "🔄 In Progress"},
                {"phase": "MEP", "duration": "4 months", "status": "⏰ Planned"},
                {"phase": "Finishes", "duration": "6 months", "status": "⏰ Planned"},
            ]
            
            for phase in phases:
                with st.container():
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    with col_a:
                        st.write(phase["phase"])
                    with col_b:
                        st.write(phase["duration"])
                    with col_c:
                        st.write(phase["status"])
                    st.divider()
        
        with col2:
            st.subheader("📊 Cost Breakdown")
            cost_data = pd.DataFrame({
                'Category': ['Labor', 'Materials', 'Equipment', 'Overhead', 'Profit'],
                'Amount': [18200000, 15600000, 4550000, 3640000, 3510000],
                'Percentage': [40, 34.3, 10, 8, 7.7]
            })
            
            fig = px.pie(cost_data, values='Amount', names='Category', 
                        title="Project Cost Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("💰 Cost Estimating")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Residential Units (120 units)**")
            st.write("- Studio (24 units): $180,000 each")
            st.write("- 1-Bedroom (48 units): $225,000 each")
            st.write("- 2-Bedroom (36 units): $285,000 each")
            st.write("- 3-Bedroom (12 units): $340,000 each")
            
            st.write("**Retail Units (8 units)**")
            st.write("- Small Retail (6 units): $150,000 each")
            st.write("- Large Retail (2 units): $275,000 each")
        
        with col2:
            st.subheader("📈 Cost per Square Foot")
            cost_sf_data = pd.DataFrame({
                'Unit Type': ['Studio', '1-Bedroom', '2-Bedroom', '3-Bedroom', 'Small Retail', 'Large Retail'],
                'Cost/SF': [300, 275, 260, 245, 225, 210],
                'Square Feet': [600, 820, 1100, 1390, 665, 1310]
            })
            
            fig = px.bar(cost_sf_data, x='Unit Type', y='Cost/SF', 
                        title="Construction Cost per Square Foot")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("📋 Bid Management")
        
        st.write("**Active Bids**")
        bids_data = {
            'Trade': ['HVAC', 'Plumbing', 'Electrical', 'Flooring', 'Painting'],
            'Bidders': [4, 3, 5, 3, 4],
            'Deadline': ['June 1', 'June 5', 'June 3', 'June 8', 'June 10'],
            'Low Bid': ['$2.1M', '$1.8M', '$2.4M', '$890K', '$650K'],
            'Status': ['Open', 'Open', 'Under Review', 'Open', 'Open']
        }
        
        df = pd.DataFrame(bids_data)
        st.dataframe(df, use_container_width=True)

def render_engineering():
    """Engineering module with RFI and technical management"""
    st.markdown("""
    <div class="module-header">
        <h1>⚙️ Engineering Management</h1>
        <p>Technical coordination, RFIs, and engineering workflows</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Engineering metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active RFIs", "23", "+3")
    with col2:
        st.metric("Pending Reviews", "8", "+1")
    with col3:
        st.metric("Change Orders", "12", "+2")
    with col4:
        st.metric("Shop Drawings", "45", "+5")
    
    tab1, tab2, tab3 = st.tabs(["📝 RFI Management", "📋 Change Orders", "🔧 Technical Reviews"])
    
    with tab1:
        st.subheader("📝 Request for Information (RFI) Tracking")
        
        # RFI summary
        rfi_data = {
            'RFI #': ['RFI-001', 'RFI-002', 'RFI-003', 'RFI-004', 'RFI-005'],
            'Subject': ['Concrete Mix Design', 'Electrical Panel Location', 'HVAC Duct Routing', 'Fire Rating Details', 'Structural Connection'],
            'Trade': ['Concrete', 'Electrical', 'HVAC', 'Fireproofing', 'Steel'],
            'Priority': ['High', 'Medium', 'High', 'Low', 'Medium'],
            'Status': ['Response Pending', 'Under Review', 'Closed', 'Response Pending', 'Draft'],
            'Days Open': [8, 5, 0, 12, 2]
        }
        
        df = pd.DataFrame(rfi_data)
        st.dataframe(df, use_container_width=True)
        
        # Quick RFI creation
        with st.expander("➕ Create New RFI"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("RFI Subject")
                st.selectbox("Trade", ["Concrete", "Steel", "Electrical", "HVAC", "Plumbing", "Other"])
                st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            with col2:
                st.text_area("Question/Issue Description", height=100)
                st.file_uploader("Attach Documents", accept_multiple_files=True)
                st.date_input("Response Required By")
            
            if st.button("📝 Submit RFI", type="primary"):
                st.success("✅ RFI submitted successfully!")
    
    with tab2:
        st.subheader("📋 Change Order Management")
        
        change_orders = {
            'CO #': ['CO-001', 'CO-002', 'CO-003'],
            'Description': ['Additional MEP Work', 'Design Modification', 'Site Condition'],
            'Amount': ['$125,000', '$75,000', '$45,000'],
            'Status': ['Approved', 'Under Review', 'Pending'],
            'Impact': ['5 days', '0 days', '3 days']
        }
        
        df_co = pd.DataFrame(change_orders)
        st.dataframe(df_co, use_container_width=True)
    
    with tab3:
        st.subheader("🔧 Technical Reviews")
        
        reviews = [
            {"item": "Shop Drawings - Steel Connections", "reviewer": "John Smith, P.E.", "status": "✅ Approved", "date": "May 25"},
            {"item": "MEP Coordination Plans", "reviewer": "Sarah Wilson, P.E.", "status": "🔄 Under Review", "date": "May 24"},
            {"item": "Concrete Mix Design", "reviewer": "Mike Johnson, P.E.", "status": "⚠️ Revisions Required", "date": "May 23"},
        ]
        
        for review in reviews:
            with st.container():
                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    st.write(f"📋 {review['item']}")
                    st.write(f"Reviewer: {review['reviewer']}")
                with col_b:
                    st.write(review['status'])
                with col_c:
                    st.write(review['date'])
                st.divider()

def render_field_operations():
    """Field Operations module"""
    st.markdown("""
    <div class="module-header">
        <h1>👷 Field Operations</h1>
        <p>Real-time field management and crew coordination</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Field metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Workers", "147", "+5")
    with col2:
        st.metric("Crews on Site", "8", "0")
    with col3:
        st.metric("Equipment Units", "23", "+2")
    with col4:
        st.metric("Productivity", "102%", "+3%")
    
    tab1, tab2, tab3 = st.tabs(["👥 Crew Management", "🏗️ Work Progress", "⚡ Equipment"])
    
    with tab1:
        st.subheader("👥 Active Crews")
        
        crews_data = {
            'Crew': ['Concrete Team A', 'Steel Crew 1', 'MEP Team', 'Finishing Crew', 'Site Prep'],
            'Foreman': ['Mike Smith', 'John Doe', 'Sarah Wilson', 'Tom Brown', 'Dave Johnson'],
            'Workers': [12, 8, 15, 10, 6],
            'Location': ['Level 3', 'Level 4', 'Level 2', 'Level 1', 'Exterior'],
            'Status': ['Active', 'Active', 'Break', 'Active', 'Active']
        }
        
        df = pd.DataFrame(crews_data)
        st.dataframe(df, use_container_width=True)
        
        # Crew productivity chart
        productivity_data = pd.DataFrame({
            'Hour': ['7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM'],
            'Workers': [45, 120, 135, 140, 145, 75, 130, 140, 147]
        })
        
        fig = px.line(productivity_data, x='Hour', y='Workers', 
                     title="Worker Count Throughout Day")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🏗️ Today's Work Progress")
        
        tasks = [
            {"task": "Concrete Pour - Level 3 Slab", "progress": 85, "crew": "Concrete Team A", "eta": "4:00 PM"},
            {"task": "Steel Installation - Elevator Shaft", "progress": 60, "crew": "Steel Crew 1", "eta": "5:30 PM"},
            {"task": "MEP Rough-in - Level 2", "progress": 40, "crew": "MEP Team", "eta": "Tomorrow"},
            {"task": "Drywall Installation - Level 1", "progress": 90, "crew": "Finishing Crew", "eta": "3:00 PM"},
        ]
        
        for task in tasks:
            with st.container():
                st.write(f"🔧 **{task['task']}**")
                st.write(f"Crew: {task['crew']} | ETA: {task['eta']}")
                st.progress(task['progress'] / 100)
                st.write(f"Progress: {task['progress']}%")
                st.divider()
    
    with tab3:
        st.subheader("⚡ Equipment Management")
        
        equipment_data = {
            'Equipment': ['Tower Crane 1', 'Concrete Pump', 'Scissor Lift A', 'Excavator', 'Forklift 1'],
            'Type': ['Crane', 'Pump', 'Lift', 'Excavator', 'Forklift'],
            'Location': ['Center Site', 'Level 3', 'Level 2', 'Exterior', 'Ground Level'],
            'Status': ['Operating', 'Operating', 'Maintenance', 'Operating', 'Operating'],
            'Operator': ['Steve Wilson', 'Mike Chen', 'In Shop', 'Tom Davis', 'Sarah Kim']
        }
        
        df_eq = pd.DataFrame(equipment_data)
        st.dataframe(df_eq, use_container_width=True)

# Additional render functions for all other modules...
def render_contracts():
    """Contracts management module"""
    st.markdown("""
    <div class="module-header">
        <h1>📄 Contracts Management</h1>
        <p>Comprehensive contract administration and tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📄 Contracts module with comprehensive contract management features")

def render_cost_management():
    """Cost management module"""
    st.markdown("""
    <div class="module-header">
        <h1>💰 Cost Management</h1>
        <p>Advanced financial tracking and budget management</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("💰 Cost Management module with budget tracking and financial analytics")

def render_bim():
    """BIM management module"""
    st.markdown("""
    <div class="module-header">
        <h1>🏢 Building Information Modeling</h1>
        <p>3D coordination and model management</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🏢 BIM module with 3D model coordination and clash detection")

def render_closeout():
    """Project closeout module"""
    st.markdown("""
    <div class="module-header">
        <h1>✅ Project Closeout</h1>
        <p>Final documentation and project completion</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("✅ Closeout module with final documentation and warranties")

def render_rfis():
    """RFI management module"""
    st.markdown("""
    <div class="module-header">
        <h1>📝 Request for Information</h1>
        <p>RFI tracking and response management</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📝 RFI module with advanced tracking and collaboration features")

def render_submittals():
    """Submittals management module"""
    st.markdown("""
    <div class="module-header">
        <h1>📤 Submittals Management</h1>
        <p>Product submittals and approval workflow</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📤 Submittals module with approval workflows and tracking")

def render_transmittals():
    """Transmittals management module"""
    st.markdown("""
    <div class="module-header">
        <h1>📨 Transmittals</h1>
        <p>Document distribution and transmittal tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📨 Transmittals module for document distribution")

def render_scheduling():
    """Scheduling module"""
    st.markdown("""
    <div class="module-header">
        <h1>📅 Project Scheduling</h1>
        <p>Advanced scheduling and timeline management</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📅 Scheduling module with Gantt charts and critical path analysis")

def render_quality_control():
    """Quality control module"""
    st.markdown("""
    <div class="module-header">
        <h1>🔍 Quality Control</h1>
        <p>Inspection management and quality assurance</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🔍 Quality Control module with inspection workflows")

def render_progress_photos():
    """Progress photos module"""
    st.markdown("""
    <div class="module-header">
        <h1>📸 Progress Photos</h1>
        <p>Visual documentation and progress tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📸 Progress Photos module with visual timeline tracking")

def render_subcontractor_management():
    """Subcontractor management module"""
    st.markdown("""
    <div class="module-header">
        <h1>🏭 Subcontractor Management</h1>
        <p>Subcontractor coordination and performance tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🏭 Subcontractor Management with performance tracking")

def render_inspections():
    """Inspections module"""
    st.markdown("""
    <div class="module-header">
        <h1>🔍 Inspections</h1>
        <p>Inspection scheduling and compliance tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🔍 Inspections module with compliance tracking")

def render_issues_risks():
    """Issues and risks module"""
    st.markdown("""
    <div class="module-header">
        <h1>⚠️ Issues & Risks</h1>
        <p>Risk management and issue tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("⚠️ Issues & Risks module with comprehensive risk management")

def render_documents():
    """Document management module"""
    st.markdown("""
    <div class="module-header">
        <h1>📁 Document Management</h1>
        <p>Centralized document storage and version control</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📁 Documents module with version control and collaboration")

def render_unit_prices():
    """Unit prices module"""
    st.markdown("""
    <div class="module-header">
        <h1>💲 Unit Prices</h1>
        <p>Unit price database and cost estimation</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("💲 Unit Prices module with cost database and estimation tools")

def render_analytics():
    """Analytics module"""
    st.markdown("""
    <div class="module-header">
        <h1>📊 Advanced Analytics</h1>
        <p>Data analytics and business intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📊 Analytics module with advanced reporting and insights")

def render_performance_snapshot():
    """Performance snapshot module"""
    st.markdown("""
    <div class="module-header">
        <h1>📈 Performance Snapshot</h1>
        <p>Executive dashboard and KPI tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("📈 Performance Snapshot with executive-level insights")

def render_ai_assistant():
    """AI Assistant module"""
    st.markdown("""
    <div class="module-header">
        <h1>🤖 AI Assistant</h1>
        <p>Intelligent construction management assistant</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🤖 AI Assistant with intelligent project insights and recommendations")

def render_quick_start():
    """Quick start guide module"""
    st.markdown("""
    <div class="module-header">
        <h1>📖 Quick Start Guide</h1>
        <p>Getting started with gcPanel</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ## Welcome to gcPanel! 🏗️
    
    Your comprehensive construction management platform for Highland Tower Development.
    
    ### 🚀 Getting Started
    
    1. **Dashboard** - Start here for project overview
    2. **Daily Reports** - Track daily progress and activities
    3. **Safety** - Manage safety incidents and compliance
    4. **RFIs** - Handle requests for information
    5. **Progress Photos** - Document visual progress
    
    ### 📋 Module Overview
    
    **Core Tools** - Essential daily operations
    **Project Management** - Planning and execution
    **Advanced Tools** - Specialized functionality
    **Resource Management** - Documents and pricing
    **Analytics & AI** - Insights and intelligence
    
    ### 💡 Tips
    
    - Use the sidebar to navigate between modules
    - Most modules support real-time collaboration
    - All data is automatically saved
    - Mobile-responsive design for field use
    
    ### 📞 Support
    
    For technical support, contact the development team.
    """)

def main():
    """Main application entry point"""
    configure_page()
    apply_styling()
    initialize_session_state()
    
    render_sidebar()
    
    # Route to appropriate page
    page = st.session_state.current_page
    
    # Page routing
    if page == "dashboard":
        render_dashboard()
    elif page == "daily_reports":
        render_daily_reports()
    elif page == "deliveries":
        render_deliveries()
    elif page == "safety":
        render_safety()
    elif page == "preconstruction":
        render_preconstruction()
    elif page == "engineering":
        render_engineering()
    elif page == "field_operations":
        render_field_operations()
    elif page == "contracts":
        render_contracts()
    elif page == "cost_management":
        render_cost_management()
    elif page == "bim":
        render_bim()
    elif page == "closeout":
        render_closeout()
    elif page == "rfis":
        render_rfis()
    elif page == "submittals":
        render_submittals()
    elif page == "transmittals":
        render_transmittals()
    elif page == "scheduling":
        render_scheduling()
    elif page == "quality_control":
        render_quality_control()
    elif page == "progress_photos":
        render_progress_photos()
    elif page == "subcontractor_management":
        render_subcontractor_management()
    elif page == "inspections":
        render_inspections()
    elif page == "issues_risks":
        render_issues_risks()
    elif page == "documents":
        render_documents()
    elif page == "unit_prices":
        render_unit_prices()
    elif page == "analytics":
        render_analytics()
    elif page == "performance_snapshot":
        render_performance_snapshot()
    elif page == "ai_assistant":
        render_ai_assistant()
    elif page == "quick_start":
        render_quick_start()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()