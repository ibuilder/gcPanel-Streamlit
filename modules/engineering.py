"""
Engineering Module for gcPanel Highland Tower Development
Advanced engineering management for the $45.5M mixed-use development
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render():
    """Render the comprehensive Engineering module"""
    
    st.markdown("""
    <div class="enterprise-header">
        <h1>⚙️ Engineering Management</h1>
        <p>Highland Tower Development - Technical Engineering Solutions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Engineering tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 RFIs", "🏗️ Structural", "⚡ MEP Systems", "🧪 Materials Testing", "📊 Engineering Analytics"])
    
    with tab1:
        render_rfis()
    
    with tab2:
        render_structural()
    
    with tab3:
        render_mep_systems()
    
    with tab4:
        render_materials_testing()
    
    with tab5:
        render_engineering_analytics()

def render_rfis():
    """Render RFI management interface"""
    st.markdown("### Request for Information (RFI) Management")
    
    # RFI overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Open RFIs", "23", "+3 this week")
    with col2:
        st.metric("Avg Response Time", "2.1 days", "-0.3 days")
    with col3:
        st.metric("Critical RFIs", "4", "⚠️")
    with col4:
        st.metric("RFIs This Month", "15", "+5 from last month")
    
    # Create new RFI
    with st.expander("📝 Create New RFI", expanded=False):
        with st.form("new_rfi"):
            col1, col2 = st.columns(2)
            
            with col1:
                rfi_subject = st.text_input("Subject*", placeholder="Foundation reinforcement details - Level B2")
                rfi_location = st.selectbox("Location", [
                    "Level B2 - Parking", "Level B1 - Retail Prep", "Ground Floor - Retail",
                    "Levels 2-5 - Residential", "Levels 6-10 - Residential", 
                    "Levels 11-15 - Residential", "Roof Level", "Mechanical Penthouse"
                ])
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                discipline = st.selectbox("Engineering Discipline", [
                    "Structural", "Mechanical", "Electrical", "Plumbing", 
                    "Civil", "Geotechnical", "Architectural"
                ])
            
            with col2:
                submitter = st.text_input("Submitted By", value="Highland Tower Engineering")
                due_date = st.date_input("Response Due Date", datetime.now() + timedelta(days=7))
                assign_to = st.selectbox("Assign To", [
                    "Sarah Chen, PE - Structural Engineer",
                    "David Kim - MEP Engineer", 
                    "Jennifer Walsh, AIA - Project Manager",
                    "Highland Structural Consultants",
                    "MEP Engineering Associates"
                ])
                cost_impact = st.selectbox("Potential Cost Impact", ["None", "Low ($0-$5K)", "Medium ($5K-$25K)", "High ($25K+)"])
            
            description = st.text_area("Detailed Description*", height=120, 
                placeholder="Describe the engineering question or clarification needed...")
            
            uploaded_files = st.file_uploader("Attach Files", accept_multiple_files=True, 
                type=['pdf', 'dwg', 'jpg', 'png', 'xlsx'])
            
            if st.form_submit_button("Submit RFI", type="primary"):
                if rfi_subject and description:
                    rfi_number = f"HTD-RFI-{datetime.now().strftime('%Y%m%d')}-{np.random.randint(100, 999)}"
                    st.success(f"✅ RFI submitted successfully! Reference: {rfi_number}")
                    st.info("📧 Notifications sent to assigned engineer and project team")
                else:
                    st.error("Please fill in all required fields (*)")
    
    # Active RFIs
    st.markdown("#### Active Highland Tower RFIs")
    
    rfi_data = {
        'RFI #': ['HTD-RFI-001', 'HTD-RFI-002', 'HTD-RFI-003', 'HTD-RFI-004', 'HTD-RFI-005'],
        'Subject': [
            'Foundation anchorage details - Level B2',
            'HVAC ductwork routing - Level 8',
            'Structural beam connection - Level 12',
            'Electrical panel location - Retail',
            'Waterproofing detail - Roof level'
        ],
        'Discipline': ['Structural', 'Mechanical', 'Structural', 'Electrical', 'Civil'],
        'Priority': ['High', 'Medium', 'Critical', 'Low', 'Medium'],
        'Status': ['Open', 'In Review', 'Answered', 'Open', 'In Review'],
        'Assigned To': ['Sarah Chen, PE', 'David Kim', 'Sarah Chen, PE', 'Highland Electrical', 'Jennifer Walsh'],
        'Due Date': ['2025-01-30', '2025-01-28', '2025-01-27', '2025-02-02', '2025-01-29'],
        'Days Open': [5, 3, 1, 8, 4]
    }
    
    df_rfis = pd.DataFrame(rfi_data)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_discipline = st.selectbox("Filter by Discipline", ["All", "Structural", "Mechanical", "Electrical", "Civil"])
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "Critical", "High", "Medium", "Low"])
    with col3:
        filter_status = st.selectbox("Filter by Status", ["All", "Open", "In Review", "Answered", "Closed"])
    
    # Display RFIs
    for index, rfi in df_rfis.iterrows():
        priority_color = {
            'Critical': '🔴',
            'High': '🟠', 
            'Medium': '🟡',
            'Low': '🟢'
        }
        
        with st.expander(f"{priority_color[rfi['Priority']]} {rfi['RFI #']} - {rfi['Subject']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Discipline:** {rfi['Discipline']}")
                st.markdown(f"**Priority:** {rfi['Priority']}")
                st.markdown(f"**Status:** {rfi['Status']}")
            
            with col2:
                st.markdown(f"**Assigned To:** {rfi['Assigned To']}")
                st.markdown(f"**Due Date:** {rfi['Due Date']}")
                st.markdown(f"**Days Open:** {rfi['Days Open']}")
            
            with col3:
                if st.button(f"📝 Update Status", key=f"update_{rfi['RFI #']}"):
                    st.success("RFI status updated")
                if st.button(f"📎 View Details", key=f"details_{rfi['RFI #']}"):
                    st.info("Opening detailed RFI view...")

def render_engineering_coordination():
    """Render engineering coordination interface - streamlined without duplicate drawing management"""
    st.markdown("### Engineering Coordination")
    
    # Quick navigation to Documents for drawing management
    st.info("📐 **Drawing Management** is available in the **Documents** section for comprehensive document control and version management.")
    
    # Engineering coordination metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active RFIs", "23", "+3 this week")
    with col2:
        st.metric("Structural Progress", "85%", "Level 13 complete")
    with col3:
        st.metric("MEP Coordination", "68%", "On schedule")
    with col4:
        st.metric("Engineering Issues", "12", "-3 resolved")
    
    # Quick coordination actions
    st.markdown("#### Quick Engineering Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Create New RFI", use_container_width=True):
            st.success("RFI creation form opened")
    
    with col2:
        if st.button("🔍 View Active Issues", use_container_width=True):
            st.info("Opening engineering issues dashboard")
    
    with col3:
        if st.button("📊 Coordination Report", use_container_width=True):
            st.info("Generating MEP coordination report")

def render_structural():
    """Render structural engineering interface"""
    st.markdown("### Structural Engineering")
    
    # Structural overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Steel Tonnage", "2,847 tons", "95% delivered")
    with col2:
        st.metric("Concrete Volume", "12,450 CY", "78% poured")
    with col3:
        st.metric("Open Issues", "12", "-3 this week")
    with col4:
        st.metric("Inspections", "89% passed", "✅")
    
    # Structural progress by level
    st.markdown("#### Construction Progress by Level")
    
    level_data = {
        'Level': ['Level B2', 'Level B1', 'Ground', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 
                 'Level 6', 'Level 7', 'Level 8', 'Level 9', 'Level 10', 'Level 11', 'Level 12', 
                 'Level 13', 'Level 14', 'Level 15', 'Roof'],
        'Concrete (%)': [100, 100, 100, 100, 100, 95, 85, 75, 60, 45, 30, 15, 5, 0, 0, 0, 0, 0],
        'Steel (%)': [100, 100, 100, 100, 100, 100, 95, 90, 85, 70, 55, 40, 25, 10, 0, 0, 0, 0],
        'MEP Rough-in (%)': [100, 100, 95, 90, 85, 75, 60, 45, 30, 15, 5, 0, 0, 0, 0, 0, 0, 0]
    }
    
    df_levels = pd.DataFrame(level_data)
    
    fig_progress = px.bar(
        df_levels, 
        x='Level', 
        y=['Concrete (%)', 'Steel (%)', 'MEP Rough-in (%)'],
        title='Highland Tower Structural Progress by Level',
        barmode='group',
        color_discrete_map={
            'Concrete (%)': '#6366f1',
            'Steel (%)': '#ef4444', 
            'MEP Rough-in (%)': '#10b981'
        }
    )
    fig_progress.update_layout(height=400)
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # Structural issues
    st.markdown("#### Active Structural Issues")
    
    structural_issues = [
        {
            "issue": "Beam connection detail revision - Level 12",
            "priority": "High",
            "status": "In Progress", 
            "assigned": "Sarah Chen, PE",
            "due_date": "2025-01-30"
        },
        {
            "issue": "Foundation reinforcement verification - Level B2",
            "priority": "Medium",
            "status": "Under Review",
            "assigned": "Highland Structural",
            "due_date": "2025-02-01"
        },
        {
            "issue": "Post-tensioning sequence - Level 8",
            "priority": "Low",
            "status": "Open",
            "assigned": "Sarah Chen, PE", 
            "due_date": "2025-02-05"
        }
    ]
    
    for issue in structural_issues:
        priority_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        
        with st.expander(f"{priority_colors[issue['priority']]} {issue['issue']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Priority:** {issue['priority']}")
                st.markdown(f"**Status:** {issue['status']}")
                st.markdown(f"**Assigned:** {issue['assigned']}")
            
            with col2:
                st.markdown(f"**Due Date:** {issue['due_date']}")
                if st.button("📝 Update", key=f"update_{issue['issue'][:20]}"):
                    st.success("Issue updated")

def render_mep_systems():
    """Render MEP systems interface"""
    st.markdown("### MEP Engineering Systems")
    
    # MEP overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("HVAC Progress", "68%", "+5% this week")
    with col2:
        st.metric("Electrical Rough-in", "72%", "+8% this week")
    with col3:
        st.metric("Plumbing Systems", "65%", "+3% this week")
    with col4:
        st.metric("Fire Protection", "58%", "+7% this week")
    
    # MEP system tabs
    mep_tab1, mep_tab2, mep_tab3, mep_tab4 = st.tabs(["🌡️ HVAC", "⚡ Electrical", "🚿 Plumbing", "🚨 Fire Protection"])
    
    with mep_tab1:
        st.markdown("#### HVAC System Status")
        
        hvac_data = {
            'Zone': ['Retail Ground Floor', 'Residential Floors 2-5', 'Residential Floors 6-10', 
                    'Residential Floors 11-15', 'Mechanical Penthouse'],
            'Equipment Status': ['Installed', 'Rough-in Complete', 'In Progress', 'Scheduled', 'Installed'],
            'Ductwork (%)': [95, 85, 60, 25, 90],
            'Controls (%)': [80, 70, 40, 10, 85],
            'Testing (%)': [60, 45, 20, 0, 70]
        }
        
        df_hvac = pd.DataFrame(hvac_data)
        st.dataframe(df_hvac, use_container_width=True)
        
        st.markdown("**HVAC Equipment Schedule:**")
        st.markdown("• Air Handling Units: 8 of 12 installed")
        st.markdown("• Rooftop Units: 6 of 8 installed")  
        st.markdown("• Heat Pumps: 45 of 60 installed")
        st.markdown("• Variable Air Volume Boxes: 180 of 240 installed")
    
    with mep_tab2:
        st.markdown("#### Electrical System Status")
        
        electrical_data = {
            'System': ['Main Service', 'Distribution Panels', 'Branch Circuits', 'Lighting', 'Emergency Power'],
            'Design (%)': [100, 100, 95, 90, 100],
            'Installation (%)': [95, 85, 70, 60, 80],
            'Testing (%)': [80, 60, 40, 30, 70]
        }
        
        df_electrical = pd.DataFrame(electrical_data)
        
        fig_electrical = px.bar(
            df_electrical,
            x='System',
            y=['Design (%)', 'Installation (%)', 'Testing (%)'],
            title='Electrical Systems Progress',
            barmode='group'
        )
        st.plotly_chart(fig_electrical, use_container_width=True)
    
    with mep_tab3:
        st.markdown("#### Plumbing System Status")
        
        plumbing_systems = [
            {"system": "Domestic Water", "progress": 75, "status": "On Track"},
            {"system": "Sanitary Waste", "progress": 68, "status": "On Track"},
            {"system": "Storm Drainage", "progress": 82, "status": "Ahead"},
            {"system": "Natural Gas", "progress": 45, "status": "Behind"}
        ]
        
        for system in plumbing_systems:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{system['system']}**")
                st.progress(system['progress'] / 100)
            
            with col2:
                st.markdown(f"{system['progress']}%")
            
            with col3:
                status_colors = {"On Track": "🟢", "Ahead": "🔵", "Behind": "🟡"}
                st.markdown(f"{status_colors[system['status']]} {system['status']}")
    
    with mep_tab4:
        st.markdown("#### Fire Protection System")
        
        fire_protection = {
            'Component': ['Sprinkler System', 'Fire Alarm', 'Smoke Control', 'Emergency Lighting', 'Fire Pumps'],
            'Installation (%)': [65, 70, 45, 80, 90],
            'Testing (%)': [40, 50, 20, 60, 85],
            'Approval Status': ['Pending', 'Approved', 'Under Review', 'Approved', 'Approved']
        }
        
        df_fire = pd.DataFrame(fire_protection)
        st.dataframe(df_fire, use_container_width=True)

def render_materials_testing():
    """Render materials testing interface"""
    st.markdown("### Materials Testing & Quality Control")
    
    # Testing overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Concrete Tests", "247", "23 this week")
    with col2:
        st.metric("Steel Inspections", "156", "98% passed")
    with col3:
        st.metric("Soil Tests", "89", "All passed")
    with col4:
        st.metric("Material Certifications", "445", "Current")
    
    # Recent test results
    st.markdown("#### Recent Test Results")
    
    test_data = {
        'Test Date': ['2025-01-27', '2025-01-26', '2025-01-25', '2025-01-24', '2025-01-23'],
        'Material': ['Concrete - Level 8', 'Steel Rebar - Level 9', 'Concrete - Level 7', 'Soil Compaction', 'Concrete - Level 8'],
        'Test Type': ['Compressive Strength', 'Tensile Test', 'Compressive Strength', 'Proctor Test', 'Slump Test'],
        'Result': ['4,850 psi', '68,500 psi', '4,920 psi', '96% Standard Proctor', '4.5 inches'],
        'Specification': ['4,500 psi min', '60,000 psi min', '4,500 psi min', '95% min', '4±1 inches'],
        'Status': ['✅ Pass', '✅ Pass', '✅ Pass', '✅ Pass', '✅ Pass'],
        'Lab': ['Highland Testing', 'Highland Testing', 'Highland Testing', 'Geotechnical Associates', 'Highland Testing']
    }
    
    df_tests = pd.DataFrame(test_data)
    st.dataframe(df_tests, use_container_width=True)
    
    # Schedule new test
    with st.expander("📋 Schedule New Material Test", expanded=False):
        with st.form("schedule_test"):
            col1, col2 = st.columns(2)
            
            with col1:
                material_type = st.selectbox("Material Type", [
                    "Concrete", "Steel Rebar", "Structural Steel", "Soil", 
                    "Masonry", "Welding", "Fireproofing"
                ])
                test_type = st.selectbox("Test Type", [
                    "Compressive Strength", "Tensile Test", "Slump Test",
                    "Air Content", "Proctor Test", "Ultrasonic Testing"
                ])
                location = st.text_input("Location", placeholder="Level 8 - Column Grid A-5")
            
            with col2:
                test_date = st.date_input("Scheduled Test Date", datetime.now() + timedelta(days=1))
                lab = st.selectbox("Testing Lab", [
                    "Highland Testing Laboratory",
                    "Metropolitan Materials Testing",
                    "Geotechnical Associates"
                ])
                priority = st.selectbox("Priority", ["Standard", "Rush", "Critical"])
            
            special_instructions = st.text_area("Special Instructions", 
                placeholder="Any special testing requirements or instructions...")
            
            if st.form_submit_button("Schedule Test", type="primary"):
                test_id = f"HTD-TEST-{datetime.now().strftime('%Y%m%d')}-{np.random.randint(100, 999)}"
                st.success(f"✅ Test scheduled successfully! ID: {test_id}")
                st.info(f"📧 Notification sent to {lab}")

def render_engineering_analytics():
    """Render engineering analytics dashboard"""
    st.markdown("### Engineering Analytics Dashboard")
    
    # Analytics overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### RFI Trends")
        
        # Generate RFI trend data
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        rfis_opened = [8, 12, 15, 10]
        rfis_closed = [6, 10, 13, 12]
        
        fig_rfi = go.Figure()
        fig_rfi.add_trace(go.Scatter(x=weeks, y=rfis_opened, name='Opened', line=dict(color='#ef4444')))
        fig_rfi.add_trace(go.Scatter(x=weeks, y=rfis_closed, name='Closed', line=dict(color='#10b981')))
        fig_rfi.update_layout(title='RFI Activity Trends', height=300)
        st.plotly_chart(fig_rfi, use_container_width=True)
    
    with col2:
        st.markdown("#### Discipline Breakdown")
        
        disciplines = ['Structural', 'Mechanical', 'Electrical', 'Plumbing', 'Civil']
        rfi_counts = [12, 8, 6, 4, 3]
        
        fig_disciplines = px.pie(
            values=rfi_counts, 
            names=disciplines,
            title='RFIs by Discipline'
        )
        fig_disciplines.update_layout(height=300)
        st.plotly_chart(fig_disciplines, use_container_width=True)
    
    with col3:
        st.markdown("#### Response Time Analysis")
        
        response_data = {
            'Priority': ['Critical', 'High', 'Medium', 'Low'],
            'Avg Response (days)': [0.5, 1.2, 2.1, 3.8],
            'Target (days)': [0.5, 1.0, 2.0, 5.0]
        }
        
        df_response = pd.DataFrame(response_data)
        
        fig_response = px.bar(
            df_response,
            x='Priority',
            y=['Avg Response (days)', 'Target (days)'],
            title='RFI Response Times',
            barmode='group'
        )
        fig_response.update_layout(height=300)
        st.plotly_chart(fig_response, use_container_width=True)
    
    # Engineering productivity metrics
    st.markdown("#### Engineering Productivity Metrics")
    
    productivity_data = {
        'Metric': ['Drawing Production', 'RFI Resolution', 'Design Changes', 'Quality Score', 'Schedule Performance'],
        'This Week': [15, 12, 3, 94, 98],
        'Last Week': [12, 10, 5, 92, 95],
        'Target': [18, 15, 2, 95, 100],
        'Trend': ['↗️', '↗️', '↘️', '↗️', '↗️']
    }
    
    df_productivity = pd.DataFrame(productivity_data)
    st.dataframe(df_productivity, use_container_width=True)

if __name__ == "__main__":
    render()