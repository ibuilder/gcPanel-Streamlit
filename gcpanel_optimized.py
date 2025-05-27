"""
Highland Tower Development - Optimized Construction Management Platform
$45.5M Mixed-Use Development - Pure Python Core with Streamlit UI

Optimized architecture using pure Python business logic for maximum longevity
"""

import streamlit as st
from core.data_models import RFIStatus, Priority, Discipline
from core.business_logic import highland_tower_manager
from core.ui_components import ui_components, data_processor
from typing import Dict, Any


def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Highland Tower Development - gcPanel",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_styling():
    """Apply optimized CSS styling"""
    st.markdown("""
    <style>
    .main .block-container {
        max-width: 1400px;
        padding: 1.5rem 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        color: #f1f5f9;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        transform: translateY(-2px);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e40af 0%, #1e3a8a 100%);
        color: white;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #fbbf24;
        font-weight: 700;
        margin: 1rem 0 0.5rem 0;
        border-bottom: 2px solid #fbbf24;
        padding-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render optimized sidebar navigation"""
    with st.sidebar:
        # Project header
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.2); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h3 style="color: #60a5fa; margin: 0;">Highland Tower Development</h3>
            <p style="margin: 0.5rem 0 0 0;"><strong>Investment:</strong> $45.5M</p>
            <p style="margin: 0;"><strong>Status:</strong> <span style="color: #10b981;">Active Development</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("### 🎯 Core Tools")
        core_modules = [
            ("📊 Dashboard", "Dashboard"),
            ("📝 Daily Reports", "Daily Reports"),
            ("🦺 Safety", "Safety")
        ]
        
        for display_name, module in core_modules:
            if st.button(display_name, key=f"core_{module}", use_container_width=True):
                st.session_state.current_menu = module
                st.rerun()
        
        st.markdown("### 🔧 Advanced Tools")
        advanced_modules = [
            ("❓ RFIs", "RFIs"),
            ("👥 Subcontractors", "Subcontractors"),
            ("📊 Inspections", "Inspections"),
            ("📸 Progress Photos", "Progress Photos"),
            ("📈 Performance", "Performance")
        ]
        
        for display_name, module in advanced_modules:
            if st.button(display_name, key=f"adv_{module}", use_container_width=True):
                st.session_state.current_menu = module
                st.rerun()
        
        st.markdown("---")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()


def render_dashboard():
    """Render optimized dashboard using pure Python data"""
    st.title("🏗️ Highland Tower Development Dashboard")
    
    # Get dashboard data from pure Python backend
    dashboard_data = ui_components.generate_dashboard_data()
    
    # Project info section
    project_info = dashboard_data["project_info"]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Project Value", project_info["value"])
    with col2:
        st.metric("Progress", project_info["progress"])
    with col3:
        st.metric("Days Remaining", project_info["days_remaining"])
    with col4:
        st.metric("Status", project_info["status"])
    
    st.markdown("---")
    
    # Key metrics
    st.markdown("### 📊 Key Performance Indicators")
    metrics = dashboard_data["key_metrics"]
    
    col1, col2, col3, col4 = st.columns(4)
    for i, metric in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.metric(
                metric["title"],
                metric["value"],
                delta=metric["trend"]
            )
    
    # Recent activities
    st.markdown("### 📋 Recent Activities")
    for activity in dashboard_data["recent_activities"][-5:]:
        st.info(activity)


def render_rfis():
    """Render optimized RFI management using pure Python backend"""
    st.title("📝 Request for Information (RFIs)")
    st.markdown("**Highland Tower Development - Professional RFI Management**")
    
    # Get RFI data from pure Python backend
    rfi_data = ui_components.generate_rfi_list_data()
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Create RFI", type="primary", use_container_width=True):
            st.session_state.rfi_mode = "create"
            st.rerun()
    
    with col2:
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.rfi_mode = "search"
            st.rerun()
    
    with col3:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.rfi_mode = "analytics"
            st.rerun()
    
    with col4:
        if st.button("📋 Export", use_container_width=True):
            export_data = highland_tower_manager.export_project_data()
            st.download_button(
                "📥 Download Data",
                str(export_data),
                "highland_tower_rfis.json",
                "application/json"
            )
    
    st.markdown("---")
    
    # Handle different modes
    if st.session_state.get("rfi_mode") == "create":
        render_rfi_form()
    elif st.session_state.get("rfi_mode") == "search":
        render_rfi_search()
    elif st.session_state.get("rfi_mode") == "analytics":
        render_rfi_analytics()
    else:
        render_rfi_list(rfi_data)


def render_rfi_list(rfi_data: Dict[str, Any]):
    """Render RFI list using pure Python data"""
    # Statistics
    stats = rfi_data["statistics"]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total RFIs", stats["total"])
    with col2:
        st.metric("Open RFIs", stats["open"])
    with col3:
        st.metric("Critical", stats["critical"])
    with col4:
        st.metric("Avg Days Open", f"{stats['avg_days_open']} days")
    
    st.markdown("### 📋 Active RFIs")
    
    # Display RFIs using pure Python data
    for rfi in rfi_data["rfis"]:
        with st.expander(f"{rfi['priority_icon']} {rfi['number']} - {rfi['subject']}", expanded=False):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown(f"""
                **📋 RFI Details:**
                - **Priority:** {rfi['priority']} {rfi['priority_icon']}
                - **Status:** {rfi['status']} {rfi['status_icon']}
                - **Discipline:** {rfi['discipline']}
                - **Location:** {rfi['location']}
                - **Submitted by:** {rfi['submitted_by']}
                - **Due Date:** {rfi['due_date']}
                - **Days Open:** {rfi['days_open']}
                """)
            
            with col2:
                st.markdown(f"**📝 Description:**")
                st.markdown(rfi['description'])
                st.markdown(f"**💰 Cost Impact:** {rfi['cost_impact']}")
                st.markdown(f"**📅 Schedule Impact:** {rfi['schedule_impact']}")
                
                # Action buttons
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                
                with btn_col1:
                    if st.button("✏️ Edit", key=f"edit_{rfi['id']}", use_container_width=True):
                        st.info(f"Edit functionality for {rfi['number']}")
                
                with btn_col2:
                    if st.button("💬 Respond", key=f"respond_{rfi['id']}", use_container_width=True):
                        st.info(f"Response functionality for {rfi['number']}")
                
                with btn_col3:
                    if st.button("📊 Details", key=f"details_{rfi['id']}", use_container_width=True):
                        st.info(f"Detailed view for {rfi['number']}")


def render_rfi_form():
    """Render RFI creation form using pure Python form structure"""
    st.markdown("### ➕ Create New RFI")
    
    if st.button("← Back to RFI List"):
        st.session_state.rfi_mode = None
        st.rerun()
    
    # Get form structure from pure Python backend
    form_data = ui_components.generate_rfi_form_data()
    
    with st.form("create_rfi_form"):
        st.markdown(f"**{form_data['title']}**")
        
        form_values = {}
        
        # Generate form fields from pure Python structure
        col1, col2 = st.columns(2)
        
        for i, field in enumerate(form_data['fields']):
            column = col1 if i % 2 == 0 else col2
            
            with column:
                if field['type'] == 'text':
                    form_values[field['name']] = st.text_input(
                        field['label'],
                        placeholder=field.get('placeholder', ''),
                        key=f"form_{field['name']}"
                    )
                elif field['type'] == 'select':
                    form_values[field['name']] = st.selectbox(
                        field['label'],
                        field['options'],
                        key=f"form_{field['name']}"
                    )
                elif field['type'] == 'textarea':
                    form_values[field['name']] = st.text_area(
                        field['label'],
                        placeholder=field.get('placeholder', ''),
                        height=120,
                        key=f"form_{field['name']}"
                    )
        
        submitted = st.form_submit_button("📤 Submit RFI", type="primary")
        
        if submitted:
            if form_values['subject'] and form_values['description']:
                # Create RFI using pure Python backend
                rfi_data = {
                    'subject': form_values['subject'],
                    'description': form_values['description'],
                    'location': form_values['location'],
                    'discipline': Discipline(form_values['discipline'].lower().replace(' ', '_')),
                    'priority': Priority(form_values['priority'].lower()),
                    'assigned_to': form_values['assigned_to'],
                    'cost_impact': form_values['cost_impact'],
                    'schedule_impact': form_values['schedule_impact'],
                    'submitted_by': "Highland Tower Team",
                    'status': RFIStatus.OPEN,
                    'submitted_date': highland_tower_manager.project.start_date,
                    'due_date': highland_tower_manager.project.start_date
                }
                
                new_rfi = highland_tower_manager.create_rfi(rfi_data)
                st.success(f"✅ RFI created successfully! Reference: {new_rfi.number}")
                st.session_state.rfi_mode = None
                st.rerun()
            else:
                st.error("Please provide required fields: Subject and Description")


def render_rfi_search():
    """Render RFI search using pure Python filtering"""
    st.markdown("### 🔍 Search Highland Tower RFIs")
    
    if st.button("← Back to RFI List"):
        st.session_state.rfi_mode = None
        st.rerun()
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All"] + [s.value.title().replace("_", " ") for s in RFIStatus])
    
    with col2:
        priority_filter = st.selectbox("Filter by Priority", ["All"] + [p.value.title() for p in Priority])
    
    with col3:
        discipline_filter = st.selectbox("Filter by Discipline", ["All"] + [d.value.title().replace("_", " ") for d in Discipline])
    
    search_text = st.text_input("🔍 Search in subjects and descriptions", placeholder="Enter keywords...")
    
    # Apply filters using pure Python backend
    filters = {}
    if status_filter != "All":
        filters["status"] = status_filter.lower().replace(" ", "_")
    if priority_filter != "All":
        filters["priority"] = priority_filter.lower()
    if discipline_filter != "All":
        filters["discipline"] = discipline_filter.lower().replace(" ", "_")
    if search_text:
        filters["search_text"] = search_text
    
    # Get filtered RFIs from pure Python backend
    all_rfis = highland_tower_manager.get_rfis()
    filtered_rfis = data_processor.filter_rfis(all_rfis, filters)
    
    st.markdown(f"### 📝 Found {len(filtered_rfis)} RFIs")
    
    # Display filtered results
    for rfi in filtered_rfis:
        st.markdown(f"**{rfi.number}** - {rfi.subject} ({rfi.priority.value.title()})")


def render_rfi_analytics():
    """Render RFI analytics using pure Python chart data"""
    st.markdown("### 📊 RFI Analytics Dashboard")
    
    if st.button("← Back to RFI List"):
        st.session_state.rfi_mode = None
        st.rerun()
    
    # Get analytics data from pure Python backend
    chart_data = ui_components.generate_analytics_charts_data()
    stats = highland_tower_manager.get_rfi_statistics()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total RFIs", stats["total"])
    with col2:
        st.metric("Open RFIs", stats["open"])
    with col3:
        st.metric("Critical RFIs", stats["critical"])
    with col4:
        st.metric("Avg Days Open", f"{stats['avg_days_open']} days")
    
    # Charts using pure Python data
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### RFIs by Priority")
        priority_data = chart_data["priority_chart"]["data"]
        if priority_data:
            st.bar_chart(priority_data)
    
    with col2:
        st.markdown("#### RFIs by Discipline")
        discipline_data = chart_data["discipline_chart"]["data"]
        if discipline_data:
            st.bar_chart(discipline_data)


def render_subcontractors():
    """Render subcontractor management using pure Python data"""
    st.title("👥 Subcontractor Management")
    
    # Get subcontractor data from pure Python backend
    sub_data = ui_components.generate_subcontractor_data()
    
    # Summary cards
    st.markdown("### 📊 Overview")
    cols = st.columns(len(sub_data["summary_cards"]))
    
    for i, card in enumerate(sub_data["summary_cards"]):
        with cols[i]:
            st.metric(card["title"], card["value"])
    
    st.markdown("---")
    
    # Subcontractor list
    st.markdown("### 👥 Active Subcontractors")
    
    for sub in sub_data["subcontractors"]:
        with st.expander(f"**{sub['company_name']}** - {sub['specialties']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Contact Information:**
                - **Contact:** {sub['contact_person']}
                - **Email:** {sub['email']}
                - **Phone:** {sub['phone']}
                """)
            
            with col2:
                st.markdown(f"""
                **Performance Metrics:**
                - **Rating:** {sub['performance_rating']}/5.0 ⭐
                - **Active Projects:** {sub['active_projects']}
                - **Contract Value:** {sub['contract_value_formatted']}
                - **Insurance:** {sub['insurance_status'].title()}
                """)


def main():
    """Main application entry point"""
    configure_page()
    apply_styling()
    
    # Initialize session state
    if "current_menu" not in st.session_state:
        st.session_state.current_menu = "Dashboard"
    
    # Render sidebar
    render_sidebar()
    
    # Route to appropriate module based on pure Python backend
    current_menu = st.session_state.current_menu
    
    if current_menu == "Dashboard":
        render_dashboard()
    elif current_menu == "RFIs":
        render_rfis()
    elif current_menu == "Subcontractors":
        render_subcontractors()
    else:
        st.title(f"🚧 {current_menu}")
        st.info(f"The {current_menu} module is being developed with pure Python architecture for maximum efficiency.")
        
        # Show sample data from pure Python backend
        if current_menu in ["Performance", "Inspections"]:
            health_metrics = highland_tower_manager.get_project_health_metrics()
            st.json(health_metrics)


if __name__ == "__main__":
    main()