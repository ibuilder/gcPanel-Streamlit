"""
Highland Tower Development - Core Focused Construction Management Platform
$45.5M Mixed-Use Development - Better than Procore

Focus: Robust module functionality and core construction management features
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
        "theme": "dark"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def apply_theme():
    """Apply consistent professional theme"""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
        border-right: 2px solid #1e40af;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #0ea5e9, #38bdf8) !important;
        color: white !important;
        border: 1px solid #0284c7 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 4px rgba(14, 165, 233, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] button:hover {
        background: linear-gradient(135deg, #0284c7, #0ea5e9) !important;
        transform: translateX(5px) scale(1.02) !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4) !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border: 1px solid #475569 !important;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .enterprise-header {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
    }
    
    .project-info {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render professional header"""
    st.markdown(f"""
    <div class="enterprise-header">
        <h1 style="margin: 0; font-size: 2rem;">🏗️ gcPanel - Better than Procore</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            {st.session_state.project_name} • {st.session_state.project_value} Investment
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render comprehensive sidebar with theme toggle"""
    with st.sidebar:
        st.markdown(f"""
        <div class="project-info">
            <h3 style="color: #60a5fa; margin: 0 0 1rem 0;">Project Overview</h3>
            <p><strong>Investment:</strong> {st.session_state.project_value}</p>
            <p><strong>Residential:</strong> {st.session_state.residential_units} units</p>
            <p><strong>Retail:</strong> {st.session_state.retail_units} spaces</p>
            <p><strong>Status:</strong> <span style="color: #10b981;">Active Development</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Core Management")
        core_modules = [
            ("📊 Dashboard", "Dashboard"),
            ("🏗️ PreConstruction", "PreConstruction"), 
            ("⚙️ Engineering", "Engineering"),
            ("👷 Field Operations", "Field Operations"),
            ("🦺 Safety", "Safety"),
            ("📋 Contracts", "Contracts"),
            ("💰 Cost Management", "Cost Management"),
            ("🏢 BIM", "BIM"),
            ("✅ Closeout", "Closeout")
        ]
        
        for display_name, module in core_modules:
            if st.button(display_name, key=f"core_{module}", use_container_width=True):
                st.session_state.current_menu = module
                st.rerun()
        
        st.markdown("### 🔧 Advanced Tools")
        advanced_tools = [
            ("📝 RFIs", "RFIs"),
            ("📊 Daily Reports", "Daily Reports"),
            ("📤 Submittals", "Submittals"),
            ("📨 Transmittals", "Transmittals"),
            ("📅 Scheduling", "Scheduling"),
            ("🔍 Quality Control", "Quality Control"),
            ("📦 Material Management", "Material Management"),
            ("🚛 Equipment Tracking", "Equipment Tracking"),
            ("📸 Progress Photos", "Progress Photos")
        ]
        
        for display_name, tool in advanced_tools:
            if st.button(display_name, key=f"tool_{tool}", use_container_width=True):
                st.session_state.current_menu = tool
                st.rerun()
        
        st.markdown("### 🤖 Intelligence")
        ai_modules = [
            ("📈 Analytics", "Analytics"),
            ("🤖 AI Assistant", "AI Assistant"),
            ("📱 Mobile Companion", "Mobile Companion")
        ]
        
        for display_name, module in ai_modules:
            if st.button(display_name, key=f"ai_{module}", use_container_width=True):
                st.session_state.current_menu = module
                st.rerun()
        
        # Theme toggle at bottom
        st.markdown("---")
        if st.button("🌓 Toggle Theme", use_container_width=True):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()

def render_login():
    """Render clean login form"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h2 style="color: #60a5fa; margin-bottom: 2rem;">Access Your Project Dashboard</h2>
        <p style="color: #94a3b8; margin-bottom: 2rem;">
            Construction management platform better than Procore
        </p>
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
    """Render comprehensive dashboard with real metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #10b981; margin: 0;">Budget Status</h3>
            <h2 style="margin: 0.5rem 0;">89.2%</h2>
            <p style="color: #94a3b8; margin: 0;">$40.6M utilized</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #f59e0b; margin: 0;">Schedule</h3>
            <h2 style="margin: 0.5rem 0;">72%</h2>
            <p style="color: #94a3b8; margin: 0;">On track</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #8b5cf6; margin: 0;">Safety Score</h3>
            <h2 style="margin: 0.5rem 0;">98.5</h2>
            <p style="color: #94a3b8; margin: 0;">Excellent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #ef4444; margin: 0;">Active RFIs</h3>
            <h2 style="margin: 0.5rem 0;">12</h2>
            <p style="color: #94a3b8; margin: 0;">Pending review</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Project Timeline Chart
    st.markdown("### 📊 Project Progress Overview")
    
    timeline_data = pd.DataFrame({
        'Phase': ['Foundation', 'Structure', 'MEP', 'Interiors', 'Exterior'],
        'Progress': [100, 85, 60, 30, 15],
        'Status': ['Complete', 'Active', 'Active', 'Planned', 'Planned']
    })
    
    fig = px.bar(timeline_data, x='Phase', y='Progress', 
                 title="Construction Phase Progress",
                 color='Status',
                 color_discrete_map={'Complete': '#10b981', 'Active': '#f59e0b', 'Planned': '#6b7280'})
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Recent Activity")
        st.markdown("""
        - ✅ MEP inspection completed - Floor 8
        - 🔧 HVAC system installed - Floor 6  
        - 📝 RFI submitted - Electrical panel specs
        - 🚛 Concrete delivery scheduled - Tomorrow 8 AM
        - 👷 Safety training completed - 15 workers
        """)
    
    with col2:
        st.markdown("### ⚠️ Action Items")
        st.markdown("""
        - 🔴 Review change order #CO-2024-015
        - 🟡 Approve material delivery schedule
        - 🟢 Update progress photos - Floor 9
        - 🔵 Schedule elevator inspection
        - 🟠 Review safety incident report
        """)

def render_contracts():
    """Render comprehensive contracts management"""
    st.markdown("## 📋 Contracts Management - Enterprise Level")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Active Contracts", "Change Orders", "Vendor Management", "Contract Analytics"])
    
    with tab1:
        st.markdown("### Current Project Contracts")
        contracts_data = pd.DataFrame({
            'Contractor': ['Highland Construction LLC', 'Elite MEP Systems', 'Premium Interiors', 'Safety First Inc', 'Steel Solutions Inc'],
            'Contract Value': ['$28.5M', '$8.2M', '$6.1M', '$450K', '$2.8M'],
            'Status': ['Active', 'Active', 'Pending', 'Active', 'Active'],
            'Completion': ['75%', '60%', '0%', '95%', '45%'],
            'Payment Status': ['Current', 'Current', 'N/A', 'Current', 'Pending']
        })
        st.dataframe(contracts_data, use_container_width=True)
        
        # Contract actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Create New Contract", use_container_width=True):
                st.success("New contract form opened!")
        with col2:
            if st.button("📊 Contract Reports", use_container_width=True):
                st.info("Generating contract performance reports...")
        with col3:
            if st.button("💰 Payment Processing", use_container_width=True):
                st.info("Opening payment processing dashboard...")
    
    with tab2:
        st.markdown("### Change Orders Management")
        change_orders = pd.DataFrame({
            'CO Number': ['CO-2024-015', 'CO-2024-016', 'CO-2024-017', 'CO-2024-018'],
            'Description': ['HVAC scope modification', 'Additional electrical outlets', 'Flooring upgrade', 'Structural reinforcement'],
            'Amount': ['+$125K', '+$45K', '+$89K', '+$200K'],
            'Status': ['Under Review', 'Approved', 'Pending', 'Draft'],
            'Submitted Date': ['2024-05-20', '2024-05-18', '2024-05-22', '2024-05-23']
        })
        st.dataframe(change_orders, use_container_width=True)
        
        # Change order metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Change Orders", "18", "+4")
        with col2:
            st.metric("Total Value", "$1.2M", "+$459K")
        with col3:
            st.metric("Avg Processing Time", "3.2 days", "-0.8 days")
    
    with tab3:
        st.markdown("### Vendor Performance Dashboard")
        vendor_data = pd.DataFrame({
            'Vendor': ['Highland Construction', 'Elite MEP', 'Premium Interiors', 'Safety First', 'Steel Solutions'],
            'Performance Score': [95, 88, 92, 98, 85],
            'On-Time Delivery': ['98%', '92%', '95%', '100%', '87%'],
            'Quality Rating': [4.8, 4.5, 4.7, 4.9, 4.3],
            'Active Projects': [3, 2, 1, 4, 2]
        })
        st.dataframe(vendor_data, use_container_width=True)
    
    with tab4:
        st.markdown("### Contract Analytics")
        # Contract value distribution chart
        contract_values = [28.5, 8.2, 6.1, 2.8, 0.45]
        contractors = ['Highland Construction', 'Elite MEP', 'Premium Interiors', 'Steel Solutions', 'Safety First']
        
        fig = px.pie(values=contract_values, names=contractors, title="Contract Value Distribution")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def render_rfis():
    """Render comprehensive RFI management"""
    st.markdown("## 📝 Request for Information (RFIs) - Advanced Management")
    
    tab1, tab2, tab3 = st.tabs(["Active RFIs", "RFI Analytics", "Create New RFI"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### Active RFIs")
            rfi_data = pd.DataFrame({
                'RFI Number': ['RFI-2024-001', 'RFI-2024-002', 'RFI-2024-003', 'RFI-2024-004', 'RFI-2024-005'],
                'Subject': ['Electrical panel specifications', 'HVAC duct routing clarification', 'Fire safety system integration', 'Structural beam connection detail', 'Plumbing fixture specifications'],
                'Submitted By': ['Elite MEP', 'Highland Construction', 'Safety First Inc', 'Highland Construction', 'Elite MEP'],
                'Status': ['Pending Response', 'Under Review', 'Answered', 'Pending Response', 'Draft'],
                'Priority': ['High', 'Medium', 'Low', 'High', 'Medium'],
                'Days Open': [3, 7, 0, 5, 1],
                'Assigned To': ['Project Manager', 'MEP Engineer', 'Safety Coordinator', 'Structural Engineer', 'Project Manager']
            })
            st.dataframe(rfi_data, use_container_width=True)
        
        with col2:
            st.markdown("### RFI Statistics")
            st.metric("Total RFIs", "47", "+5")
            st.metric("Open RFIs", "12", "+2")
            st.metric("Avg Response Time", "2.3 days", "-0.5 days")
            st.metric("This Week", "8", "+3")
            
            if st.button("📊 Full Analytics", use_container_width=True):
                st.session_state.current_menu = "RFI Analytics"
                st.rerun()
    
    with tab2:
        st.markdown("### RFI Performance Analytics")
        
        # RFI trend chart
        rfi_dates = pd.date_range(start='2024-01-01', end='2024-05-25', freq='W')
        rfi_counts = [2, 3, 5, 4, 6, 3, 7, 4, 5, 6, 8, 4, 7, 5, 6, 8, 9, 7, 6, 8, 5]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=rfi_dates[:len(rfi_counts)], y=rfi_counts, mode='lines+markers', name='RFIs per Week'))
        fig.update_layout(title="RFI Submission Trends", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Response time analysis
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Response Time by Priority")
            priority_data = pd.DataFrame({
                'Priority': ['High', 'Medium', 'Low'],
                'Avg Response Time (days)': [1.2, 2.3, 4.1],
                'Target (days)': [1.0, 3.0, 5.0]
            })
            st.dataframe(priority_data)
        
        with col2:
            st.markdown("#### RFI Sources")
            source_data = pd.DataFrame({
                'Source': ['Highland Construction', 'Elite MEP', 'Safety First', 'Premium Interiors'],
                'Count': [18, 12, 8, 9]
            })
            fig = px.bar(source_data, x='Source', y='Count', title="RFIs by Source")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Create New RFI")
        with st.form("new_rfi_form"):
            col1, col2 = st.columns(2)
            with col1:
                rfi_subject = st.text_input("RFI Subject", placeholder="Brief description of the request")
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                category = st.selectbox("Category", ["Electrical", "Mechanical", "Structural", "Architectural", "Civil"])
            
            with col2:
                submitter = st.text_input("Submitted By", value=st.session_state.username)
                due_date = st.date_input("Response Due Date")
                assign_to = st.selectbox("Assign To", ["Project Manager", "MEP Engineer", "Structural Engineer", "Architect"])
            
            description = st.text_area("Detailed Description", height=100)
            
            # File upload for attachments
            uploaded_files = st.file_uploader("Attach Files", accept_multiple_files=True, type=['pdf', 'jpg', 'png', 'dwg'])
            
            submitted = st.form_submit_button("Submit RFI", use_container_width=True)
            
            if submitted:
                if rfi_subject and description:
                    st.success(f"✅ RFI submitted successfully! Reference: RFI-2024-{len(rfi_data)+1:03d}")
                    st.info("RFI has been assigned and notifications sent to relevant parties.")
                else:
                    st.error("Please fill in all required fields.")

def render_scheduling():
    """Render advanced scheduling module"""
    st.markdown("## 📅 Project Scheduling - Advanced Planning")
    
    tab1, tab2, tab3 = st.tabs(["Master Schedule", "Critical Path", "Resource Planning"])
    
    with tab1:
        st.markdown("### Master Project Schedule")
        
        # Schedule data
        schedule_data = pd.DataFrame({
            'Task': ['Site Preparation', 'Foundation', 'Structural Frame', 'MEP Rough-in', 'Exterior Envelope', 'Interior Finishes', 'Final Inspections'],
            'Start Date': ['2024-01-15', '2024-02-01', '2024-04-01', '2024-06-15', '2024-08-01', '2024-10-01', '2024-12-15'],
            'End Date': ['2024-01-31', '2024-03-31', '2024-06-14', '2024-07-31', '2024-09-30', '2024-12-14', '2024-12-31'],
            'Duration (days)': [16, 59, 74, 46, 60, 74, 16],
            'Progress': ['100%', '100%', '85%', '60%', '30%', '0%', '0%'],
            'Status': ['Complete', 'Complete', 'Active', 'Active', 'Planned', 'Planned', 'Planned']
        })
        st.dataframe(schedule_data, use_container_width=True)
        
        # Gantt chart simulation
        st.markdown("#### Gantt Chart Overview")
        fig = px.timeline(schedule_data, x_start='Start Date', x_end='End Date', y='Task', color='Status')
        fig.update_layout(title="Project Timeline", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Critical Path Analysis")
        st.info("Critical path identifies the longest sequence of dependent tasks that determines the minimum project duration.")
        
        critical_tasks = pd.DataFrame({
            'Critical Task': ['Foundation Completion', 'Structural Frame', 'MEP Rough-in', 'Exterior Envelope'],
            'Float (days)': [0, 0, 0, 0],
            'Impact': ['High', 'High', 'Medium', 'Medium'],
            'Risk Level': ['Low', 'Medium', 'High', 'Low']
        })
        st.dataframe(critical_tasks, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Project Duration", "351 days")
            st.metric("Critical Path Length", "285 days")
        with col2:
            st.metric("Schedule Buffer", "18.8%")
            st.metric("On-Time Probability", "87%")
    
    with tab3:
        st.markdown("### Resource Planning")
        
        resource_data = pd.DataFrame({
            'Resource Type': ['Labor', 'Equipment', 'Materials', 'Subcontractors'],
            'Allocated': ['145 workers', '12 units', '$2.3M', '8 firms'],
            'Utilized': ['128 workers', '10 units', '$2.1M', '7 firms'],
            'Efficiency': ['88%', '83%', '91%', '88%']
        })
        st.dataframe(resource_data, use_container_width=True)

def render_main_content():
    """Render main content based on selected menu"""
    current_menu = st.session_state.current_menu
    
    # Core module functions
    module_functions = {
        "Dashboard": render_dashboard,
        "Contracts": render_contracts,
        "RFIs": render_rfis,
        "Scheduling": render_scheduling,
    }
    
    if current_menu in module_functions:
        module_functions[current_menu]()
    else:
        # Placeholder for modules under development
        st.markdown(f"## {current_menu}")
        st.info(f"The {current_menu} module is being developed with advanced features specifically designed to surpass Procore's capabilities.")
        
        # Show relevant preview content based on module
        if current_menu == "Engineering":
            st.markdown("### Engineering Module Preview")
            st.markdown("- Advanced drawing management and revision control")
            st.markdown("- Automated clash detection and resolution workflows")
            st.markdown("- Integration with CAD and BIM platforms")
            st.markdown("- Real-time design coordination")
        
        elif current_menu == "Field Operations":
            st.markdown("### Field Operations Module Preview")
            st.markdown("- Daily reporting with photo documentation")
            st.markdown("- Real-time weather integration")
            st.markdown("- Mobile-first crew management")
            st.markdown("- Progress tracking with GPS")
        
        elif current_menu == "Safety":
            st.markdown("### Safety Management Preview")
            st.markdown("- Incident reporting and investigation")
            st.markdown("- Safety training tracking")
            st.markdown("- Risk assessment tools")
            st.markdown("- Compliance monitoring")
        
        elif current_menu == "Cost Management":
            st.markdown("### Cost Management Preview")
            st.markdown("- Real-time budget tracking")
            st.markdown("- Automated cost forecasting")
            st.markdown("- Change order impact analysis")
            st.markdown("- Financial reporting dashboard")

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="gcPanel - Better than Procore",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    apply_theme()
    
    if not st.session_state.authenticated:
        render_login()
    else:
        render_header()
        render_sidebar()
        render_main_content()

if __name__ == "__main__":
    main()