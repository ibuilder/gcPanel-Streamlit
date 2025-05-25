"""
Building Inspections Module
Highland Tower Development - Inspection Scheduling and Results
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render():
    """Render the Building Inspections module"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">
            📊 Building Inspections
        </h1>
        <p style="color: #e8f4fd; margin: 1rem 0 0 0; font-size: 1.2rem;">
            Highland Tower Development - Inspection Management
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📅 Schedule Inspection", type="primary", use_container_width=True):
            st.session_state.show_schedule = True
    
    with col2:
        if st.button("📋 View Results", use_container_width=True):
            st.session_state.show_results = True
    
    with col3:
        if st.button("📊 Inspection Report", use_container_width=True):
            st.session_state.show_report = True
    
    with col4:
        if st.button("⚠️ Failed Inspections", use_container_width=True):
            st.session_state.show_failed = True
    
    # Highland Tower Inspection Overview
    st.markdown("### 🏗️ Highland Tower Inspection Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Pass Rate", "96.2%", "+2.1%")
    
    with col2:
        st.metric("This Month", "24 Inspections", "+6")
    
    with col3:
        st.metric("Pending", "3 Inspections", "This week")
    
    with col4:
        st.metric("Re-inspections", "2 Required", "-1")
    
    # Recent and upcoming inspections
    tab1, tab2, tab3 = st.tabs(["📅 Upcoming Inspections", "📋 Recent Results", "📊 Inspection Analytics"])
    
    with tab1:
        render_upcoming_inspections()
    
    with tab2:
        render_recent_results()
    
    with tab3:
        render_inspection_analytics()

def render_upcoming_inspections():
    """Render upcoming scheduled inspections"""
    
    st.markdown("### 📅 Highland Tower Upcoming Inspections")
    
    upcoming_data = pd.DataFrame([
        {
            "Date": "2025-01-27",
            "Time": "9:00 AM",
            "Type": "Final Electrical",
            "Floor/Area": "Level 12 - Residential",
            "Inspector": "City Electrical Dept",
            "Prep Status": "Ready",
            "Contact": "Lisa Chen"
        },
        {
            "Date": "2025-01-28", 
            "Time": "2:00 PM",
            "Type": "MEP Rough-in",
            "Floor/Area": "Level 14 - Residential", 
            "Inspector": "Building Department",
            "Prep Status": "In Progress",
            "Contact": "Alex Rodriguez"
        },
        {
            "Date": "2025-01-30",
            "Time": "10:30 AM", 
            "Type": "Fire Safety Systems",
            "Floor/Area": "Basement Levels 1-2",
            "Inspector": "Fire Marshal",
            "Prep Status": "Scheduled",
            "Contact": "Mike Johnson"
        },
        {
            "Date": "2025-02-03",
            "Time": "1:00 PM",
            "Type": "Structural Frame", 
            "Floor/Area": "Level 15 - Penthouse",
            "Inspector": "Structural Engineer",
            "Prep Status": "Pending",
            "Contact": "Sarah Davis"
        }
    ])
    
    for idx, inspection in upcoming_data.iterrows():
        # Color code based on prep status
        if inspection['Prep Status'] == "Ready":
            status_color = "#28a745"
            status_icon = "✅"
        elif inspection['Prep Status'] == "In Progress":
            status_color = "#ffc107"
            status_icon = "🔄"
        else:
            status_color = "#6c757d"
            status_icon = "⏳"
        
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 2, 1])
            
            with col1:
                st.markdown(f"**{inspection['Type']}**")
                st.caption(f"{inspection['Date']} at {inspection['Time']}")
            
            with col2:
                st.write(inspection['Floor/Area'])
            
            with col3:
                st.write(f"Inspector: {inspection['Inspector']}")
                st.caption(f"Contact: {inspection['Contact']}")
            
            with col4:
                st.markdown(f"""
                <div style="color: {status_color}; font-weight: bold;">
                    {status_icon} {inspection['Prep Status']}
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                if st.button("📝", key=f"edit_inspection_{idx}", help="Edit inspection"):
                    st.info(f"Editing {inspection['Type']} inspection")
        
        st.markdown("---")

def render_recent_results():
    """Render recent inspection results"""
    
    st.markdown("### 📋 Highland Tower Recent Inspection Results")
    
    results_data = pd.DataFrame([
        {
            "Date": "2025-01-24",
            "Type": "Plumbing Rough-in",
            "Floor/Area": "Level 11 - Residential",
            "Result": "Pass",
            "Score": "98%",
            "Inspector": "City Plumbing Dept",
            "Notes": "Excellent workmanship, no issues found"
        },
        {
            "Date": "2025-01-22",
            "Type": "HVAC Installation", 
            "Floor/Area": "Level 10 - Residential",
            "Result": "Pass",
            "Score": "95%",
            "Inspector": "HVAC Inspector",
            "Notes": "Minor documentation update needed"
        },
        {
            "Date": "2025-01-20",
            "Type": "Concrete Pour",
            "Floor/Area": "Level 13 - Slab",
            "Result": "Fail", 
            "Score": "78%",
            "Inspector": "Structural Inspector",
            "Notes": "Surface finish requires attention - re-inspection scheduled"
        },
        {
            "Date": "2025-01-18",
            "Type": "Electrical Panel",
            "Floor/Area": "Main Electrical Room",
            "Result": "Pass",
            "Score": "100%",
            "Inspector": "City Electrical Dept", 
            "Notes": "Perfect installation, ahead of schedule"
        }
    ])
    
    for idx, result in results_data.iterrows():
        # Color code based on result
        if result['Result'] == "Pass":
            result_color = "#28a745"
            result_icon = "✅"
        else:
            result_color = "#dc3545"
            result_icon = "❌"
        
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 1, 3])
            
            with col1:
                st.markdown(f"**{result['Type']}**")
                st.caption(f"{result['Date']} • {result['Floor/Area']}")
            
            with col2:
                st.write(f"Inspector: {result['Inspector']}")
                st.caption(f"Score: {result['Score']}")
            
            with col3:
                st.markdown(f"""
                <div style="color: {result_color}; font-weight: bold; text-align: center;">
                    {result_icon}<br>{result['Result']}
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.write(f"**Notes:** {result['Notes']}")
        
        st.markdown("---")

def render_inspection_analytics():
    """Render inspection analytics and trends"""
    
    st.markdown("### 📊 Highland Tower Inspection Analytics")
    
    # Monthly inspection trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Monthly Pass Rates")
        months = ["Sep", "Oct", "Nov", "Dec", "Jan"]
        pass_rates = [94.2, 95.1, 96.8, 95.5, 96.2]
        
        chart_data = pd.DataFrame({
            "Month": months,
            "Pass Rate": pass_rates
        })
        st.line_chart(chart_data.set_index("Month"))
    
    with col2:
        st.markdown("#### 📊 Inspection Types Breakdown")
        inspection_types = pd.DataFrame({
            "Type": ["Electrical", "Plumbing", "HVAC", "Structural", "Fire Safety"],
            "Count": [45, 38, 32, 28, 15]
        })
        st.bar_chart(inspection_types.set_index("Type"))
    
    # Inspector performance
    st.markdown("#### 👨‍🔧 Inspector Performance Summary")
    
    inspector_data = pd.DataFrame([
        {
            "Inspector": "City Electrical Dept",
            "Inspections": 45,
            "Pass Rate": "97.8%",
            "Avg Response Time": "2.1 days",
            "Rating": "⭐⭐⭐⭐⭐"
        },
        {
            "Inspector": "Building Department", 
            "Inspections": 38,
            "Pass Rate": "94.7%",
            "Avg Response Time": "3.2 days",
            "Rating": "⭐⭐⭐⭐"
        },
        {
            "Inspector": "Fire Marshal",
            "Inspections": 15,
            "Pass Rate": "100%",
            "Avg Response Time": "1.8 days", 
            "Rating": "⭐⭐⭐⭐⭐"
        }
    ])
    
    st.dataframe(inspector_data, use_container_width=True, hide_index=True)
    
    # Common inspection issues
    st.markdown("#### ⚠️ Common Issues Identified")
    
    issues_data = pd.DataFrame([
        {"Issue": "Documentation incomplete", "Frequency": 12, "Resolution": "Template provided"},
        {"Issue": "Surface finish quality", "Frequency": 8, "Resolution": "Additional QC checks"},
        {"Issue": "Code compliance clarification", "Frequency": 5, "Resolution": "Updated procedures"},
        {"Issue": "Material certification missing", "Frequency": 3, "Resolution": "Vendor requirements updated"}
    ])
    
    st.dataframe(issues_data, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    render()