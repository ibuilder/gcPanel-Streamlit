"""
Enhanced Dashboard with Real Database Integration
Highland Tower Development - Enterprise Dashboard with Live Data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add database path to imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database.connection import (
        get_project_metrics, 
        get_daily_reports, 
        get_rfis, 
        get_submittals,
        get_project_info,
        initialize_database
    )
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

def render_enhanced_dashboard():
    """Render enhanced dashboard with real data integration"""
    
    st.markdown("## 🏗️ Highland Tower Development Dashboard")
    st.markdown("*$45.5M Mixed-Use Development - Real-Time Project Intelligence*")
    
    # Initialize database connection
    if DATABASE_AVAILABLE:
        db_connected = initialize_database()
    else:
        db_connected = False
    
    if db_connected:
        st.success("✅ Live Data Connected - Highland Tower Development")
        project_data = get_project_info()
        metrics = get_project_metrics()
    else:
        st.info("📊 Enterprise Demo Mode - Highland Tower Development")
        # Demo data for Highland Tower
        project_data = {
            'name': 'Highland Tower Development',
            'description': '$45.5M Mixed-Use Development - 120 Residential + 8 Retail Units',
            'contract_value': 45500000.00,
            'status': 'active'
        }
        metrics = {
            'total_rfis': 23,
            'total_submittals': 18,
            'total_reports': 45,
            'project_progress': 67.5,
            'budget_utilization': 58.3,
            'safety_days': 127
        }
    
    # Project Header
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### {project_data['name']}")
        st.markdown(f"**{project_data['description']}**")
        st.markdown(f"💰 Contract Value: ${project_data['contract_value']:,.2f}")
    
    with col2:
        st.metric("Project Status", project_data['status'].title())
        st.metric("Safety Record", f"{metrics['safety_days']} days")
    
    with col3:
        st.metric("Progress", f"{metrics['project_progress']:.1f}%")
        st.metric("Budget Used", f"{metrics['budget_utilization']:.1f}%")
    
    st.divider()
    
    # Key Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='margin: 0; font-size: 2.5em;'>{}</h2>
            <p style='margin: 5px 0 0 0; opacity: 0.9;'>Active RFIs</p>
        </div>
        """.format(metrics['total_rfis']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='margin: 0; font-size: 2.5em;'>{}</h2>
            <p style='margin: 5px 0 0 0; opacity: 0.9;'>Submittals</p>
        </div>
        """.format(metrics['total_submittals']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='margin: 0; font-size: 2.5em;'>{}</h2>
            <p style='margin: 5px 0 0 0; opacity: 0.9;'>Daily Reports</p>
        </div>
        """.format(metrics['total_reports']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;'>
            <h2 style='margin: 0; font-size: 2.5em;'>127</h2>
            <p style='margin: 5px 0 0 0; opacity: 0.9;'>Safety Days</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Project Progress Tracking")
        
        # Progress chart with real data structure
        progress_data = pd.DataFrame({
            'Phase': ['Foundation', 'Structure', 'Envelope', 'MEP', 'Finishes'],
            'Planned': [100, 85, 70, 45, 25],
            'Actual': [100, 88, 65, 40, 20],
            'Budget': [95, 82, 68, 42, 22]
        })
        
        fig_progress = px.bar(
            progress_data, 
            x='Phase', 
            y=['Planned', 'Actual', 'Budget'],
            title='Highland Tower Development Progress by Phase',
            barmode='group',
            color_discrete_map={
                'Planned': '#3366CC',
                'Actual': '#28A745', 
                'Budget': '#FD7E14'
            }
        )
        fig_progress.update_layout(
            template="plotly_white",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_progress, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Cost Performance")
        
        # Cost breakdown
        cost_data = pd.DataFrame({
            'Category': ['Labor', 'Materials', 'Equipment', 'Overhead'],
            'Budget': [18500000, 15200000, 7800000, 4000000],
            'Actual': [17800000, 14900000, 7600000, 3900000]
        })
        
        fig_cost = px.bar(
            cost_data,
            x='Category',
            y=['Budget', 'Actual'],
            title='Highland Tower Budget vs Actual Costs',
            barmode='group',
            color_discrete_map={'Budget': '#DC3545', 'Actual': '#28A745'}
        )
        fig_cost.update_layout(
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_cost, use_container_width=True)
    
    # Recent Activity Section
    st.divider()
    st.markdown("### 📋 Recent Project Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔧 Latest RFIs")
        if db_connected:
            rfis = get_rfis()[:5]  # Get latest 5 RFIs
            if rfis:
                for rfi in rfis:
                    with st.expander(f"RFI-{rfi.get('rfi_number', 'N/A')} - {rfi.get('subject', 'No Subject')[:50]}..."):
                        st.write(f"**Priority:** {rfi.get('priority', 'N/A').title()}")
                        st.write(f"**Status:** {rfi.get('status', 'N/A').title()}")
                        st.write(f"**Location:** {rfi.get('location', 'N/A')}")
                        st.write(f"**Submitted:** {rfi.get('created_at', 'N/A')}")
            else:
                st.info("No RFIs found. Create your first RFI in the RFIs module.")
        else:
            # Demo RFI data
            demo_rfis = [
                {"number": "2025-001", "subject": "Foundation reinforcement details", "priority": "high", "status": "open"},
                {"number": "2025-002", "subject": "HVAC ductwork routing clarification", "priority": "medium", "status": "pending"},
                {"number": "2025-003", "subject": "Elevator shaft dimensions", "priority": "medium", "status": "answered"}
            ]
            for rfi in demo_rfis:
                with st.expander(f"RFI-{rfi['number']} - {rfi['subject']}"):
                    st.write(f"**Priority:** {rfi['priority'].title()}")
                    st.write(f"**Status:** {rfi['status'].title()}")
                    st.write("**Location:** Level 14 - North Wing")
    
    with col2:
        st.markdown("#### 📄 Latest Submittals")
        if db_connected:
            submittals = get_submittals()[:5]  # Get latest 5 submittals
            if submittals:
                for submittal in submittals:
                    with st.expander(f"SUB-{submittal.get('submittal_number', 'N/A')} - {submittal.get('title', 'No Title')[:50]}..."):
                        st.write(f"**Status:** {submittal.get('status', 'N/A').title()}")
                        st.write(f"**Priority:** {submittal.get('priority', 'N/A').title()}")
                        st.write(f"**Contractor:** {submittal.get('contractor_name', 'N/A')}")
                        st.write(f"**Due Date:** {submittal.get('due_date', 'N/A')}")
            else:
                st.info("No submittals found. Create your first submittal in the Submittals module.")
        else:
            # Demo submittal data
            demo_submittals = [
                {"number": "SUB-001", "title": "Steel Beam Specifications", "status": "approved", "contractor": "Highland Steel Co."},
                {"number": "SUB-002", "title": "Window Installation Details", "status": "under_review", "contractor": "Premium Windows LLC"},
                {"number": "SUB-003", "title": "Concrete Mix Design", "status": "submitted", "contractor": "Metro Concrete"}
            ]
            for submittal in demo_submittals:
                with st.expander(f"SUB-{submittal['number']} - {submittal['title']}"):
                    st.write(f"**Status:** {submittal['status'].replace('_', ' ').title()}")
                    st.write(f"**Contractor:** {submittal['contractor']}")
                    st.write("**Specification:** 05 12 00 - Structural Steel")
    
    # Quick Actions
    st.divider()
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 New Daily Report", type="secondary", use_container_width=True):
            st.session_state.current_menu = "Field Operations"
            st.rerun()
    
    with col2:
        if st.button("❓ Submit RFI", type="secondary", use_container_width=True):
            st.session_state.current_menu = "RFIs"
            st.rerun()
    
    with col3:
        if st.button("📄 New Submittal", type="secondary", use_container_width=True):
            st.session_state.current_menu = "Submittals"
            st.rerun()
    
    with col4:
        if st.button("📊 View Analytics", type="secondary", use_container_width=True):
            st.session_state.current_menu = "Analytics"
            st.rerun()

def render():
    """Main render function for the enhanced dashboard"""
    render_enhanced_dashboard()