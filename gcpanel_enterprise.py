"""
Highland Tower Development - gcPanel Enterprise
$45.5M Mixed-Use Construction Management Platform
Single-file architecture with integrated modules for maximum performance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional

# Configure page
st.set_page_config(
    page_title="Highland Tower Development - gcPanel Enterprise",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_session_state():
    defaults = {
        'authenticated': False,
        'username': '',
        'user_role': 'user',
        'current_menu': 'Dashboard',
        'theme': 'dark'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Apply enterprise theme
def apply_enterprise_theme():
    theme = st.session_state.get('theme', 'dark')
    
    if theme == 'dark':
        colors = {
            'primary': '#4A90E2',
            'secondary': '#5BA0F2',
            'accent': '#6BB6FF',
            'success': '#28A745',
            'bg_primary': '#1A1D29',
            'bg_secondary': '#252A3A',
            'bg_card': '#2D3348',
            'text_primary': '#FFFFFF',
            'text_secondary': '#B8BCC8'
        }
    else:
        colors = {
            'primary': '#2E7BD4',
            'secondary': '#1E6BBF',
            'accent': '#0A5AA3',
            'success': '#218838',
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F8F9FA',
            'bg_card': '#FFFFFF',
            'text_primary': '#212529',
            'text_secondary': '#6C757D'
        }
    
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, {colors['bg_primary']} 0%, {colors['bg_secondary']} 100%);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}
    h1, h2, h3 {{ color: {colors['primary']} !important; font-weight: 600; }}
    .stSidebar {{ background: {colors['bg_card']}; }}
    .stButton > button {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem;
        font-weight: 500; transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        background: linear-gradient(135deg, {colors['secondary']} 0%, {colors['accent']} 100%);
        transform: translateY(-1px);
    }}
    .stMetric {{
        background: {colors['bg_card']}; padding: 1.5rem; border-radius: 12px;
        border-left: 4px solid {colors['primary']}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .enterprise-card {{
        background: {colors['bg_card']}; padding: 1.5rem; border-radius: 12px;
        border: 1px solid {colors['primary']}20; margin: 1rem 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# Render login
def render_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="enterprise-card" style="text-align: center;">
            <h1>🏗️ gcPanel Enterprise</h1>
            <p>Highland Tower Development</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Login", use_container_width=True):
                if username and password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = "admin" if username.lower() == "admin" else "user"
                    st.rerun()
                else:
                    st.error("Please enter credentials")
        with col_b:
            if st.button("Demo Access", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.username = "Demo User"
                st.session_state.user_role = "user"
                st.rerun()

# Render sidebar
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #4A90E2; font-size: 1.5rem;">gcPanel</h1>
            <p style="color: #6C757D; font-size: 0.75rem;">Enterprise Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        st.markdown(f"""
        <div class="enterprise-card">
            <p>👤 {st.session_state.username}</p>
            <p style="font-size: 0.75rem; color: #6C757D;">Role: {st.session_state.user_role.title()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        menu_items = [
            ("📊", "Dashboard"),
            ("🏗️", "PreConstruction"),
            ("⚙️", "Engineering"),
            ("👷", "Field Operations"),
            ("🦺", "Safety"),
            ("📋", "Contracts"),
            ("💰", "Cost Management"),
            ("🏢", "BIM"),
            ("✅", "Closeout"),
            ("📈", "Analytics"),
            ("📁", "Documents"),
            ("⚙️", "Settings")
        ]
        
        st.subheader("Navigation")
        for icon, menu in menu_items:
            if st.button(f"{icon} {menu}", key=f"nav_{menu}", use_container_width=True):
                st.session_state.current_menu = menu
                st.rerun()
        
        st.markdown("---")
        
        # Theme toggle
        theme_label = "🌙 Dark" if st.session_state.theme == 'dark' else "☀️ Light"
        if st.button(f"Theme: {theme_label}", use_container_width=True):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# Dashboard module
def render_dashboard():
    st.title("📊 Enterprise Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Project Progress", "68%", "↗️ +12%")
    with col2:
        st.metric("Budget Performance", "$31.2M", "↗️ +$2.8M")
    with col3:
        st.metric("Safety Score", "99.2%", "↗️ +0.8%")
    with col4:
        st.metric("Quality Index", "96.5%", "↗️ +1.2%")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Progress Analytics")
        progress_data = pd.DataFrame({
            'Week': range(1, 13),
            'Planned': [5, 12, 20, 28, 35, 42, 50, 58, 65, 72, 80, 87],
            'Actual': [4, 11, 22, 30, 37, 45, 52, 60, 68, 75, 82, 88]
        })
        fig = px.line(progress_data, x='Week', y=['Planned', 'Actual'], 
                     color_discrete_map={'Planned': '#6C757D', 'Actual': '#4A90E2'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Cost Analysis")
        cost_data = pd.DataFrame({
            'Category': ['Foundation', 'Structure', 'MEP', 'Finishes', 'Sitework'],
            'Budget': [8500000, 15200000, 12800000, 6200000, 2800000],
            'Actual': [8200000, 14800000, 11900000, 5800000, 2600000]
        })
        fig = px.bar(cost_data, x='Category', y=['Budget', 'Actual'], barmode='group',
                    color_discrete_map={'Budget': '#6C757D', 'Actual': '#4A90E2'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# PreConstruction module
def render_preconstruction():
    st.title("🏗️ PreConstruction")
    
    tabs = st.tabs(["Project Planning", "Permits", "Estimates", "Schedules"])
    
    with tabs[0]:
        st.subheader("📋 Project Planning")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="enterprise-card">
                <h4>Project Overview</h4>
                <p><strong>Highland Tower Development</strong></p>
                <p>$45.5M Mixed-Use Project</p>
                <p>120 Residential + 8 Retail Units</p>
                <p>15 Stories Above Ground + 2 Below</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="enterprise-card">
                <h4>Key Milestones</h4>
                <p>✅ Site Preparation Complete</p>
                <p>🔄 Foundation in Progress</p>
                <p>⏳ Steel Delivery Scheduled</p>
                <p>⏳ MEP Rough-in Planned</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.subheader("📄 Permits & Approvals")
        permits_data = pd.DataFrame({
            'Permit Type': ['Building Permit', 'MEP Permit', 'Fire Safety', 'Occupancy'],
            'Status': ['Approved', 'In Review', 'Pending', 'Not Started'],
            'Submitted': ['2024-01-15', '2024-02-01', '2024-02-15', 'TBD'],
            'Expected Approval': ['2024-02-15', '2024-03-01', '2024-03-15', '2024-12-01']
        })
        st.dataframe(permits_data, use_container_width=True)
    
    with tabs[2]:
        st.subheader("💲 Cost Estimates")
        estimate_data = pd.DataFrame({
            'Work Package': ['Site Prep', 'Foundation', 'Structure', 'MEP', 'Finishes'],
            'Estimated Cost': [2800000, 8500000, 15200000, 12800000, 6200000],
            'Contingency': [280000, 850000, 1520000, 1280000, 620000],
            'Total': [3080000, 9350000, 16720000, 14080000, 6820000]
        })
        st.dataframe(estimate_data, use_container_width=True)
    
    with tabs[3]:
        st.subheader("📅 Master Schedule")
        schedule_data = pd.DataFrame({
            'Phase': ['Site Preparation', 'Foundation', 'Structure', 'MEP Rough-in', 'Finishes'],
            'Start Date': ['2024-01-01', '2024-02-15', '2024-04-01', '2024-08-01', '2024-11-01'],
            'Duration (weeks)': [6, 8, 16, 12, 20],
            'Status': ['Complete', 'In Progress', 'Scheduled', 'Scheduled', 'Scheduled']
        })
        st.dataframe(schedule_data, use_container_width=True)

# Engineering module
def render_engineering():
    st.title("⚙️ Engineering")
    
    tabs = st.tabs(["RFIs", "Submittals", "Transmittals", "Change Orders"])
    
    with tabs[0]:
        st.subheader("❓ Requests for Information")
        rfi_data = pd.DataFrame({
            'RFI #': ['RFI-001', 'RFI-002', 'RFI-003', 'RFI-004'],
            'Subject': ['Foundation Detail Clarification', 'Steel Connection Detail', 'MEP Coordination', 'Finish Schedule'],
            'From': ['Field Supervisor', 'Steel Contractor', 'MEP Contractor', 'GC'],
            'Status': ['Open', 'Answered', 'Open', 'Draft'],
            'Date': ['2024-05-20', '2024-05-18', '2024-05-22', '2024-05-23']
        })
        st.dataframe(rfi_data, use_container_width=True)
    
    with tabs[1]:
        st.subheader("📋 Submittals")
        submittal_data = pd.DataFrame({
            'Submittal #': ['SUB-001', 'SUB-002', 'SUB-003', 'SUB-004'],
            'Description': ['Structural Steel Shop Drawings', 'MEP Equipment Specs', 'Concrete Mix Design', 'Window Systems'],
            'Contractor': ['Steel Inc', 'MEP Solutions', 'Concrete Co', 'Window Pro'],
            'Status': ['Under Review', 'Approved', 'Revise & Resubmit', 'Not Submitted'],
            'Due Date': ['2024-05-25', '2024-05-20', '2024-05-28', '2024-06-01']
        })
        st.dataframe(submittal_data, use_container_width=True)
    
    with tabs[2]:
        st.subheader("📤 Transmittals")
        transmittal_data = pd.DataFrame({
            'Transmittal #': ['TRX-001', 'TRX-002', 'TRX-003'],
            'Description': ['Revised Architectural Drawings', 'Updated Structural Calcs', 'MEP Coordination Drawings'],
            'To': ['All Contractors', 'Steel Contractor', 'MEP Contractor'],
            'Date Sent': ['2024-05-15', '2024-05-18', '2024-05-21'],
            'Acknowledgment': ['Received', 'Received', 'Pending']
        })
        st.dataframe(transmittal_data, use_container_width=True)
    
    with tabs[3]:
        st.subheader("🔄 Change Orders")
        co_data = pd.DataFrame({
            'CO #': ['CO-001', 'CO-002', 'CO-003'],
            'Description': ['Additional Foundation Work', 'MEP Scope Addition', 'Finish Upgrade'],
            'Cost Impact': [125000, 85000, 65000],
            'Time Impact': ['2 weeks', '1 week', '0 days'],
            'Status': ['Approved', 'Under Review', 'Approved']
        })
        st.dataframe(co_data, use_container_width=True)

# Field Operations module
def render_field_operations():
    st.title("👷 Field Operations")
    
    tabs = st.tabs(["Daily Reports", "Progress Photos", "Quality Control", "Inspections"])
    
    with tabs[0]:
        st.subheader("📋 Daily Reports")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="enterprise-card">
                <h4>Today's Activities</h4>
                <p>• Foundation pour - Area B2-East</p>
                <p>• Steel delivery inspection</p>
                <p>• MEP rough-in coordination</p>
                <p>• Safety meeting conducted</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="enterprise-card">
                <h4>Crew Summary</h4>
                <p>• Concrete crew: 12 workers</p>
                <p>• Steel crew: 8 workers</p>
                <p>• MEP crew: 6 workers</p>
                <p>• Total on site: 26 workers</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.subheader("📸 Progress Photos")
        photo_dates = ['2024-05-20', '2024-05-21', '2024-05-22', '2024-05-23']
        selected_date = st.selectbox("Select Date", photo_dates)
        st.info(f"Progress photos for {selected_date} would be displayed here")
    
    with tabs[2]:
        st.subheader("✅ Quality Control")
        qc_data = pd.DataFrame({
            'Inspection Type': ['Concrete Pour', 'Steel Welding', 'MEP Installation', 'Waterproofing'],
            'Inspector': ['QC Manager', 'Welding Inspector', 'MEP QC', 'QC Manager'],
            'Date': ['2024-05-20', '2024-05-21', '2024-05-22', '2024-05-23'],
            'Result': ['Pass', 'Pass', 'Minor Issues', 'Pass'],
            'Notes': ['Good quality', 'Excellent work', 'Spacing adjustment needed', 'Proper application']
        })
        st.dataframe(qc_data, use_container_width=True)
    
    with tabs[3]:
        st.subheader("🔍 Inspections")
        inspection_data = pd.DataFrame({
            'Inspection': ['Foundation', 'Rebar Placement', 'Concrete Pour', 'Steel Erection'],
            'Inspector': ['City Inspector', 'Third Party', 'City Inspector', 'Third Party'],
            'Status': ['Passed', 'Passed', 'Scheduled', 'Pending'],
            'Date': ['2024-05-15', '2024-05-18', '2024-05-25', 'TBD']
        })
        st.dataframe(inspection_data, use_container_width=True)

# Safety module
def render_safety():
    st.title("🦺 Safety Management")
    
    tabs = st.tabs(["Safety Metrics", "Incidents", "Training", "Audits"])
    
    with tabs[0]:
        st.subheader("📊 Safety Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Days Without Incident", "127", "↗️ +1")
        with col2:
            st.metric("Safety Score", "99.2%", "↗️ +0.8%")
        with col3:
            st.metric("Training Compliance", "100%", "✅")
    
    with tabs[1]:
        st.subheader("🚨 Incident Reports")
        incident_data = pd.DataFrame({
            'Date': ['2024-01-15', '2024-03-22'],
            'Type': ['Near Miss', 'Minor Injury'],
            'Description': ['Unsecured material', 'Minor cut from tools'],
            'Action Taken': ['Toolbox talk', 'First aid, safety briefing'],
            'Status': ['Closed', 'Closed']
        })
        st.dataframe(incident_data, use_container_width=True)
    
    with tabs[2]:
        st.subheader("🎓 Safety Training")
        training_data = pd.DataFrame({
            'Training Topic': ['OSHA 10', 'Fall Protection', 'Crane Safety', 'Hazmat Handling'],
            'Required For': ['All Workers', 'Elevated Work', 'Crane Operators', 'Specialized Crew'],
            'Completion Rate': ['100%', '98%', '100%', '95%'],
            'Next Due': ['Annual', '2024-06-01', 'Annual', '2024-07-15']
        })
        st.dataframe(training_data, use_container_width=True)
    
    with tabs[3]:
        st.subheader("🔍 Safety Audits")
        audit_data = pd.DataFrame({
            'Audit Date': ['2024-05-01', '2024-04-15', '2024-04-01'],
            'Auditor': ['Safety Manager', 'Third Party', 'Safety Manager'],
            'Score': ['98%', '96%', '97%'],
            'Findings': ['2 minor', '3 minor', '2 minor'],
            'Status': ['Closed', 'Closed', 'Closed']
        })
        st.dataframe(audit_data, use_container_width=True)

# Cost Management module
def render_cost_management():
    st.title("💰 Cost Management")
    
    tabs = st.tabs(["Budget Overview", "Invoices", "Change Orders", "Cash Flow"])
    
    with tabs[0]:
        st.subheader("📊 Budget Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Budget", "$45.5M", "Baseline")
        with col2:
            st.metric("Committed", "$31.2M", "68.6%")
        with col3:
            st.metric("Remaining", "$14.3M", "31.4%")
        
        budget_data = pd.DataFrame({
            'Category': ['Site Prep', 'Foundation', 'Structure', 'MEP', 'Finishes', 'Contingency'],
            'Budget': [2800000, 8500000, 15200000, 12800000, 6200000, 2000000],
            'Committed': [2800000, 8200000, 14800000, 3200000, 1200000, 1000000],
            'Remaining': [0, 300000, 400000, 9600000, 5000000, 1000000]
        })
        st.dataframe(budget_data, use_container_width=True)
    
    with tabs[1]:
        st.subheader("📄 Invoice Management")
        invoice_data = pd.DataFrame({
            'Invoice #': ['INV-001', 'INV-002', 'INV-003', 'INV-004'],
            'Vendor': ['Concrete Co', 'Steel Inc', 'MEP Solutions', 'Site Prep LLC'],
            'Amount': [125000, 850000, 45000, 280000],
            'Status': ['Paid', 'Approved', 'Under Review', 'Paid'],
            'Due Date': ['2024-05-15', '2024-05-25', '2024-05-30', '2024-05-10']
        })
        st.dataframe(invoice_data, use_container_width=True)
    
    with tabs[2]:
        st.subheader("🔄 Change Order Impact")
        co_financial = pd.DataFrame({
            'Change Order': ['CO-001', 'CO-002', 'CO-003'],
            'Description': ['Additional Foundation', 'MEP Addition', 'Finish Upgrade'],
            'Cost': [125000, 85000, 65000],
            'Status': ['Approved', 'Under Review', 'Approved'],
            'Budget Impact': ['+2.8%', '+1.9%', '+1.4%']
        })
        st.dataframe(co_financial, use_container_width=True)
    
    with tabs[3]:
        st.subheader("💹 Cash Flow Projection")
        cashflow_data = pd.DataFrame({
            'Month': ['May 2024', 'Jun 2024', 'Jul 2024', 'Aug 2024', 'Sep 2024'],
            'Projected Costs': [2800000, 3200000, 4100000, 3800000, 2900000],
            'Actual Costs': [2650000, 3150000, 0, 0, 0],
            'Variance': [-150000, -50000, 0, 0, 0]
        })
        fig = px.line(cashflow_data, x='Month', y=['Projected Costs', 'Actual Costs'],
                     color_discrete_map={'Projected Costs': '#6C757D', 'Actual Costs': '#4A90E2'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# BIM module
def render_bim():
    st.title("🏢 Building Information Modeling")
    
    tabs = st.tabs(["3D Viewer", "Clash Detection", "Model Coordination", "4D Scheduling"])
    
    with tabs[0]:
        st.subheader("🎯 3D Model Viewer")
        st.info("3D BIM viewer would be integrated here with actual model files")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="enterprise-card">
                <h4>Model Information</h4>
                <p><strong>Model:</strong> Highland Tower Development</p>
                <p><strong>Version:</strong> v2.3.1</p>
                <p><strong>Last Updated:</strong> 2024-05-23</p>
                <p><strong>File Size:</strong> 245 MB</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="enterprise-card">
                <h4>Model Stats</h4>
                <p><strong>Elements:</strong> 125,847</p>
                <p><strong>Families:</strong> 2,431</p>
                <p><strong>Levels:</strong> 17</p>
                <p><strong>Phases:</strong> 4</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.subheader("⚠️ Clash Detection")
        clash_data = pd.DataFrame({
            'Clash ID': ['CLASH-001', 'CLASH-002', 'CLASH-003', 'CLASH-004'],
            'Type': ['Hard Clash', 'Soft Clash', 'Hard Clash', 'Clearance'],
            'Disciplines': ['Structure/MEP', 'MEP/Arch', 'MEP/MEP', 'Structure/Arch'],
            'Level': ['Level 3', 'Level 5', 'Level 7', 'Level 2'],
            'Status': ['Resolved', 'Open', 'In Review', 'Resolved'],
            'Priority': ['High', 'Medium', 'High', 'Low']
        })
        st.dataframe(clash_data, use_container_width=True)
    
    with tabs[2]:
        st.subheader("🔄 Model Coordination")
        coord_data = pd.DataFrame({
            'Discipline': ['Architecture', 'Structural', 'MEP', 'Civil'],
            'Last Update': ['2024-05-23', '2024-05-22', '2024-05-23', '2024-05-20'],
            'Version': ['v2.3.1', 'v2.3.0', 'v2.3.1', 'v2.2.8'],
            'Status': ['Current', 'Update Pending', 'Current', 'Update Pending'],
            'Coordinator': ['Arch Team', 'Structural Eng', 'MEP Eng', 'Civil Eng']
        })
        st.dataframe(coord_data, use_container_width=True)
    
    with tabs[3]:
        st.subheader("📅 4D Scheduling")
        st.info("4D scheduling visualization linking BIM model to project timeline")
        schedule_phases = pd.DataFrame({
            'Phase': ['Foundation', 'Structure L1-5', 'Structure L6-10', 'Structure L11-15', 'MEP Rough-in'],
            'Start Date': ['2024-02-15', '2024-04-01', '2024-06-01', '2024-08-01', '2024-08-15'],
            'Duration': ['6 weeks', '8 weeks', '8 weeks', '8 weeks', '12 weeks'],
            'Status': ['Complete', 'In Progress', 'Scheduled', 'Scheduled', 'Scheduled'],
            'Model Elements': ['Foundation', 'Floors 1-5', 'Floors 6-10', 'Floors 11-15', 'MEP Systems']
        })
        st.dataframe(schedule_phases, use_container_width=True)

# Additional modules with similar structure
def render_contracts():
    st.title("📋 Contract Management")
    st.info("Contract management features - subcontractor agreements, change orders, payment applications")

def render_closeout():
    st.title("✅ Project Closeout")
    st.info("Closeout documentation, punch lists, warranties, and final inspections")

def render_analytics():
    st.title("📈 Analytics & Reporting")
    st.info("Advanced analytics, KPI dashboards, and custom reporting")

def render_documents():
    st.title("📁 Document Management")
    st.info("Centralized document storage, version control, and collaboration")

def render_settings():
    st.title("⚙️ Settings")
    st.info("User preferences, system configuration, and administration")

# Main content router
def render_main_content():
    current_menu = st.session_state.current_menu
    
    module_map = {
        "Dashboard": render_dashboard,
        "PreConstruction": render_preconstruction,
        "Engineering": render_engineering,
        "Field Operations": render_field_operations,
        "Safety": render_safety,
        "Contracts": render_contracts,
        "Cost Management": render_cost_management,
        "BIM": render_bim,
        "Closeout": render_closeout,
        "Analytics": render_analytics,
        "Documents": render_documents,
        "Settings": render_settings
    }
    
    if current_menu in module_map:
        module_map[current_menu]()
    else:
        st.error(f"Module {current_menu} not found")

# Main application
def main():
    initialize_session_state()
    apply_enterprise_theme()
    
    if not st.session_state.authenticated:
        render_login()
    else:
        render_sidebar()
        render_main_content()

if __name__ == "__main__":
    main()