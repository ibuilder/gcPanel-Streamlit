"""
Highland Tower Development - Daily Reports UI
Enterprise frontend interface for the daily reports backend system.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any

# Import the backend
from modules.daily_reports_backend import (
    daily_reports_manager, 
    DailyReport, 
    ReportStatus, 
    WeatherCondition,
    WorkActivity,
    SafetyIncident,
    MaterialDelivery
)

def render_daily_reports_enterprise():
    """Render the enterprise daily reports interface with backend integration"""
    
    st.markdown("""
    <div class="module-header">
        <h1>📋 Daily Reports Management</h1>
        <p>Highland Tower Development - Enterprise reporting system with data persistence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display summary metrics
    render_summary_metrics()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Reports Overview", 
        "➕ Create New Report", 
        "📈 Analytics", 
        "⚙️ Management"
    ])
    
    with tab1:
        render_reports_overview()
    
    with tab2:
        render_create_report_form()
    
    with tab3:
        render_analytics_dashboard()
    
    with tab4:
        render_management_tools()

def render_summary_metrics():
    """Display key metrics from the backend"""
    stats = daily_reports_manager.generate_summary_stats()
    
    if not stats:
        st.info("No reports available. Create your first daily report to see metrics.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Reports",
            value=stats['total_reports'],
            delta=f"Latest: {stats['latest_report_date']}"
        )
    
    with col2:
        st.metric(
            label="👥 Total Crew Hours", 
            value=f"{stats['total_crew_hours']:,.0f}",
            delta=f"Avg crew: {stats['average_crew_size']}"
        )
    
    with col3:
        approved_count = stats['status_breakdown'].get('Approved', 0)
        st.metric(
            label="✅ Approved Reports",
            value=approved_count,
            delta=f"{(approved_count/stats['total_reports']*100):.0f}% approval rate"
        )
    
    with col4:
        draft_count = stats['status_breakdown'].get('Draft', 0)
        st.metric(
            label="📝 Draft Reports",
            value=draft_count,
            delta="Pending completion"
        )

def render_reports_overview():
    """Display all reports with filtering and management options"""
    st.subheader("📋 All Daily Reports")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            options=["All"] + [status.value for status in ReportStatus],
            key="status_filter"
        )
    
    with col2:
        date_from = st.date_input("From Date", key="date_from")
    
    with col3:
        date_to = st.date_input("To Date", value=date.today(), key="date_to")
    
    # Get filtered reports
    reports = daily_reports_manager.get_all_reports()
    
    if status_filter != "All":
        reports = [r for r in reports if r.status.value == status_filter]
    
    if date_from and date_to:
        reports = [r for r in reports if date_from.isoformat() <= r.date <= date_to.isoformat()]
    
    if not reports:
        st.info("No reports match your filter criteria.")
        return
    
    # Display reports
    for report in reports:
        render_report_card(report)

def render_report_card(report: DailyReport):
    """Render a single report card with actions"""
    status_color = {
        ReportStatus.DRAFT: "🟡",
        ReportStatus.SUBMITTED: "🔵", 
        ReportStatus.APPROVED: "🟢",
        ReportStatus.REVISION_REQUIRED: "🟠"
    }
    
    with st.expander(
        f"{status_color.get(report.status, '⚪')} {report.date} | {report.weather.value} | Crew: {report.crew_size}",
        expanded=False
    ):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**📊 Status:** {report.status.value}")
            st.write(f"**🌤️ Weather:** {report.weather.value} ({report.temperature}°F)")
            st.write(f"**👥 Crew Size:** {report.crew_size} workers")
            st.write(f"**⏱️ Work Hours:** {report.work_hours} hours")
            st.write(f"**👤 Created by:** {report.created_by}")
            
            if report.work_summary:
                st.write(f"**📝 Summary:** {report.work_summary}")
            
            # Show work activities
            if report.work_activities:
                st.write("**🔨 Work Activities:**")
                for activity in report.work_activities:
                    st.write(f"• {activity.description} ({activity.progress_percentage}% complete)")
            
            # Show safety incidents
            if report.safety_incidents:
                st.write("**⚠️ Safety Incidents:**")
                for incident in report.safety_incidents:
                    st.write(f"• {incident.description} (Severity: {incident.severity})")
            
            # Show deliveries
            if report.material_deliveries:
                st.write("**🚚 Material Deliveries:**")
                for delivery in report.material_deliveries:
                    st.write(f"• {delivery.material_type} from {delivery.supplier}")
        
        with col2:
            st.write("**Actions:**")
            
            if st.button(f"📄 View Details", key=f"view_{report.report_id}"):
                st.session_state.selected_report = report.report_id
                st.info("Report details would open in modal/detailed view")
            
            if st.button(f"✏️ Edit", key=f"edit_{report.report_id}"):
                st.session_state.edit_report = report.report_id
                st.info("Edit mode activated")
            
            if report.status == ReportStatus.DRAFT:
                if st.button(f"📤 Submit", key=f"submit_{report.report_id}"):
                    daily_reports_manager.update_report(
                        report.report_id, 
                        {'status': ReportStatus.SUBMITTED}
                    )
                    st.success("Report submitted for approval!")
                    st.rerun()
            
            if st.button(f"🗑️ Delete", key=f"delete_{report.report_id}"):
                if daily_reports_manager.delete_report(report.report_id):
                    st.success("Report deleted!")
                    st.rerun()

def render_create_report_form():
    """Render the create new report form"""
    st.subheader("➕ Create New Daily Report")
    
    with st.form("new_report_form", clear_on_submit=True):
        # Basic info
        col1, col2 = st.columns(2)
        
        with col1:
            report_date = st.date_input("Report Date", value=date.today())
            weather = st.selectbox(
                "Weather Condition",
                options=[w.value for w in WeatherCondition]
            )
            temperature = st.number_input("Temperature (°F)", value=72, min_value=-50, max_value=150)
        
        with col2:
            crew_size = st.number_input("Crew Size", value=1, min_value=1, max_value=100)
            work_hours = st.number_input("Work Hours", value=8.0, min_value=0.1, max_value=24.0, step=0.5)
            created_by = st.text_input("Created By", value="Site Manager")
        
        # Work summary
        st.markdown("### 📝 Work Summary")
        work_summary = st.text_area("Work Summary", height=100)
        challenges = st.text_area("Challenges Encountered", height=80)
        next_day_plan = st.text_area("Next Day Plan", height=80)
        notes = st.text_area("Additional Notes", height=60)
        
        # Submit button
        if st.form_submit_button("📋 Create Report", use_container_width=True):
            # Validate data
            report_data = {
                'date': report_date.isoformat(),
                'project_name': "Highland Tower Development",
                'weather': WeatherCondition(weather),
                'temperature': temperature,
                'crew_size': crew_size,
                'work_hours': work_hours,
                'created_by': created_by,
                'work_summary': work_summary,
                'challenges': challenges,
                'next_day_plan': next_day_plan,
                'notes': notes
            }
            
            # Validate
            errors = daily_reports_manager.validate_report_data(report_data)
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Create report
                report_id = daily_reports_manager.create_report(report_data)
                st.success(f"✅ Daily report created successfully! ID: {report_id}")
                st.rerun()

def render_analytics_dashboard():
    """Render analytics and insights"""
    st.subheader("📈 Analytics Dashboard")
    
    reports = daily_reports_manager.get_all_reports()
    
    if not reports:
        st.info("No data available for analytics. Create some reports first.")
        return
    
    # Create analytics dataframe
    df_data = []
    for report in reports:
        df_data.append({
            'Date': report.date,
            'Crew Size': report.crew_size,
            'Work Hours': report.work_hours,
            'Total Crew Hours': report.crew_size * report.work_hours,
            'Weather': report.weather.value,
            'Status': report.status.value,
            'Activities Count': len(report.work_activities),
            'Safety Incidents': len(report.safety_incidents),
            'Deliveries Count': len(report.material_deliveries)
        })
    
    df = pd.DataFrame(df_data)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Daily Crew Hours Trend**")
        st.line_chart(df.set_index('Date')['Total Crew Hours'])
    
    with col2:
        st.markdown("**🌤️ Weather Distribution**")
        weather_counts = df['Weather'].value_counts()
        st.bar_chart(weather_counts)
    
    # Data table
    st.markdown("**📋 Reports Data Table**")
    st.dataframe(df, use_container_width=True)

def render_management_tools():
    """Render management and bulk operations"""
    st.subheader("⚙️ Management Tools")
    
    # Bulk operations
    st.markdown("#### 🔧 Bulk Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export All Reports", use_container_width=True):
            st.info("Export functionality would generate CSV/PDF export")
    
    with col2:
        if st.button("🗑️ Clear Draft Reports", use_container_width=True):
            draft_reports = daily_reports_manager.get_reports_by_status(ReportStatus.DRAFT)
            if draft_reports:
                for report in draft_reports:
                    daily_reports_manager.delete_report(report.report_id)
                st.success(f"Deleted {len(draft_reports)} draft reports")
                st.rerun()
            else:
                st.info("No draft reports to delete")
    
    # System stats
    st.markdown("#### 📊 System Statistics")
    stats = daily_reports_manager.generate_summary_stats()
    
    if stats:
        stats_df = pd.DataFrame([
            {"Metric": "Total Reports", "Value": stats['total_reports']},
            {"Metric": "Total Crew Hours", "Value": f"{stats['total_crew_hours']:,.0f}"},
            {"Metric": "Average Crew Size", "Value": stats['average_crew_size']},
            {"Metric": "Latest Report", "Value": stats['latest_report_date']}
        ])
        
        st.dataframe(stats_df, use_container_width=True, hide_index=True)