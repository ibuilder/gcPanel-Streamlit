"""
Highland Tower Development - Clean Modular gcPanel
Completely refactored for independent component loading and debugging
"""

import streamlit as st
import pandas as pd
import plotly.express as px

def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        "authenticated": False,
        "username": "",
        "user_role": "guest", 
        "current_menu": "Dashboard",
        "theme": "dark"
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def apply_theme():
    """Apply theme based on user selection"""
    current_theme = st.session_state.get("theme", "dark")
    
    if current_theme == "dark":
        st.markdown("""
        <style>
            .stApp { background-color: #0e1117; color: white; }
            section[data-testid="stSidebar"] { 
                background-color: #262730; 
                color: white;
            }
            section[data-testid="stSidebar"] .stMarkdown { color: white; }
            section[data-testid="stSidebar"] h1, 
            section[data-testid="stSidebar"] h2, 
            section[data-testid="stSidebar"] h3, 
            section[data-testid="stSidebar"] h4, 
            section[data-testid="stSidebar"] h5, 
            section[data-testid="stSidebar"] h6 { color: white; }
            section[data-testid="stSidebar"] p { color: #e2e8f0; }
            section[data-testid="stSidebar"] .stSelectbox label { color: white; }
            section[data-testid="stSidebar"] .stButton label { color: white; }
            .main .block-container { background-color: #0e1117; color: white; padding-top: 1rem; }
            [data-testid="metric-container"] { background-color: #262730; border: 1px solid #464854; color: white; }
            .stButton > button { background-color: #3498db; color: white; border: none; }
            .stButton > button:hover { background-color: #2980b9; }
            .sidebar .sidebar-content { color: white; }
            div[data-testid="stSidebar"] > div { color: white; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp { background-color: #ffffff; color: #262730; }
            section[data-testid="stSidebar"] { background-color: #f0f2f6; }
            .main .block-container { background-color: #ffffff; color: #262730; padding-top: 1rem; }
            [data-testid="metric-container"] { background-color: #f0f2f6; border: 1px solid #d1d5db; color: #262730; }
            .stButton > button { background-color: #3498db; color: white; border: none; }
            .stButton > button:hover { background-color: #2980b9; }
        </style>
        """, unsafe_allow_html=True)

def render_sidebar():
    """Render the complete sidebar"""
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 3em; margin-bottom: 10px;'>🏗️</div>
            <h2 style='color: #3498db; margin: 0; font-weight: bold;'>gcPanel</h2>
            <p style='color: #95a5a6; font-size: 0.9em; margin: 5px 0;'>Construction Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation Menu (moved up below logo)
        is_authenticated = st.session_state.get("authenticated", False)
        
        if is_authenticated:
            st.markdown("### 🧭 Navigation")
            
            # Create navigation buttons with icons
            if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.get("current_menu", "Dashboard") == "Dashboard" else "secondary"):
                st.session_state["current_menu"] = "Dashboard"
                st.rerun()
            
            if st.button("🏗️ Preconstruction", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "Preconstruction" else "secondary"):
                st.session_state["current_menu"] = "Preconstruction"
                st.rerun()
            
            if st.button("⚙️ Engineering", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "Engineering" else "secondary"):
                st.session_state["current_menu"] = "Engineering"
                st.rerun()
            
            if st.button("👷 Field Operations", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "Field Operations" else "secondary"):
                st.session_state["current_menu"] = "Field Operations"
                st.rerun()
            
            if st.button("🦺 Safety", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "Safety" else "secondary"):
                st.session_state["current_menu"] = "Safety"
                st.rerun()
            
            if st.button("📄 Contracts", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "Contracts" else "secondary"):
                st.session_state["current_menu"] = "Contracts"
                st.rerun()
            
            if st.button("💰 Cost Management", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "Cost Management" else "secondary"):
                st.session_state["current_menu"] = "Cost Management"
                st.rerun()
            
            if st.button("🏢 BIM", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "BIM" else "secondary"):
                st.session_state["current_menu"] = "BIM"
                st.rerun()
            
            if st.button("✅ Closeout", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "Closeout" else "secondary"):
                st.session_state["current_menu"] = "Closeout"
                st.rerun()
            
            if st.button("📈 Analytics", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "Analytics" else "secondary"):
                st.session_state["current_menu"] = "Analytics"
                st.rerun()
            
            if st.button("📁 Documents", use_container_width=True, type="primary" if st.session_state.get("current_menu") == "Documents" else "secondary"):
                st.session_state["current_menu"] = "Documents"
                st.rerun()
        
        st.divider()
        
        # Project Information
        st.markdown("### 🏗️ Highland Tower Development")
        st.markdown("""
        **Project Value:** $45.5M  
        **Type:** Mixed-Use Development  
        **Units:** 120 Residential + 8 Retail  
        **Size:** 168,500 sq ft  
        **Floors:** 15 Above + 2 Below Ground
        """)
        
        st.divider()
        
        # User info or About section
        
        if is_authenticated:
            current_user = st.session_state.get("username", "Project Manager")
            user_role = st.session_state.get("user_role", "admin")
            st.markdown(f"**User:** {current_user}  \n**Role:** {user_role.title()}")
        else:
            st.markdown("### About gcPanel")
            st.markdown("""
            **gcPanel** is the industry-leading construction management platform.
            
            🏗️ **Features:**
            • Project Dashboard & Analytics
            • BIM Integration & Visualization  
            • Safety Management & Compliance
            • Cost Control & Budget Tracking
            • Document Management
            • Field Operations Support
            
            💼 **Perfect for:**
            • General Contractors • Project Managers
            • Construction Teams • Development Companies
            """)
            
            if st.button("🌐 Visit www.gcpanel.co", use_container_width=True, type="primary"):
                st.markdown("[Visit gcPanel.co](https://www.gcpanel.co)")
        
        # Quick Actions (for authenticated users only)
        if is_authenticated:
            st.divider()
            st.markdown("### ⚡ Quick Actions")
            if st.button("📊 View Reports", use_container_width=True):
                st.session_state["current_menu"] = "Analytics"
                st.rerun()
            
            if st.button("📋 Safety Check", use_container_width=True):
                st.session_state["current_menu"] = "Safety"
                st.rerun()
            
            if st.button("💰 Budget Review", use_container_width=True):
                st.session_state["current_menu"] = "Cost Management"
                st.rerun()
        
        st.divider()
        
        # Theme Toggle
        st.markdown("### 🎨 Theme")
        current_theme = st.session_state.get("theme", "dark")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Dark", 
                        type="primary" if current_theme == "dark" else "secondary",
                        use_container_width=True):
                st.session_state.theme = "dark"
                st.rerun()
        
        with col2:
            if st.button("☀️ Light", 
                        type="primary" if current_theme == "light" else "secondary", 
                        use_container_width=True):
                st.session_state.theme = "light"
                st.rerun()

def render_login():
    """Render login form"""
    st.title("🏗️ gcPanel Login")
    st.subheader("Highland Tower Development")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if submitted:
            if username and password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_role = "admin"
                st.rerun()
            else:
                st.error("Please enter username and password")
    
    # Demo accounts
    st.divider()
    st.subheader("Demo Accounts")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍💼 Project Manager", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Project Manager"
            st.session_state.user_role = "admin"
            st.rerun()
    
    with col2:
        if st.button("👷‍♂️ Superintendent", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Superintendent"
            st.session_state.user_role = "field"
            st.rerun()

def render_dashboard():
    """Render the main dashboard"""
    st.title("🏗️ Highland Tower Development Dashboard")
    
    # Project Overview Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Project Value", "$45.5M", "On Budget")
    with col2:
        st.metric("Progress", "67%", "2% this week")
    with col3:
        st.metric("Units Complete", "81/128", "5 this week")
    with col4:
        st.metric("Safety Score", "98%", "0.5% improvement")
    
    st.divider()
    
    # Recent Activity and Action Items
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 Recent Activity")
        st.write("• Foundation inspection completed - Unit 12A")
        st.write("• MEP rough-in approved - Floors 8-10")
        st.write("• Concrete pour scheduled - Level B2")
        st.write("• Fire safety inspection passed - Retail spaces")
        st.write("• Final electrical inspection - Units 45-50")
    
    with col2:
        st.subheader("⚠️ Action Items")
        st.warning("🔧 HVAC system calibration due - Floor 15")
        st.info("📋 Weekly safety meeting - Tomorrow 9 AM")
        st.success("✅ Permit renewal submitted - On track")
        st.error("🚨 Weather delay possible - Monitor forecast")
    
    st.divider()
    
    # Progress Chart
    st.subheader("📊 Construction Progress")
    progress_data = pd.DataFrame({
        'Phase': ['Foundation', 'Structure', 'MEP', 'Interior', 'Exterior'],
        'Planned': [100, 100, 85, 45, 30],
        'Actual': [100, 98, 82, 42, 25]
    })
    
    fig = px.bar(progress_data, x='Phase', y=['Planned', 'Actual'], 
                title='Project Phase Progress (%)', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

def render_main_content():
    """Render main content based on selected module"""
    current_menu = st.session_state.get("current_menu", "Dashboard")
    
    try:
        if current_menu == "Dashboard":
            render_dashboard()
        elif current_menu == "Preconstruction":
            # Import and use the sophisticated preconstruction module
            import modules.preconstruction
            modules.preconstruction.render()
        elif current_menu == "Engineering":
            # Import the advanced engineering module
            try:
                import modules.engineering
                modules.engineering.render()
            except ImportError:
                import modules.rfis
                modules.rfis.render()
        elif current_menu == "Field Operations":
            # Import field operations with daily reports and photo logs
            try:
                import modules.field_operations
                modules.field_operations.render()
            except ImportError:
                import modules.daily_reports
                modules.daily_reports.render()
        elif current_menu == "Safety":
            # Import safety management with incident tracking
            try:
                import modules.safety
                modules.safety.render()
            except ImportError:
                st.title("🦺 Safety Management")
                st.info("Safety module loading...")
        elif current_menu == "Contracts":
            # Import contracts with CRUD functionality
            try:
                import modules.contracts
                modules.contracts.render()
            except ImportError:
                st.title("📄 Contract Management")
                st.info("Contracts module loading...")
        elif current_menu == "Cost Management":
            # Import the sophisticated cost management with CRUD
            try:
                import modules.cost_management
                modules.cost_management.render()
            except ImportError:
                st.title("💰 Cost Management")
                st.info("Cost management module loading...")
        elif current_menu == "BIM":
            # Import BIM with 3D viewer and clash detection
            try:
                import modules.bim
                modules.bim.render()
            except ImportError:
                try:
                    import modules.bim_viewer.basic_viewer
                    modules.bim_viewer.basic_viewer.render()
                except ImportError:
                    st.title("🏢 BIM Management")
                    st.info("BIM module loading...")
        elif current_menu == "Closeout":
            # Import closeout module
            try:
                import modules.closeout
                modules.closeout.render()
            except ImportError:
                st.title("✅ Project Closeout")
                st.info("Closeout module loading...")
        elif current_menu == "Analytics":
            # Import analytics module
            try:
                import modules.analytics
                modules.analytics.render()
            except ImportError:
                st.title("📈 Analytics & Business Intelligence")
                st.info("Analytics module loading...")
        elif current_menu == "Documents":
            # Import document management
            try:
                import modules.documents
                modules.documents.render()
            except ImportError:
                try:
                    import modules.pdf_viewer.pdf_viewer
                    modules.pdf_viewer.pdf_viewer.render()
                except ImportError:
                    st.title("📁 Document Management")
                    st.info("Documents module loading...")
        else:
            st.title(f"🔧 {current_menu}")
            st.info(f"The {current_menu} module is being connected.")
    
    except Exception as e:
        st.error(f"Error loading {current_menu} module: {str(e)}")
        st.info("Please try selecting a different module or refresh the page.")

# Removed placeholder functions - now using actual sophisticated modules

def render_engineering():
    """Render Engineering module"""
    st.title("⚙️ Engineering")
    
    tab1, tab2, tab3, tab4 = st.tabs(["RFIs", "Submittals", "Transmittals", "Design Coordination"])
    
    with tab1:
        st.subheader("RFIs (Request for Information)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Open RFIs", "12", "-3 this week")
        with col2:
            st.metric("Pending Response", "8", "2 overdue")
        with col3:
            st.metric("Avg Response Time", "3.2 days", "Target: 3 days")
    
    with tab2:
        st.subheader("Submittals")
        st.write("**Recent Submittals:**")
        st.success("✅ HVAC Equipment - Approved")
        st.warning("⏳ Elevator Systems - Under Review")
        st.info("📋 Window Systems - Submitted")
    
    with tab3:
        st.subheader("Transmittals")
        st.write("**Document Transmittals:**")
        st.write("• Structural drawings revision 3")
        st.write("• MEP coordination drawings")
        st.write("• Architectural details package")
    
    with tab4:
        st.subheader("Design Coordination")
        st.write("**Coordination Status:**")
        st.write("• Architectural-Structural: 95% complete")
        st.write("• MEP-Structural: 87% complete")
        st.write("• Fire protection integration: 92% complete")

def render_field_operations():
    """Render Field Operations module"""
    st.title("👷 Field Operations")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Daily Reports", "Progress Tracking", "Quality Control", "Inspections"])
    
    with tab1:
        st.subheader("Daily Reports")
        st.write("**Today's Activities:**")
        st.write("• Concrete pour - Level 8 deck")
        st.write("• MEP rough-in - Levels 6-7")
        st.write("• Drywall installation - Level 4")
        st.write("• Site utilities installation")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Crew Size", "45", "+5 today")
        with col2:
            st.metric("Weather", "Clear", "Good conditions")
    
    with tab2:
        st.subheader("Progress Tracking")
        st.write("**Weekly Progress:**")
        progress_data = pd.DataFrame({
            'Activity': ['Foundation', 'Structure', 'MEP', 'Finishes'],
            'Planned': [100, 75, 45, 20],
            'Actual': [100, 78, 42, 18]
        })
        st.dataframe(progress_data)
    
    with tab3:
        st.subheader("Quality Control")
        st.write("**QC Checkpoints:**")
        st.success("✅ Concrete strength tests passed")
        st.success("✅ Structural inspections current")
        st.warning("⚠️ Waterproofing inspection pending")
    
    with tab4:
        st.subheader("Inspections")
        st.write("**Upcoming Inspections:**")
        st.write("• Foundation final - January 28")
        st.write("• Electrical rough-in - January 30")
        st.write("• Fire sprinkler - February 2")

def render_safety():
    """Render Safety module"""
    st.title("🦺 Safety")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Incidents", "Training", "Compliance"])
    
    with tab1:
        st.subheader("Safety Dashboard")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Days Without Incident", "156", "+1")
        with col2:
            st.metric("Safety Score", "98%", "+0.5%")
        with col3:
            st.metric("Training Completion", "94%", "Target: 95%")
        with col4:
            st.metric("Inspections This Week", "12", "All passed")
    
    with tab2:
        st.subheader("Incident Reports")
        st.success("🎉 Zero incidents this month!")
        st.write("**Recent Safety Highlights:**")
        st.write("• New safety harness training completed")
        st.write("• Updated fall protection protocols")
        st.write("• Weekly toolbox talks conducted")
    
    with tab3:
        st.subheader("Training Records")
        st.write("**Required Training Status:**")
        st.write("• OSHA 30-Hour: 89% completion")
        st.write("• Fall Protection: 96% completion")
        st.write("• Equipment Operation: 92% completion")
    
    with tab4:
        st.subheader("Compliance Monitoring")
        st.write("**Regulatory Compliance:**")
        st.success("✅ OSHA compliance current")
        st.success("✅ EPA requirements met")
        st.info("📋 Monthly safety audit scheduled")

def render_contracts():
    """Render Contracts module"""
    st.title("📄 Contracts")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Prime Contract", "Subcontracts", "Change Orders", "Procurement"])
    
    with tab1:
        st.subheader("Prime Contract")
        st.write("**Contract Details:**")
        st.write("• Contract Value: $45.5M")
        st.write("• Duration: 24 months")
        st.write("• Completion: March 2026")
        st.write("• Performance: On schedule")
    
    with tab2:
        st.subheader("Subcontracts")
        st.write("**Major Subcontractors:**")
        st.write("• Excavation: ABC Earthworks - $1.2M")
        st.write("• Concrete: Metro Concrete - $8.5M")
        st.write("• Steel: Steel Solutions - $6.8M")
        st.write("• MEP: Technical Systems - $9.2M")
    
    with tab3:
        st.subheader("Change Orders")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pending COs", "3", "Review needed")
        with col2:
            st.metric("Approved COs", "$125K", "Within budget")
    
    with tab4:
        st.subheader("Procurement")
        st.write("**Material Orders:**")
        st.write("• Structural steel: Delivered")
        st.write("• Windows: In production")
        st.write("• HVAC equipment: Ordered")

def render_cost_management():
    """Render Cost Management module"""
    st.title("💰 Cost Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Budget", "Cash Flow", "Billing", "Forecasting"])
    
    with tab1:
        st.subheader("Budget Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Budget", "$45.5M", "Baseline")
        with col2:
            st.metric("Current Budget", "$45.7M", "+$200K COs")
        with col3:
            st.metric("Spent to Date", "$30.4M", "67% of budget")
    
    with tab2:
        st.subheader("Cash Flow Analysis")
        st.write("**Monthly Cash Flow:**")
        st.write("• January: $2.8M projected")
        st.write("• February: $3.1M projected")
        st.write("• March: $2.9M projected")
    
    with tab3:
        st.subheader("AIA Billing (G702/G703)")
        st.write("**Current Application:**")
        st.write("• Application #8 - January 2025")
        st.write("• Amount: $2,847,500")
        st.write("• Status: Under review")
    
    with tab4:
        st.subheader("Cost Forecasting")
        st.write("**Projected Final Cost:**")
        st.success("✅ On budget: $45.7M projected final")
        st.write("• Remaining work: $15.3M")
        st.write("• Contingency available: $450K")

def render_bim():
    """Render BIM module"""
    st.title("🏢 BIM")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Model Viewer", "Clash Detection", "4D Scheduling", "Model Coordination"])
    
    with tab1:
        st.subheader("3D Model Viewer")
        st.info("📱 Interactive 3D model viewer will load here")
        st.write("**Model Information:**")
        st.write("• Last updated: January 25, 2025")
        st.write("• Model size: 485 MB")
        st.write("• Elements: 12,847 objects")
    
    with tab2:
        st.subheader("Clash Detection")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Clashes", "8", "-5 resolved")
        with col2:
            st.metric("Critical Clashes", "2", "Priority")
        
        st.write("**Recent Clashes:**")
        st.warning("⚠️ HVAC duct conflicts with structural beam - Level 8")
        st.info("🔄 Electrical conduit routing issue - Level 6")
    
    with tab3:
        st.subheader("4D Scheduling")
        st.write("**Construction Sequence:**")
        st.write("• Foundation: Complete")
        st.write("• Structure: 78% complete")
        st.write("• MEP rough-in: 42% complete")
        st.write("• Exterior envelope: 25% complete")
    
    with tab4:
        st.subheader("Model Coordination")
        st.write("**Coordination Status:**")
        st.success("✅ Architectural model: Up to date")
        st.success("✅ Structural model: Up to date")
        st.warning("⚠️ MEP model: Update pending")

def render_closeout():
    """Render Closeout module"""
    st.title("✅ Closeout")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Punchlist", "Documentation", "Commissioning", "Handover"])
    
    with tab1:
        st.subheader("Punchlist Management")
        st.write("**Completion Status:**")
        st.write("• Total items: 847")
        st.write("• Completed: 623 (74%)")
        st.write("• Remaining: 224")
        st.write("• Critical: 12 items")
    
    with tab2:
        st.subheader("Project Documentation")
        st.write("**Required Documents:**")
        st.success("✅ As-built drawings")
        st.success("✅ Operation manuals")
        st.warning("⏳ Warranty documentation")
        st.info("📋 Final inspections pending")
    
    with tab3:
        st.subheader("Systems Commissioning")
        st.write("**Commissioning Status:**")
        st.write("• HVAC systems: 85% complete")
        st.write("• Fire safety: 92% complete")
        st.write("• Electrical: 78% complete")
        st.write("• Elevators: 95% complete")
    
    with tab4:
        st.subheader("Project Handover")
        st.write("**Handover Preparation:**")
        st.write("• Training schedules prepared")
        st.write("• Maintenance manuals compiled")
        st.write("• Warranty periods documented")
        st.write("• Final walkthrough scheduled")

def render_analytics():
    """Render Analytics module"""
    st.title("📈 Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["KPIs", "Performance", "Trends", "Reports"])
    
    with tab1:
        st.subheader("Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Schedule Performance", "102%", "+2% ahead")
        with col2:
            st.metric("Cost Performance", "99.2%", "Under budget")
        with col3:
            st.metric("Quality Score", "96%", "+1% improvement")
        with col4:
            st.metric("Safety Rating", "98%", "Excellent")
    
    with tab2:
        st.subheader("Project Performance")
        st.write("**Performance Trends:**")
        st.write("• Productivity up 8% this quarter")
        st.write("• Rework reduced by 15%")
        st.write("• Material waste down 12%")
    
    with tab3:
        st.subheader("Trend Analysis")
        st.write("**Data Insights:**")
        st.write("• Weather delays decreased 20%")
        st.write("• Subcontractor performance improved")
        st.write("• Change order frequency stable")
    
    with tab4:
        st.subheader("Reports")
        st.write("**Available Reports:**")
        st.write("• Weekly progress report")
        st.write("• Monthly financial summary")
        st.write("• Safety performance report")
        st.write("• Quality metrics dashboard")

def render_documents():
    """Render Documents module"""
    st.title("📁 Documents")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Drawings", "Specifications", "Correspondence", "Photos"])
    
    with tab1:
        st.subheader("Project Drawings")
        st.write("**Drawing Sets:**")
        st.write("• Architectural: 45 sheets")
        st.write("• Structural: 32 sheets")
        st.write("• MEP: 68 sheets")
        st.write("• Site/Civil: 12 sheets")
    
    with tab2:
        st.subheader("Technical Specifications")
        st.write("**Specification Sections:**")
        st.write("• Division 03 - Concrete")
        st.write("• Division 05 - Metals")
        st.write("• Division 23 - HVAC")
        st.write("• Division 26 - Electrical")
    
    with tab3:
        st.subheader("Project Correspondence")
        st.write("**Recent Communications:**")
        st.write("• Architect coordination meeting notes")
        st.write("• Owner approval requests")
        st.write("• Permit agency responses")
    
    with tab4:
        st.subheader("Photo Documentation")
        st.write("**Photo Categories:**")
        st.write("• Progress photos: 1,247 images")
        st.write("• Quality documentation: 423 images")
        st.write("• Safety inspections: 89 images")

def main():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(
        page_title="Highland Tower Development - gcPanel",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply theme
    apply_theme()
    
    # Check authentication and render appropriate content
    if not st.session_state.get("authenticated", False):
        # Show sidebar for non-authenticated users
        render_sidebar()
        
        # Show login in main content
        render_login()
    else:
        # Show sidebar for authenticated users
        render_sidebar()
        
        # Show main content
        render_main_content()
        
        # Logout button in main area
        if st.button("🚪 Logout", key="logout_main"):
            for key in ["authenticated", "username", "user_role"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()