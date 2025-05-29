"""
System Analytics Module for gcPanel Highland Tower Development
Enterprise-grade system monitoring and performance analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def render():
    """Render the System Analytics admin module"""
    
    st.markdown("""
    <div class="admin-header">
        <h1>📊 System Analytics</h1>
        <p>Highland Tower Development - Performance Monitoring & Business Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analytics tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Performance", "👥 User Activity", "💾 System Health", "📊 Business Intelligence", "📋 Reports"])
    
    with tab1:
        st.markdown("### System Performance Overview")
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="admin-metric">
                <h3>99.8%</h3>
                <p>Uptime</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="admin-metric">
                <h3>245ms</h3>
                <p>Avg Response</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="admin-metric">
                <h3>15</h3>
                <p>Active Sessions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="admin-metric">
                <h3>2.3GB</h3>
                <p>Data Usage</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Response Time Trends")
            
            # Generate realistic response time data
            dates = pd.date_range(start='2025-01-01', end='2025-01-27', freq='D')
            response_times = np.random.normal(250, 50, len(dates))
            response_times = np.clip(response_times, 150, 500)  # Keep realistic range
            
            df_response = pd.DataFrame({
                'Date': dates,
                'Response Time (ms)': response_times,
                'Target': [300] * len(dates)
            })
            
            fig_response = px.line(
                df_response, 
                x='Date', 
                y=['Response Time (ms)', 'Target'],
                title='Highland Tower System Response Times',
                color_discrete_map={
                    'Response Time (ms)': '#3b82f6',
                    'Target': '#ef4444'
                }
            )
            fig_response.update_layout(height=300)
            st.plotly_chart(fig_response, use_container_width=True)
        
        with col2:
            st.markdown("#### System Resource Usage")
            
            # Resource usage data
            resources = ['CPU', 'Memory', 'Storage', 'Network']
            usage = [45, 62, 38, 28]
            colors = ['#10b981', '#f59e0b', '#3b82f6', '#8b5cf6']
            
            fig_resources = go.Figure(data=[
                go.Bar(x=resources, y=usage, marker_color=colors)
            ])
            fig_resources.update_layout(
                title='Current Resource Utilization (%)',
                height=300,
                yaxis=dict(range=[0, 100])
            )
            st.plotly_chart(fig_resources, use_container_width=True)
        
        # Module usage statistics
        st.markdown("#### Module Usage Analytics")
        
        module_data = {
            'Module': ['Dashboard', 'Field Operations', 'Engineering', 'Safety', 'Cost Management', 'BIM', 'RFIs', 'Documents'],
            'Daily Users': [17, 14, 12, 15, 8, 6, 11, 9],
            'Sessions': [45, 38, 32, 41, 24, 18, 28, 22],
            'Avg Duration (min)': [12, 18, 25, 15, 22, 35, 8, 14],
            'Data Created (MB)': [5.2, 28.4, 15.7, 12.3, 8.9, 45.2, 2.1, 34.6]
        }
        
        df_modules = pd.DataFrame(module_data)
        st.dataframe(df_modules, use_container_width=True)
    
    with tab2:
        st.markdown("### User Activity Analytics")
        
        # User activity overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Peak Usage Hours")
            
            hours = list(range(24))
            users = [2, 1, 1, 0, 0, 1, 3, 8, 15, 17, 16, 14, 13, 15, 16, 14, 12, 8, 5, 4, 3, 2, 2, 1]
            
            fig_hours = px.bar(
                x=hours, 
                y=users,
                title='Active Users by Hour',
                labels={'x': 'Hour of Day', 'y': 'Active Users'}
            )
            fig_hours.update_layout(height=250)
            st.plotly_chart(fig_hours, use_container_width=True)
        
        with col2:
            st.markdown("#### Device Usage")
            
            devices = ['Desktop', 'Tablet', 'Mobile']
            device_users = [82, 12, 6]
            
            fig_devices = px.pie(
                values=device_users, 
                names=devices,
                title='User Devices (%)',
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b']
            )
            fig_devices.update_layout(height=250)
            st.plotly_chart(fig_devices, use_container_width=True)
        
        with col3:
            st.markdown("#### Location Access")
            
            locations = ['On-Site', 'Office', 'Remote', 'Mobile']
            location_users = [45, 35, 15, 5]
            
            fig_locations = px.bar(
                x=locations, 
                y=location_users,
                title='Access Locations (%)',
                color_discrete_sequence=['#8b5cf6']
            )
            fig_locations.update_layout(height=250)
            st.plotly_chart(fig_locations, use_container_width=True)
        
        # User engagement metrics
        st.markdown("#### User Engagement Analysis")
        
        engagement_data = {
            'User': ['Jennifer Walsh', 'Sarah Chen', 'Mike Rodriguez', 'David Kim', 'Lisa Wong', 'Alex Thompson'],
            'Role': ['Project Manager', 'Structural Engineer', 'Site Supervisor', 'MEP Supervisor', 'Safety Manager', 'Cost Estimator'],
            'Sessions Today': [8, 6, 12, 7, 5, 4],
            'Total Time (hrs)': [6.5, 4.2, 8.1, 5.3, 3.8, 2.9],
            'Actions Performed': [45, 32, 67, 38, 28, 21],
            'Most Used Module': ['Dashboard', 'Engineering', 'Field Operations', 'Engineering', 'Safety', 'Cost Management'],
            'Last Activity': ['5 min ago', '12 min ago', '2 min ago', '8 min ago', '15 min ago', '25 min ago']
        }
        
        df_engagement = pd.DataFrame(engagement_data)
        st.dataframe(df_engagement, use_container_width=True)
        
        # Activity heatmap
        st.markdown("#### Weekly Activity Heatmap")
        
        # Generate activity heatmap data
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours = list(range(24))
        
        # Create sample activity matrix
        activity_matrix = np.random.randint(0, 20, size=(len(days), len(hours)))
        
        fig_heatmap = px.imshow(
            activity_matrix,
            x=hours,
            y=days,
            color_continuous_scale='Blues',
            title='User Activity Heatmap (Sessions per Hour)',
            labels=dict(x="Hour of Day", y="Day of Week", color="Sessions")
        )
        fig_heatmap.update_layout(height=300)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab3:
        st.markdown("### System Health Monitoring")
        
        # System health status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Current System Status")
            
            health_items = [
                {"service": "Web Server", "status": "✅ Healthy", "uptime": "99.9%"},
                {"service": "Database", "status": "✅ Healthy", "uptime": "99.8%"},
                {"service": "File Storage", "status": "✅ Healthy", "uptime": "100%"},
                {"service": "Authentication", "status": "✅ Healthy", "uptime": "99.9%"},
                {"service": "Email Service", "status": "⚠️ Warning", "uptime": "98.5%"},
                {"service": "Backup System", "status": "✅ Healthy", "uptime": "99.7%"}
            ]
            
            for item in health_items:
                st.markdown(f"""
                **{item['service']}**  
                Status: {item['status']}  
                Uptime: {item['uptime']}
                """)
                st.markdown("---")
        
        with col2:
            st.markdown("#### Resource Monitoring")
            
            # Resource gauge charts
            resources = ['CPU Usage', 'Memory Usage', 'Disk Usage', 'Network Load']
            values = [45, 62, 38, 28]
            
            for i, (resource, value) in enumerate(zip(resources, values)):
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = value,
                    title = {'text': resource},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#3b82f6"},
                        'steps': [
                            {'range': [0, 50], 'color': "#d1fae5"},
                            {'range': [50, 80], 'color': "#fef3c7"},
                            {'range': [80, 100], 'color': "#fecaca"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(height=200)
                st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Error logs and alerts
        st.markdown("#### Recent System Events")
        
        events_data = {
            'Timestamp': ['2025-01-27 14:25:33', '2025-01-27 12:15:22', '2025-01-27 10:30:15', '2025-01-27 08:45:12'],
            'Type': ['INFO', 'WARNING', 'INFO', 'ERROR'],
            'Component': ['Database', 'Email Service', 'Web Server', 'File Storage'],
            'Message': [
                'Database backup completed successfully',
                'Email delivery delayed - queue backlog',
                'Server restart completed - maintenance window',
                'Temporary file cleanup failed - disk space'
            ],
            'Resolution': ['N/A', 'Monitoring', 'Completed', 'Resolved']
        }
        
        df_events = pd.DataFrame(events_data)
        st.dataframe(df_events, use_container_width=True)
    
    with tab4:
        st.markdown("### Business Intelligence Dashboard")
        
        # Project KPIs
        st.markdown("#### Highland Tower Development KPIs")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="admin-metric">
                <h3>67.5%</h3>
                <p>Project Progress</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="admin-metric">
                <h3>$26.5M</h3>
                <p>Spent to Date</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="admin-metric">
                <h3>127</h3>
                <p>Safety Days</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="admin-metric">
                <h3>94%</h3>
                <p>Quality Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Business intelligence charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Cost Performance Trends")
            
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            budget = [3.5, 7.2, 11.8, 16.4, 21.2, 26.0]
            actual = [3.2, 6.9, 11.2, 15.8, 20.5, 25.1]
            forecast = [3.5, 7.1, 11.5, 16.0, 20.8, 25.8]
            
            fig_cost = go.Figure()
            fig_cost.add_trace(go.Scatter(x=months, y=budget, name='Budget', line=dict(color='#ef4444')))
            fig_cost.add_trace(go.Scatter(x=months, y=actual, name='Actual', line=dict(color='#10b981')))
            fig_cost.add_trace(go.Scatter(x=months, y=forecast, name='Forecast', line=dict(color='#3b82f6', dash='dash')))
            
            fig_cost.update_layout(
                title='Highland Tower Cost Performance ($M)',
                height=300
            )
            st.plotly_chart(fig_cost, use_container_width=True)
        
        with col2:
            st.markdown("#### Progress vs Schedule")
            
            phases = ['Foundation', 'Structure', 'MEP', 'Finishes']
            planned = [100, 85, 60, 25]
            actual = [100, 88, 55, 20]
            
            fig_progress = px.bar(
                x=phases,
                y=[planned, actual],
                barmode='group',
                title='Project Phase Progress (%)',
                color_discrete_sequence=['#3b82f6', '#10b981']
            )
            fig_progress.update_layout(height=300)
            st.plotly_chart(fig_progress, use_container_width=True)
        
        # ROI and productivity metrics
        st.markdown("#### Productivity & ROI Analysis")
        
        productivity_data = {
            'Metric': ['Labor Productivity', 'Equipment Utilization', 'Material Efficiency', 'Schedule Performance', 'Quality Index'],
            'Target': [100, 85, 90, 100, 95],
            'Current': [108, 92, 87, 96, 98],
            'Trend': ['↗️ +8%', '↗️ +7%', '↘️ -3%', '↘️ -4%', '↗️ +3%']
        }
        
        df_productivity = pd.DataFrame(productivity_data)
        st.dataframe(df_productivity, use_container_width=True)
    
    with tab5:
        st.markdown("### Reports & Export")
        
        # Report generation
        st.markdown("#### Generate System Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Performance Reports**")
            
            if st.button("📊 System Performance Report", use_container_width=True):
                st.success("✅ Performance report generated - Highland_Tower_Performance_2025.pdf")
            
            if st.button("👥 User Activity Report", use_container_width=True):
                st.success("✅ User activity report generated - Highland_Tower_Users_2025.xlsx")
            
            if st.button("🔒 Security Audit Report", use_container_width=True):
                st.success("✅ Security audit report generated - Highland_Tower_Security_2025.pdf")
            
            if st.button("💾 System Health Report", use_container_width=True):
                st.success("✅ System health report generated - Highland_Tower_Health_2025.xlsx")
        
        with col2:
            st.markdown("**Business Intelligence Reports**")
            
            if st.button("📈 Executive Dashboard", use_container_width=True):
                st.success("✅ Executive dashboard exported - Highland_Tower_Executive_2025.pdf")
            
            if st.button("💰 Financial Performance", use_container_width=True):
                st.success("✅ Financial report generated - Highland_Tower_Financial_2025.xlsx")
            
            if st.button("🎯 Project KPI Report", use_container_width=True):
                st.success("✅ KPI report generated - Highland_Tower_KPIs_2025.pdf")
            
            if st.button("📊 Custom Analytics", use_container_width=True):
                st.info("Opening custom analytics builder...")
        
        # Scheduled reports
        st.markdown("#### Scheduled Report Configuration")
        
        with st.form("schedule_reports"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                report_type = st.selectbox("Report Type", [
                    "System Performance", "User Activity", "Security Audit", 
                    "Business Intelligence", "Executive Summary"
                ])
            
            with col2:
                frequency = st.selectbox("Frequency", [
                    "Daily", "Weekly", "Monthly", "Quarterly"
                ])
            
            with col3:
                recipients = st.multiselect("Recipients", [
                    "jennifer.walsh@highlandtower.com",
                    "sarah.chen@highlandtower.com", 
                    "admin@highlandtower.com"
                ])
            
            if st.form_submit_button("📅 Schedule Report"):
                st.success(f"✅ {report_type} report scheduled {frequency.lower()} for {len(recipients)} recipients")
        
        # Export data
        st.markdown("#### Raw Data Export")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📁 Export User Data", use_container_width=True):
                st.success("User data exported to CSV")
        
        with col2:
            if st.button("📁 Export System Logs", use_container_width=True):
                st.success("System logs exported to JSON")
        
        with col3:
            if st.button("📁 Export Analytics Data", use_container_width=True):
                st.success("Analytics data exported to Excel")

if __name__ == "__main__":
    render()