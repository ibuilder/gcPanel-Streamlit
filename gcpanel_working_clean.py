"""
Highland Tower Development - Professional Construction Management Platform
$45.5M Mixed-Use Development - 120 Residential + 8 Retail Units

Enterprise-grade construction management with comprehensive modules
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def initialize_session_state():
    """Initialize session state with default values."""
    defaults = {
        "authenticated": False,
        "username": "",
        "current_menu": "Dashboard",
        "project_name": "Highland Tower Development",
        "project_value": "$45.5M",
        "residential_units": 120,
        "retail_units": 8,
        "theme": "dark"  # Default to dark theme
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def apply_theme():
    """Apply theme based on user selection - dark as default"""
    theme = st.session_state.get("theme", "dark")
    
    if theme == "dark":
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f1f5f9;
        }
        
        /* Dark Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
            border-right: 2px solid #1e40af;
        }
        
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        
        section[data-testid="stSidebar"] button {
            background: rgba(30, 64, 175, 0.2) !important;
            color: white !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        section[data-testid="stSidebar"] button:hover {
            background: rgba(59, 130, 246, 0.4) !important;
            transform: translateX(5px) !important;
        }
        
        /* Main content cards */
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
            border: 1px solid #475569 !important;
        }
        
        .enterprise-header {
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        }
        
        .project-info {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-left: 4px solid #3b82f6;
        }
        </style>
        """, unsafe_allow_html=True)
    
    else:  # light theme
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            color: #1e293b;
        }
        
        /* Light Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%) !important;
            border-right: 2px solid #cbd5e1;
        }
        
        section[data-testid="stSidebar"] * {
            color: #1e293b !important;
        }
        
        section[data-testid="stSidebar"] button {
            background: rgba(59, 130, 246, 0.1) !important;
            color: #1e40af !important;
            border: 1px solid rgba(59, 130, 246, 0.2) !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        section[data-testid="stSidebar"] button:hover {
            background: rgba(59, 130, 246, 0.2) !important;
            transform: translateX(5px) !important;
        }
        
        /* Main content cards */
        .metric-card {
            background: white !important;
            border: 1px solid #e2e8f0 !important;
        }
        
        .enterprise-header {
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        }
        
        .project-info {
            background: white;
            border-left: 4px solid #3b82f6;
        }
        </style>
        """, unsafe_allow_html=True)
    
    .enterprise-header {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
    }
    
    .project-info {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    }
    
    .nav-button {
        width: 100%;
        margin-bottom: 0.5rem;
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        background: white;
        text-align: left;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .nav-button:hover {
        background: #f1f5f9;
        border-color: #3b82f6;
    }
    
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def render_enterprise_header():
    """Render professional header with project information"""
    st.markdown(f"""
    <div class="enterprise-header">
        <h1 style="margin: 0; font-size: 2rem;">🏗️ gcPanel Construction Management</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            {st.session_state.project_name} • {st.session_state.project_value} Investment
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render comprehensive sidebar navigation"""
    with st.sidebar:
        st.markdown(f"""
        <div class="project-info">
            <h3 style="color: #1e40af; margin: 0 0 1rem 0;">Project Overview</h3>
            <p><strong>Investment:</strong> {st.session_state.project_value}</p>
            <p><strong>Residential:</strong> {st.session_state.residential_units} units</p>
            <p><strong>Retail:</strong> {st.session_state.retail_units} spaces</p>
            <p><strong>Status:</strong> <span style="color: #059669;">Active Development</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Core Management")
        core_modules = [
            "Dashboard", "PreConstruction", "Engineering", "Field Operations",
            "Safety", "Contracts", "Cost Management", "BIM", "Closeout"
        ]
        
        for module in core_modules:
            if st.button(f"📋 {module}", key=f"core_{module}", use_container_width=True):
                st.session_state.current_menu = module
        
        st.markdown("### 🔧 Advanced Tools")
        advanced_tools = [
            "RFIs", "Daily Reports", "Submittals", "Transmittals",
            "Scheduling", "Quality Control", "Material Management",
            "Equipment Tracking", "Progress Photos"
        ]
        
        for tool in advanced_tools:
            if st.button(f"⚡ {tool}", key=f"tool_{tool}", use_container_width=True):
                st.session_state.current_menu = tool
        
        st.markdown("### 🤖 Intelligence")
        ai_modules = ["Analytics", "AI Assistant", "Mobile Companion"]
        
        for module in ai_modules:
            if st.button(f"🧠 {module}", key=f"ai_{module}", use_container_width=True):
                st.session_state.current_menu = module

def render_login():
    """Render clean login form"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <div class="login-container">
            <h2 style="color: #1e40af; margin-bottom: 2rem;">Access Your Project Dashboard</h2>
            <p style="color: #64748b; margin-bottom: 2rem;">
                Manage your construction project with enterprise-grade tools
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submitted = st.form_submit_button("Access Dashboard", use_container_width=True)
            
            if submitted and username and password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()

def render_dashboard():
    """Render comprehensive dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #059669; margin: 0;">Budget Status</h3>
            <h2 style="margin: 0.5rem 0;">89.2%</h2>
            <p style="color: #64748b; margin: 0;">$40.6M utilized</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #dc2626; margin: 0;">Schedule</h3>
            <h2 style="margin: 0.5rem 0;">72%</h2>
            <p style="color: #64748b; margin: 0;">On track</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #7c3aed; margin: 0;">Safety Score</h3>
            <h2 style="margin: 0.5rem 0;">98.5</h2>
            <p style="color: #64748b; margin: 0;">Excellent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #ea580c; margin: 0;">Active RFIs</h3>
            <h2 style="margin: 0.5rem 0;">12</h2>
            <p style="color: #64748b; margin: 0;">Pending review</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Project Timeline Chart
    st.markdown("### 📊 Project Timeline & Progress")
    
    # Sample timeline data
    timeline_data = pd.DataFrame({
        'Phase': ['Foundation', 'Structure', 'MEP', 'Interiors', 'Exterior'],
        'Progress': [100, 85, 60, 30, 15],
        'Status': ['Complete', 'Active', 'Active', 'Planned', 'Planned']
    })
    
    fig = px.bar(timeline_data, x='Phase', y='Progress', 
                 title="Construction Phase Progress",
                 color='Status',
                 color_discrete_map={'Complete': '#059669', 'Active': '#dc2626', 'Planned': '#64748b'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent Activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Recent Activity")
        activities = [
            "✅ MEP inspection completed - Floor 8",
            "🔧 HVAC system installed - Floor 6",
            "📝 RFI submitted - Electrical panel specs",
            "🚛 Concrete delivery scheduled - Tomorrow 8 AM",
            "👷 Safety training completed - 15 workers"
        ]
        
        for activity in activities:
            st.markdown(f"<p style='margin: 0.5rem 0;'>{activity}</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⚠️ Action Items")
        action_items = [
            "🔴 Review change order #CO-2024-015",
            "🟡 Approve material delivery schedule",
            "🟢 Update progress photos - Floor 9",
            "🔵 Schedule elevator inspection",
            "🟠 Review safety incident report"
        ]
        
        for item in action_items:
            st.markdown(f"<p style='margin: 0.5rem 0;'>{item}</p>", unsafe_allow_html=True)

def render_contracts():
    """Render contracts management module"""
    st.markdown("## 📋 Contracts Management")
    
    tab1, tab2, tab3 = st.tabs(["Active Contracts", "Change Orders", "Vendor Management"])
    
    with tab1:
        st.markdown("### Current Project Contracts")
        contracts_data = pd.DataFrame({
            'Contractor': ['Highland Construction LLC', 'Elite MEP Systems', 'Premium Interiors', 'Safety First Inc'],
            'Contract Value': ['$28.5M', '$8.2M', '$6.1M', '$450K'],
            'Status': ['Active', 'Active', 'Pending', 'Active'],
            'Completion': ['75%', '60%', '0%', '95%']
        })
        st.dataframe(contracts_data, use_container_width=True)
    
    with tab2:
        st.markdown("### Change Orders")
        change_orders = pd.DataFrame({
            'CO Number': ['CO-2024-015', 'CO-2024-016', 'CO-2024-017'],
            'Description': ['HVAC scope modification', 'Additional electrical outlets', 'Flooring upgrade'],
            'Amount': ['+$125K', '+$45K', '+$89K'],
            'Status': ['Under Review', 'Approved', 'Pending']
        })
        st.dataframe(change_orders, use_container_width=True)
    
    with tab3:
        st.markdown("### Vendor Performance")
        st.info("Track vendor performance, delivery schedules, and quality metrics")

def render_engineering():
    """Render engineering module"""
    st.markdown("## 🔧 Engineering & Technical")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 RFIs (Request for Information)")
        rfi_data = pd.DataFrame({
            'RFI #': ['RFI-001', 'RFI-002', 'RFI-003'],
            'Subject': ['Electrical panel specs', 'HVAC duct routing', 'Fire safety system'],
            'Status': ['Pending', 'Answered', 'Under Review'],
            'Days Open': [3, 0, 7]
        })
        st.dataframe(rfi_data, use_container_width=True)
    
    with col2:
        st.markdown("### 📤 Submittals")
        submittals_data = pd.DataFrame({
            'Submittal': ['Concrete Mix Design', 'Steel Specifications', 'Window Samples'],
            'Status': ['Approved', 'Under Review', 'Resubmit Required'],
            'Due Date': ['Completed', '2024-05-30', '2024-06-05']
        })
        st.dataframe(submittals_data, use_container_width=True)

def render_safety():
    """Render safety management module"""
    st.markdown("## 🦺 Safety Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Days Without Incident", "127", "🟢")
    
    with col2:
        st.metric("Safety Score", "98.5/100", "+2.1")
    
    with col3:
        st.metric("Active Workers", "245", "+12")
    
    st.markdown("### Recent Safety Updates")
    safety_updates = [
        "✅ Weekly safety training completed - 45 attendees",
        "🦺 New PPE distributed to all workers",
        "📋 Safety inspection passed - No violations",
        "🚨 Emergency drill conducted successfully"
    ]
    
    for update in safety_updates:
        st.markdown(f"- {update}")

def render_rfis():
    """Render RFIs module"""
    st.markdown("## 📝 Request for Information (RFIs)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Active RFIs")
        rfi_detailed = pd.DataFrame({
            'RFI Number': ['RFI-2024-001', 'RFI-2024-002', 'RFI-2024-003', 'RFI-2024-004'],
            'Subject': ['Electrical panel specifications', 'HVAC duct routing clarification', 'Fire safety system integration', 'Structural beam connection detail'],
            'Submitted By': ['Elite MEP', 'Highland Construction', 'Safety First Inc', 'Highland Construction'],
            'Status': ['Pending Response', 'Under Review', 'Answered', 'Pending Response'],
            'Priority': ['High', 'Medium', 'Low', 'High'],
            'Days Open': [3, 7, 0, 5]
        })
        st.dataframe(rfi_detailed, use_container_width=True)
    
    with col2:
        st.markdown("### Quick Actions")
        if st.button("📝 Create New RFI", use_container_width=True):
            st.success("RFI form opened!")
        
        if st.button("📊 RFI Analytics", use_container_width=True):
            st.info("Analytics dashboard loading...")
        
        st.markdown("### RFI Statistics")
        st.metric("Total RFIs", "47")
        st.metric("Avg Response Time", "2.3 days")
        st.metric("Open RFIs", "12")

def render_main_content():
    """Render main content based on selected menu"""
    current_menu = st.session_state.current_menu
    
    # Module mapping for clean navigation
    modules = {
        "Dashboard": render_dashboard,
        "Contracts": render_contracts,
        "Engineering": render_engineering,
        "Safety": render_safety,
        "RFIs": render_rfis,
    }
    
    if current_menu in modules:
        modules[current_menu]()
    else:
        # Default content for modules not yet implemented
        st.markdown(f"## {current_menu}")
        st.info(f"The {current_menu} module is being developed. Coming soon with advanced features!")
        
        # Show some sample content based on module type
        if current_menu in ["Field Operations", "Daily Reports"]:
            st.markdown("### Daily Operations Overview")
            st.markdown("- Weather conditions and work progress")
            st.markdown("- Crew attendance and productivity")
            st.markdown("- Material deliveries and equipment status")
        
        elif current_menu in ["Cost Management", "Analytics"]:
            st.markdown("### Financial Analytics")
            st.markdown("- Budget tracking and forecasting")
            st.markdown("- Cost variance analysis")
            st.markdown("- ROI and profitability metrics")
        
        elif current_menu == "BIM":
            st.markdown("### Building Information Modeling")
            st.markdown("- 3D model visualization")
            st.markdown("- Clash detection and resolution")
            st.markdown("- Model coordination workflows")

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="gcPanel - Highland Tower Development",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    apply_professional_theme()
    
    if not st.session_state.authenticated:
        render_login()
    else:
        render_enterprise_header()
        render_sidebar()
        render_main_content()

if __name__ == "__main__":
    main()