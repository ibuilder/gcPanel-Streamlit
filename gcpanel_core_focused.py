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
    """Enterprise dashboard with advanced analytics and real-time insights"""
    st.title("🏗️ Highland Tower Development - Executive Dashboard")
    st.markdown("**$45.5M Mixed-Use Development** | 120 Residential + 8 Retail Units | 15 Stories")
    
    # Real-time KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Project Progress", "67.3%", "2.1% this week", help="Overall completion vs baseline schedule")
    with col2:
        st.metric("Budget Performance", "$30.5M", "-$2.1M under", help="Spent vs $45.5M total budget")
    with col3:
        st.metric("Schedule Variance", "5 Days", "Ahead of schedule", help="Current vs planned timeline")
    with col4:
        st.metric("Safety Rating", "98.5%", "+0.5% improvement", help="OSHA compliance score")
    with col5:
        st.metric("Quality Score", "96.2%", "+1.2% this month", help="QC inspections passed")
    
    # Advanced Analytics Tabs
    st.markdown("### 📊 Advanced Project Analytics")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Progress", "💰 Financials", "👷 Resources", "🎯 Critical Path", "⚠️ Risk Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            # Progress visualization
            progress_data = pd.DataFrame({
                'Floor': [f'Level {i}' for i in range(1, 16)],
                'Structural': [100 if i <= 12 else 85 if i == 13 else 30 if i == 14 else 0 for i in range(1, 16)],
                'MEP': [100 if i <= 9 else 70 if i <= 11 else 20 if i <= 13 else 0 for i in range(1, 16)],
                'Finishes': [100 if i <= 6 else 40 if i <= 8 else 10 if i <= 10 else 0 for i in range(1, 16)]
            })
            
            fig = px.bar(progress_data, x='Floor', y=['Structural', 'MEP', 'Finishes'], 
                        title="Floor-by-Floor Progress", barmode='group')
            fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            **Current Phase Status:**
            
            🏗️ **Structural (Level 13)**
            - Steel erection: 85% complete
            - Concrete pour: Scheduled Friday
            - Inspection: Passed preliminary
            
            ⚡ **MEP Systems (Level 9-11)**
            - Electrical rough-in: 70% complete
            - Plumbing stack: 90% complete
            - HVAC ducts: 65% complete
            
            🎨 **Interior Finishes (Level 6-8)**
            - Drywall: 40% complete
            - Flooring prep: 25% complete
            - Paint prep: 15% complete
            """)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            # Financial breakdown
            financial_data = pd.DataFrame({
                'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Overhead'],
                'Budgeted': [18.2, 15.8, 6.3, 3.7, 1.5],
                'Actual': [17.8, 16.1, 5.9, 3.5, 1.4],
                'Forecasted': [17.9, 16.3, 6.0, 3.6, 1.5]
            })
            
            fig = px.bar(financial_data, x='Category', y=['Budgeted', 'Actual', 'Forecasted'],
                        title="Cost Performance by Category (Millions $)", barmode='group')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            **Financial Performance:**
            
            💰 **Total Budget:** $45.5M
            📊 **Spent to Date:** $30.5M (67%)
            📈 **Forecast at Completion:** $43.4M
            💚 **Projected Savings:** $2.1M (4.6%)
            
            **Cost Trends:**
            - Labor: 2% under budget (efficiency gains)
            - Materials: 3% over (steel price increase)
            - Equipment: 6% under (better utilization)
            
            **Change Orders:**
            - Approved: $890K (15 COs)
            - Pending: $340K (5 COs)
            - Rejected: $120K (3 COs)
            """)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Current Workforce:**
            - **Total Workers:** 89 active
            - **Prime Contractor:** 34 workers
            - **Subcontractors:** 55 workers (12 companies)
            - **Safety Officers:** 3 full-time
            - **QC Inspectors:** 2 full-time
            
            **Productivity Metrics:**
            - Average daily hours: 8.2
            - Overtime hours this week: 127
            - Efficiency rating: 94.2%
            - Worker satisfaction: 87%
            """)
        
        with col2:
            st.markdown("""
            **Resource Allocation:**
            
            **Level 13 (Current Focus):**
            - Ironworkers: 12
            - Concrete crew: 8
            - Crane operators: 2
            
            **Level 9-11 (MEP):**
            - Electricians: 15
            - Plumbers: 8
            - HVAC techs: 6
            
            **Level 6-8 (Finishes):**
            - Drywall crew: 10
            - Flooring team: 6
            - Painters: 4
            """)
    
    with tab4:
        st.markdown("""
        **Critical Path Analysis:**
        
        🚨 **Critical Activities (Next 30 Days):**
        1. **Level 13 Steel Erection** - 5 days remaining
        2. **Elevator Shaft Concrete** - Depends on #1
        3. **Level 9 MEP Inspection** - 3 days (parallel)
        4. **Curtain Wall Installation** - 10 days (Level 8-10)
        
        ⚡ **Schedule Acceleration Opportunities:**
        - Increase Level 13 crew by 25% → Save 2 days
        - Parallel MEP rough-in on Levels 12-13 → Save 5 days
        - Pre-fabricate bathroom pods → Save 8 days
        
        📊 **Float Analysis:**
        - Critical path float: 0 days
        - Near-critical activities: 12 (1-3 days float)
        - Weather contingency: 10 days built-in
        """)
    
    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **High Priority Risks:**
            
            🔴 **CRITICAL:**
            - Steel delivery delays (10% probability)
            - Weather impact on concrete (25% probability)
            
            🟡 **MEDIUM:**
            - Labor shortage (15% probability)
            - MEP coordination conflicts (20% probability)
            - Permit approval delays (10% probability)
            
            🟢 **LOW:**
            - Material price increases (5% probability)
            - Equipment breakdowns (8% probability)
            """)
        
        with col2:
            st.markdown("""
            **Risk Mitigation Status:**
            
            ✅ **Active Mitigations:**
            - Alternative steel suppliers identified
            - Weather monitoring system deployed
            - Cross-trained labor pool established
            - Weekly MEP coordination meetings
            
            📋 **Contingency Plans:**
            - $1.5M budget reserve (3.3%)
            - 15-day schedule buffer
            - Emergency equipment rental agreements
            - Fast-track permit expeditor on retainer
            """)
    
    # Quick Action Dashboard
    st.markdown("### ⚡ Executive Action Center")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("📝 New RFI", use_container_width=True):
            st.session_state.current_menu = "RFIs"
            st.rerun()
    
    with col2:
        if st.button("📊 Daily Report", use_container_width=True):
            st.session_state.current_menu = "Daily Reports"
            st.rerun()
    
    with col3:
        if st.button("🦺 Safety Alert", use_container_width=True):
            st.session_state.current_menu = "Safety"
            st.rerun()
    
    with col4:
        if st.button("💰 Cost Update", use_container_width=True):
            st.session_state.current_menu = "Cost Management"
            st.rerun()
    
    with col5:
        if st.button("📸 Photo Upload", use_container_width=True):
            st.session_state.current_menu = "Progress Photos"
            st.rerun()
    
    with col6:
        if st.button("📋 QC Inspection", use_container_width=True):
            st.session_state.current_menu = "Quality Control"
            st.rerun()
    
    # Live Activity Feed
    st.markdown("### 🔔 Live Project Feed")
    
    # Real-time activity simulation
    import datetime
    now = datetime.datetime.now()
    
    activities = [
        ("🚨", "HIGH", "RFI-2025-089: Structural beam connection detail needed for Level 13", "2 minutes ago"),
        ("✅", "SUCCESS", "Daily report completed: Zone C electrical rough-in inspection passed", "15 minutes ago"),
        ("💰", "WARNING", "Cost variance alert: Steel materials 3.2% over budget this week", "28 minutes ago"),
        ("📸", "INFO", "Progress photos uploaded: Level 12 interior framing completion", "45 minutes ago"),
        ("🎉", "SUCCESS", "Milestone achieved: Level 11 MEP rough-in 100% complete", "1 hour ago"),
        ("👷", "INFO", "Crew assignment: Team Delta moved to Level 14 preparation work", "2 hours ago"),
        ("🔍", "WARNING", "Quality checkpoint: Minor concrete finish touch-up needed Unit 1205", "3 hours ago"),
        ("📦", "INFO", "Material delivery confirmed: Curtain wall panels Level 8-10 arriving Thursday", "4 hours ago"),
        ("⚡", "INFO", "MEP coordination meeting completed: Electrical/plumbing conflicts resolved", "5 hours ago"),
        ("🚛", "SUCCESS", "Equipment delivery: Tower crane maintenance completed ahead of schedule", "6 hours ago")
    ]
    
    for icon, priority, message, time in activities:
        if priority == "HIGH":
            st.error(f"{icon} **{message}** - *{time}*")
        elif priority == "WARNING":
            st.warning(f"{icon} **{message}** - *{time}*")
        elif priority == "SUCCESS":
            st.success(f"{icon} **{message}** - *{time}*")
        else:
            st.info(f"{icon} **{message}** - *{time}*")

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
    
    # Complete module functions with advanced features
    module_functions = {
        "Dashboard": render_dashboard,
        "Contracts": render_contracts,
        "RFIs": render_rfis,
        "Scheduling": render_scheduling,
        "Engineering": render_engineering,
        "Field Operations": render_field_operations,
        "Safety": render_safety,
        "Cost Management": render_cost_management,
        "Daily Reports": render_daily_reports,
        "Progress Photos": render_progress_photos,
        "Quality Control": render_quality_control,
        "Material Management": render_material_management,
        "BIM": render_bim,
        "Analytics": render_analytics,
    }
    
    if current_menu in module_functions:
        module_functions[current_menu]()
    else:
        # Advanced preview for remaining modules
        st.markdown(f"## {current_menu}")
        st.info(f"The {current_menu} module is being developed with enterprise-grade features designed to outperform Procore.")
        
        if current_menu == "PreConstruction":
            st.markdown("### 🏗️ PreConstruction Module")
            st.markdown("**Complete pre-construction planning and coordination platform**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **📋 Planning Tools:**
                - Project scope definition
                - Constructability reviews
                - Value engineering analysis
                - Risk assessment matrix
                """)
            with col2:
                st.markdown("""
                **📊 Advanced Features:**
                - AI-powered schedule optimization
                - Cost estimation with market data
                - Permit tracking and coordination
                - Trade partner qualification
                """)
        
        elif current_menu == "Closeout":
            st.markdown("### ✅ Project Closeout Module")
            st.markdown("**Comprehensive project completion and handover management**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **📋 Closeout Tasks:**
                - Punch list management
                - Final inspections tracking
                - Warranty documentation
                - As-built drawing compilation
                """)
            with col2:
                st.markdown("""
                **🎯 Advanced Features:**
                - Automated compliance checking
                - Digital handover packages
                - Maintenance manual integration
                - Owner training coordination
                """)
        
        elif current_menu == "Submittals":
            st.markdown("### 📤 Submittals Management")
            st.markdown("**Complete submittal workflow with automated tracking**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **📋 Core Features:**
                - Submittal creation and routing
                - Review workflow management
                - Approval tracking
                - Revision control
                """)
            with col2:
                st.markdown("""
                **⚡ Smart Features:**
                - Auto-routing by specification
                - Review time analytics
                - Integration with procurement
                - Mobile approval capability
                """)
        
        else:
            st.markdown(f"### Advanced {current_menu} capabilities coming soon...")
            st.markdown("- Enterprise-grade functionality")
            st.markdown("- Real-time collaboration tools") 
            st.markdown("- Advanced analytics and reporting")
            st.markdown("- Mobile-first design")

def render_engineering():
    """Advanced Engineering module with comprehensive workflow management"""
    st.title("⚙️ Engineering Management - Advanced Coordination")
    st.markdown("**Complete engineering workflow from design through construction**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📐 Drawing Management", "🔧 Coordination", "📊 Analytics", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### 📐 Drawing Management & Revision Control")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            drawing_data = [
                {"Sheet": "A-101", "Title": "Level 1 Floor Plan", "Rev": "C", "Date": "2025-01-20", "Status": "Current"},
                {"Sheet": "S-201", "Title": "Level 13 Framing Plan", "Rev": "B", "Date": "2025-01-22", "Status": "Under Review"},
                {"Sheet": "M-301", "Title": "HVAC Level 9-11", "Rev": "A", "Date": "2025-01-18", "Status": "Current"},
                {"Sheet": "E-401", "Title": "Electrical Riser Diagram", "Rev": "D", "Date": "2025-01-21", "Status": "Superseded"}
            ]
            st.dataframe(pd.DataFrame(drawing_data), use_container_width=True)
        
        with col2:
            st.metric("Total Drawings", "247")
            st.metric("Current Revision", "Rev C")
            st.metric("Under Review", "12")
            st.metric("Coordination Issues", "3")
    
    with tab2:
        st.markdown("### 🔧 MEP Coordination Dashboard")
        st.warning("🚨 **Active Coordination Issues:** 3 conflicts require immediate attention")
        
        coordination_issues = [
            {"Issue": "HVAC duct conflicts with structural beam", "Location": "Level 11, Grid C3", "Priority": "High", "Assigned": "MEP Engineer"},
            {"Issue": "Electrical conduit routing needs adjustment", "Location": "Level 9, Corridor", "Priority": "Medium", "Assigned": "Electrical Engineer"},
            {"Issue": "Plumbing stack conflicts with architecture", "Location": "Level 12, Unit 1205", "Priority": "High", "Assigned": "Architect"}
        ]
        
        for issue in coordination_issues:
            with st.expander(f"⚠️ {issue['Issue']} - {issue['Priority']} Priority"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Location:** {issue['Location']}")
                with col2:
                    st.markdown(f"**Assigned To:** {issue['Assigned']}")
                with col3:
                    if st.button(f"Resolve Issue", key=f"resolve_{issue['Issue'][:10]}"):
                        st.success("Issue marked for resolution!")

def render_field_operations():
    """Advanced Field Operations with real-time crew and progress management"""
    st.title("👷 Field Operations - Live Project Management")
    st.markdown("**Real-time field coordination and workforce management**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Crew Management", "📊 Daily Reports", "🌤️ Weather Impact", "📱 Mobile Tools"])
    
    with tab1:
        st.markdown("### 👥 Active Crew Management")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Workers", "89", "+5 today")
        with col2:
            st.metric("Active Crews", "12", "All zones covered")
        with col3:
            st.metric("Safety Officers", "3", "On-site now")
        with col4:
            st.metric("Productivity", "94%", "+2% vs target")
        
        # Crew assignments by floor
        st.markdown("### 🏗️ Current Crew Assignments")
        
        crew_assignments = [
            {"Level": "Level 13", "Crew": "Structural Team A", "Activity": "Steel erection", "Count": 12, "Supervisor": "Mike Chen"},
            {"Level": "Level 11", "Crew": "MEP Team B", "Activity": "Electrical rough-in", "Count": 8, "Supervisor": "Sarah Johnson"},
            {"Level": "Level 9", "Crew": "MEP Team C", "Activity": "Plumbing installation", "Count": 6, "Supervisor": "Carlos Rodriguez"},
            {"Level": "Level 7", "Crew": "Finishing Team D", "Activity": "Drywall installation", "Count": 10, "Supervisor": "Jennifer Walsh"}
        ]
        
        for assignment in crew_assignments:
            with st.expander(f"👷 {assignment['Level']} - {assignment['Crew']} ({assignment['Count']} workers)"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Activity:** {assignment['Activity']}")
                    st.markdown(f"**Supervisor:** {assignment['Supervisor']}")
                with col2:
                    st.markdown(f"**Crew Size:** {assignment['Count']} workers")
                    st.markdown(f"**Status:** ✅ On Schedule")
                with col3:
                    if st.button(f"📞 Contact Supervisor", key=f"contact_{assignment['Level']}"):
                        st.info(f"Calling {assignment['Supervisor']}...")

def render_safety():
    """Comprehensive Safety Management with incident tracking and compliance"""
    st.title("🦺 Safety Management - Zero Incident Goal")
    st.markdown("**Comprehensive safety program with real-time monitoring**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Safety Dashboard", "⚠️ Incident Reporting", "📚 Training Tracker", "🎯 Compliance"])
    
    with tab1:
        st.markdown("### 🎯 Safety Performance Dashboard")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Safety Score", "98.5%", "+0.5% this month")
        with col2:
            st.metric("Days Since Incident", "47", "🎉 Excellent")
        with col3:
            st.metric("Near Misses", "2", "This week")
        with col4:
            st.metric("Training Complete", "94%", "Target: 100%")
        with col5:
            st.metric("PPE Compliance", "99.2%", "✅ Excellent")
        
        # Recent safety activities
        st.markdown("### 📋 Recent Safety Activities")
        safety_activities = [
            "✅ Daily safety briefing completed - All crews",
            "🎓 Fall protection training - 15 workers certified",
            "🔍 Weekly safety inspection - Level 13 structural work",
            "📋 Toolbox talk: Electrical safety around MEP work",
            "🚨 Near miss reported: Crane load swing (resolved)"
        ]
        
        for activity in safety_activities:
            st.info(activity)

def render_cost_management():
    """Advanced Cost Management with AI-powered forecasting"""
    st.title("💰 Cost Management - Financial Control Center")
    st.markdown("**Real-time budget tracking with predictive analytics**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Budget Overview", "📈 Forecasting", "💳 Change Orders", "📋 Cost Controls"])
    
    with tab1:
        st.markdown("### 💰 Real-Time Budget Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Budget", "$45.5M", "Approved contract")
        with col2:
            st.metric("Spent to Date", "$30.5M", "67% of budget")
        with col3:
            st.metric("Forecast Final", "$43.4M", "$2.1M under budget")
        with col4:
            st.metric("Contingency", "$1.5M", "3.3% remaining")
        
        # Cost breakdown visualization
        cost_data = pd.DataFrame({
            'Category': ['Labor', 'Materials', 'Equipment', 'Subcontractors', 'Overhead'],
            'Budget': [18.2, 15.8, 6.3, 3.7, 1.5],
            'Actual': [17.8, 16.1, 5.9, 3.5, 1.4],
            'Variance': [-0.4, 0.3, -0.4, -0.2, -0.1]
        })
        
        fig = px.bar(cost_data, x='Category', y=['Budget', 'Actual'], 
                    title="Budget vs Actual by Category (Millions $)", barmode='group')
        st.plotly_chart(fig, use_container_width=True)

def render_daily_reports():
    """Advanced Daily Reporting with automated data collection"""
    st.title("📊 Daily Reports - Project Progress Documentation")
    st.markdown("**Comprehensive daily reporting with automated insights**")
    
    tab1, tab2, tab3 = st.tabs(["📝 Create Report", "📊 Recent Reports", "📈 Analytics"])
    
    with tab1:
        st.markdown("### 📝 Daily Progress Report")
        
        col1, col2 = st.columns(2)
        with col1:
            report_date = st.date_input("Report Date", value=pd.Timestamp.now())
            weather = st.selectbox("Weather Conditions", ["Clear", "Partly Cloudy", "Overcast", "Light Rain", "Heavy Rain", "Snow"])
            temp_high = st.number_input("High Temperature (°F)", value=72)
            temp_low = st.number_input("Low Temperature (°F)", value=58)
        
        with col2:
            total_workers = st.number_input("Total Workers On-Site", value=89)
            work_hours = st.number_input("Total Work Hours", value=712)
            safety_incidents = st.number_input("Safety Incidents", value=0)
            quality_issues = st.number_input("Quality Issues", value=0)
        
        st.markdown("### 🏗️ Work Progress by Area")
        
        progress_areas = [
            {"Area": "Level 13 Structural", "Progress": 85, "Crew": 12, "Notes": "Steel erection proceeding on schedule"},
            {"Area": "Level 11 MEP", "Progress": 70, "Crew": 14, "Notes": "Electrical rough-in completion target Friday"},
            {"Area": "Level 9 Interior", "Progress": 45, "Crew": 8, "Notes": "Drywall installation started this week"}
        ]
        
        for area in progress_areas:
            with st.expander(f"🔧 {area['Area']} - {area['Progress']}% Complete"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text_input("Progress %", value=area['Progress'], key=f"progress_{area['Area']}")
                with col2:
                    st.text_input("Crew Size", value=area['Crew'], key=f"crew_{area['Area']}")
                with col3:
                    st.text_area("Notes", value=area['Notes'], key=f"notes_{area['Area']}")
        
        if st.button("📤 Submit Daily Report", type="primary", use_container_width=True):
            st.balloons()
            st.success("✅ Daily report submitted successfully! Report DR-2025-025 created.")

def render_progress_photos():
    """Advanced Progress Photo Management with AI organization"""
    st.title("📸 Progress Photos - Visual Documentation")
    st.markdown("**AI-powered photo organization and progress tracking**")
    
    tab1, tab2, tab3 = st.tabs(["📷 Upload Photos", "🖼️ Photo Gallery", "📊 Progress Timeline"])
    
    with tab1:
        st.markdown("### 📷 Upload Progress Photos")
        
        col1, col2 = st.columns(2)
        with col1:
            photo_location = st.selectbox("Location", ["Level 13", "Level 12", "Level 11", "Level 10", "Exterior", "Site Overall"])
            photo_category = st.selectbox("Category", ["Structural", "MEP", "Finishes", "Exterior", "Safety", "General"])
            photo_date = st.date_input("Photo Date")
        
        with col2:
            photographer = st.text_input("Photographer", value="Site Supervisor")
            notes = st.text_area("Photo Description", placeholder="Describe what the photo shows...")
        
        uploaded_photos = st.file_uploader("Upload Photos", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
        
        if uploaded_photos:
            st.success(f"✅ {len(uploaded_photos)} photos ready for upload")
            if st.button("📤 Upload & Process Photos", type="primary"):
                st.balloons()
                st.success("🎉 Photos uploaded and automatically organized by AI!")

def render_quality_control():
    """Advanced Quality Control with inspection workflows"""
    st.title("🔍 Quality Control - Inspection Management")
    st.markdown("**Comprehensive QC program with digital workflows**")
    
    tab1, tab2, tab3 = st.tabs(["✅ Inspections", "📋 Checklists", "📊 QC Metrics"])
    
    with tab1:
        st.markdown("### 🔍 Active Inspections")
        
        inspections = [
            {"ID": "QC-2025-045", "Type": "Structural", "Location": "Level 13", "Status": "In Progress", "Inspector": "John Davis"},
            {"ID": "QC-2025-044", "Type": "MEP Rough-in", "Location": "Level 11", "Status": "Passed", "Inspector": "Maria Garcia"},
            {"ID": "QC-2025-043", "Type": "Concrete", "Location": "Level 12", "Status": "Failed", "Inspector": "Robert Kim"}
        ]
        
        for inspection in inspections:
            status_color = "🟢" if inspection["Status"] == "Passed" else "🔴" if inspection["Status"] == "Failed" else "🟡"
            
            with st.expander(f"{status_color} {inspection['ID']} - {inspection['Type']} | {inspection['Status']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Location:** {inspection['Location']}")
                with col2:
                    st.markdown(f"**Inspector:** {inspection['Inspector']}")
                with col3:
                    if st.button(f"View Details", key=f"view_{inspection['ID']}"):
                        st.info(f"Opening detailed inspection report for {inspection['ID']}")

def render_material_management():
    """Advanced Material Management with supply chain integration"""
    st.title("📦 Material Management - Supply Chain Control")
    st.markdown("**Complete material tracking from procurement to installation**")
    
    tab1, tab2, tab3 = st.tabs(["📦 Inventory", "🚚 Deliveries", "📊 Analytics"])
    
    with tab1:
        st.markdown("### 📦 Current Material Inventory")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Items", "1,247", "Tracked in system")
        with col2:
            st.metric("Critical Stock", "12", "Items below threshold")
        with col3:
            st.metric("Pending Orders", "23", "Awaiting delivery")
        with col4:
            st.metric("Value On-Site", "$2.3M", "Current inventory")
        
        # Material categories
        materials = [
            {"Category": "Structural Steel", "On-Site": "850 tons", "Needed": "920 tons", "Status": "⚠️ Order placed"},
            {"Category": "Concrete", "On-Site": "2,400 CY", "Needed": "2,850 CY", "Status": "✅ Scheduled"},
            {"Category": "Windows", "On-Site": "45 units", "Needed": "120 units", "Status": "🚚 In transit"},
            {"Category": "Electrical", "On-Site": "85%", "Needed": "100%", "Status": "✅ On schedule"}
        ]
        
        for material in materials:
            with st.expander(f"📦 {material['Category']} | {material['Status']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**On-Site:** {material['On-Site']}")
                with col2:
                    st.markdown(f"**Total Needed:** {material['Needed']}")
                with col3:
                    st.markdown(f"**Status:** {material['Status']}")

def render_bim():
    """Advanced BIM Management with 3D coordination"""
    st.title("🏢 BIM Management - 3D Project Coordination")
    st.markdown("**Building Information Modeling with clash detection and coordination**")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Model Coordination", "⚠️ Clash Detection", "📊 BIM Analytics"])
    
    with tab1:
        st.markdown("### 🎯 3D Model Coordination")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Current Model Status:**
            - Architectural: Rev C (Current)
            - Structural: Rev B (Under Review)
            - MEP: Rev A (Coordinating)
            - Site: Rev A (Current)
            """)
        
        with col2:
            st.markdown("""
            **Coordination Metrics:**
            - Total Elements: 45,672
            - Clash Tests Run: 247
            - Active Clashes: 12
            - Resolved This Week: 8
            """)
        
        st.info("🔄 **Next Coordination Meeting:** Thursday 2 PM - All disciplines required")

def render_analytics():
    """Advanced Analytics with AI-powered insights"""
    st.title("📈 Advanced Analytics - AI-Powered Project Insights")
    st.markdown("**Comprehensive project analytics with predictive modeling**")
    
    tab1, tab2, tab3 = st.tabs(["📊 Executive Dashboard", "🔮 Predictive Analytics", "💡 AI Insights"])
    
    with tab1:
        st.markdown("### 📊 Executive Performance Dashboard")
        
        # Key performance indicators
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Project Health", "94%", "+2% this month")
        with col2:
            st.metric("Schedule Performance", "102%", "Ahead of plan")
        with col3:
            st.metric("Cost Performance", "96%", "Under budget")
        with col4:
            st.metric("Quality Score", "97%", "Excellent")
        
        # Performance trends
        performance_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Schedule': [98, 100, 101, 102],
            'Budget': [99, 98, 97, 96],
            'Quality': [95, 96, 96, 97],
            'Safety': [97, 98, 98, 99]
        })
        
        fig = px.line(performance_data, x='Week', y=['Schedule', 'Budget', 'Quality', 'Safety'],
                     title="📈 Weekly Performance Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🔮 AI-Powered Predictions")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🎯 Completion Forecast:**
            - Projected Completion: May 15, 2025
            - Confidence Level: 87%
            - Weather Risk Factor: Low
            - Resource Availability: Good
            """)
        
        with col2:
            st.markdown("""
            **💰 Cost Forecast:**
            - Final Cost Prediction: $43.4M
            - Confidence Level: 92%
            - Potential Savings: $2.1M
            - Risk Factors: Material prices
            """)

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