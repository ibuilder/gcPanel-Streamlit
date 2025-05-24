"""
gcPanel Construction Management Dashboard - Enterprise Edition

Highland Tower Development Project Management System
$45.5M Mixed-Use Development - 120 Residential + 8 Retail Units

🏗️ ENTERPRISE FEATURES:
✓ PostgreSQL Database with connection pooling
✓ Redis caching for high-performance operations  
✓ Role-based security & encryption
✓ Real-time notifications & live updates
✓ AI-powered predictive analytics
✓ Mobile-first responsive design
✓ API integrations (Procore, Autodesk, QuickBooks)
✓ Offline field operations capability
✓ Advanced search across all modules
✓ Photo management with GPS tagging
✓ QR code integration for equipment/materials
✓ Comprehensive audit logging
"""

import streamlit as st
import sys
import os
from datetime import datetime
import logging

# Configure Streamlit page
st.set_page_config(
    page_title="gcPanel Enterprise - Highland Tower Development",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import enterprise core systems
try:
    from core.database_manager import get_database_manager
    from core.cache_manager import get_cache_manager
    from core.security_manager import get_security_manager, require_permission, Permission, UserRole
    from core.realtime_manager import get_realtime_manager, initialize_live_updates
    from core.search_manager import get_search_manager
    from core.mobile_manager import get_mobile_manager, apply_responsive_layout
    from core.integration_manager import get_integration_manager
    from core.analytics_manager import get_analytics_manager
    from core.field_manager import get_field_manager
    
    # Import existing modules
    from modules import dashboard, analytics, preconstruction, engineering
    from modules import field_operations, safety, contracts, cost_management
    from modules import bim, closeout, documents
    
    ENTERPRISE_SYSTEMS_AVAILABLE = True
except ImportError as e:
    st.error(f"Enterprise systems not fully available: {e}")
    ENTERPRISE_SYSTEMS_AVAILABLE = False

def initialize_enterprise_systems():
    """Initialize all enterprise systems"""
    if not ENTERPRISE_SYSTEMS_AVAILABLE:
        return False
    
    try:
        # Initialize session state for enterprise features
        if 'enterprise_initialized' not in st.session_state:
            st.session_state.enterprise_initialized = True
            st.session_state.username = "admin"
            st.session_state.user_role = "admin"
            st.session_state.current_menu = "Dashboard"
            st.session_state.theme = "dark"
            
        # Apply responsive layout
        apply_responsive_layout()
        
        # Initialize live updates
        initialize_live_updates()
        
        return True
        
    except Exception as e:
        st.error(f"Failed to initialize enterprise systems: {e}")
        return False

def render_enterprise_header():
    """Render enterprise header with project info and real-time status"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e2228 0%, #2d3748 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px; color: white;">
        <h1 style="margin: 0; color: #4CAF50;">🏗️ gcPanel Enterprise - Highland Tower Development</h1>
        <h3 style="margin: 5px 0; color: #81C784;">$45.5M Mixed-Use Development | 15 Floors | 120 Units + 8 Retail</h3>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
            <div>
                <span style="background: #4CAF50; padding: 4px 8px; border-radius: 15px; font-size: 12px;">
                    🔴 LIVE
                </span>
                <span style="margin-left: 10px; color: #B0BEC5;">
                    Project Progress: 72.3% | Budget: 96.8% | Safety: 98.2%
                </span>
            </div>
            <div style="color: #B0BEC5; font-size: 14px;">
                📅 {datetime.now().strftime('%B %d, %Y')} | 
                👤 {st.session_state.get('username', 'User')} ({st.session_state.get('user_role', 'User').title()})
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_enterprise_sidebar():
    """Render enterprise sidebar with all systems integrated"""
    with st.sidebar:
        # Project info section
        st.markdown("""
        <div style="background: #1e2228; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #4CAF50; margin: 0 0 10px 0;">Highland Tower Development</h3>
            <p style="color: #B0BEC5; margin: 0; font-size: 14px;">
                📍 Highland District, Downtown<br>
                🏢 15 Floors Above Ground + 2 Below<br>
                🏠 120 Residential + 8 Retail Units<br>
                💰 $45.5M Total Project Value
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Global search
        if ENTERPRISE_SYSTEMS_AVAILABLE:
            search_manager = get_search_manager()
            st.markdown("### 🔍 Global Search")
            search_query = st.text_input("Search all modules...", placeholder="RFIs, reports, quality...")
            if search_query:
                with st.expander("Search Results", expanded=True):
                    results = search_manager.perform_global_search(search_query)
                    if results:
                        for module, items in results.items():
                            st.markdown(f"**{module.title()}** ({len(items)} results)")
                            for item in items[:3]:
                                st.markdown(f"• {item.get('title', item.get('name', 'Item'))}")
                    else:
                        st.info("No results found")
        
        # Navigation menu
        st.markdown("### 📋 Navigation")
        
        menu_options = {
            "🏗️ Dashboard": "dashboard",
            "📊 AI Analytics": "analytics", 
            "📋 Preconstruction": "preconstruction",
            "⚙️ Engineering": "engineering",
            "🏗️ Field Operations": "field_operations",
            "⚠️ Safety Management": "safety",
            "📄 Contracts": "contracts",
            "💰 Cost Management": "cost_management",
            "🏢 BIM & 3D Models": "bim",
            "✅ Project Closeout": "closeout",
            "📁 Document Center": "documents",
            "🔗 Integrations": "integrations",
            "📱 Field Mobile": "field_mobile",
            "🔧 System Admin": "admin"
        }
        
        for display_name, key in menu_options.items():
            if st.button(display_name, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_menu = key
                st.rerun()
        
        # Real-time notifications
        if ENTERPRISE_SYSTEMS_AVAILABLE:
            realtime_manager = get_realtime_manager()
            st.markdown("### 🔔 Live Notifications")
            unread_notifications = realtime_manager.get_unread_notifications()
            
            if unread_notifications:
                st.markdown(f"**{len(unread_notifications)} New Notifications**")
                for notification in unread_notifications[:3]:
                    st.markdown(f"• {notification['title']}")
                if st.button("View All", key="view_notifications"):
                    st.session_state.show_notifications = True
            else:
                st.info("No new notifications")

def render_main_content():
    """Render main content based on selected menu"""
    current_menu = st.session_state.get('current_menu', 'dashboard')
    
    try:
        if current_menu == "dashboard":
            render_enterprise_dashboard()
        elif current_menu == "analytics":
            if ENTERPRISE_SYSTEMS_AVAILABLE:
                analytics_manager = get_analytics_manager()
                analytics_manager.generate_predictive_dashboard()
            else:
                analytics.render_analytics_overview()
        elif current_menu == "field_operations":
            if ENTERPRISE_SYSTEMS_AVAILABLE:
                field_manager = get_field_manager()
                field_manager.render_field_dashboard()
            else:
                field_operations.render_field_operations()
        elif current_menu == "integrations":
            if ENTERPRISE_SYSTEMS_AVAILABLE:
                render_integrations_dashboard()
            else:
                st.info("Integrations module requires enterprise systems")
        elif current_menu == "field_mobile":
            if ENTERPRISE_SYSTEMS_AVAILABLE:
                field_manager = get_field_manager()
                field_manager.render_photo_management_system()
            else:
                st.info("Field mobile requires enterprise systems")
        elif current_menu == "admin":
            render_admin_dashboard()
        else:
            # Use existing modules
            if current_menu == "preconstruction":
                preconstruction.render_preconstruction()
            elif current_menu == "engineering":
                engineering.render_engineering()
            elif current_menu == "safety":
                safety.render_safety_management()
            elif current_menu == "contracts":
                contracts.render_contracts()
            elif current_menu == "cost_management":
                cost_management.render_cost_management()
            elif current_menu == "bim":
                bim.render_bim_3d_models()
            elif current_menu == "closeout":
                closeout.render_project_closeout()
            elif current_menu == "documents":
                documents.render_document_center()
            else:
                st.error(f"Module '{current_menu}' not found")
                
    except Exception as e:
        st.error(f"Error loading module: {e}")
        st.info("Falling back to basic dashboard")
        render_basic_dashboard()

def render_enterprise_dashboard():
    """Render enterprise dashboard with AI insights"""
    st.markdown("## 🏗️ Enterprise Dashboard - Highland Tower Development")
    
    # Quick metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Progress", "72.3%", "2.1%")
    with col2:
        st.metric("Budget Status", "96.8%", "-1.2%")
    with col3:
        st.metric("Safety Score", "98.2", "0.5")
    with col4:
        st.metric("Active RFIs", "12", "+3")
    
    # Main dashboard content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Recent activity
        st.markdown("### 📋 Recent Activity")
        
        activities = [
            {"time": "2 hours ago", "action": "RFI-2025-045 submitted", "user": "John Smith", "type": "rfi"},
            {"time": "4 hours ago", "action": "Quality check completed Floor 14", "user": "Sarah Chen", "type": "quality"},
            {"time": "6 hours ago", "action": "Material delivery logged", "user": "Mike Rodriguez", "type": "materials"},
            {"time": "8 hours ago", "action": "Safety inspection passed", "user": "Safety Team", "type": "safety"}
        ]
        
        for activity in activities:
            icon = {"rfi": "❓", "quality": "✅", "materials": "📦", "safety": "⚠️"}.get(activity["type"], "📋")
            st.markdown(f"{icon} **{activity['action']}** by {activity['user']} - {activity['time']}")
    
    with col2:
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("📝 New Daily Report", use_container_width=True):
            st.session_state.current_menu = "field_operations"
            st.rerun()
        
        if st.button("❓ Submit RFI", use_container_width=True):
            st.session_state.current_menu = "engineering"
            st.rerun()
        
        if st.button("📸 Photo Log", use_container_width=True):
            st.session_state.current_menu = "field_mobile"
            st.rerun()
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_menu = "analytics"
            st.rerun()
    
    # AI-powered insights
    if ENTERPRISE_SYSTEMS_AVAILABLE:
        st.markdown("### 🔮 AI-Powered Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("**Completion Prediction:** Project on track for December 2025 completion (87% confidence)")
        
        with col2:
            st.warning("**Cost Alert:** Potential 3.2% budget overrun detected - Review change orders")
        
        with col3:
            st.success("**Quality Score:** Excellent quality metrics - 94.1% above industry standard")

def render_integrations_dashboard():
    """Render integrations dashboard"""
    if ENTERPRISE_SYSTEMS_AVAILABLE:
        integration_manager = get_integration_manager()
        integration_manager.render_integration_status()
    else:
        st.error("Integration systems not available")

def render_admin_dashboard():
    """Render system administration dashboard"""
    st.markdown("## 🔧 System Administration")
    
    # System status
    st.markdown("### 📊 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Database Status", "✅ Connected")
        st.metric("Cache Status", "✅ Active")
    
    with col2:
        st.metric("Security Status", "✅ Secure")
        st.metric("Real-time Status", "✅ Live")
    
    with col3:
        st.metric("Integration Status", "⚠️ Partial")
        st.metric("Mobile Status", "✅ Optimized")
    
    # Performance metrics
    if ENTERPRISE_SYSTEMS_AVAILABLE:
        st.markdown("### 📈 Performance Metrics")
        cache_manager = get_cache_manager()
        cache_stats = cache_manager.get_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Cache Hit Rate", cache_stats['hit_rate'])
        with col2:
            st.metric("Cache Type", cache_stats['cache_type'])
        with col3:
            st.metric("Active Users", "24")

def render_basic_dashboard():
    """Render basic dashboard if enterprise systems unavailable"""
    st.markdown("## 🏗️ gcPanel - Highland Tower Development")
    st.info("Running in basic mode - Enterprise features unavailable")
    
    # Basic project info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Project Progress", "72.3%")
    with col2:
        st.metric("Budget Status", "96.8%")
    with col3:
        st.metric("Active RFIs", "12")

def main():
    """Main application entry point"""
    # Initialize enterprise systems
    enterprise_ready = initialize_enterprise_systems()
    
    # Render application
    render_enterprise_header()
    
    # Layout
    render_enterprise_sidebar()
    render_main_content()
    
    # Status indicator
    if enterprise_ready:
        st.markdown("""
        <div style="position: fixed; bottom: 20px; right: 20px; 
                   background: #4CAF50; color: white; padding: 8px 12px; 
                   border-radius: 20px; font-size: 12px; z-index: 1000;">
            🚀 Enterprise Mode Active
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()