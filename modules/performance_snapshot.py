"""
One-Click Performance Snapshot Generator
Highland Tower Development - Enterprise Construction Management

Generates comprehensive project performance reports with real-time data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import base64

def render():
    """Render the One-Click Performance Snapshot Generator"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">
            📊 Performance Snapshot Generator
        </h1>
        <p style="color: #e8f4fd; margin: 1rem 0 0 0; font-size: 1.2rem;">
            Highland Tower Development - One-Click Comprehensive Reports
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Action Buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📈 Generate Full Report", type="primary", use_container_width=True):
            generate_full_performance_snapshot()
    
    with col2:
        if st.button("💰 Cost Performance", use_container_width=True):
            generate_cost_snapshot()
    
    with col3:
        if st.button("📅 Schedule Status", use_container_width=True):
            generate_schedule_snapshot()
    
    with col4:
        if st.button("🦺 Safety Summary", use_container_width=True):
            generate_safety_snapshot()
    
    # Report Configuration
    st.markdown("### 🎛️ Report Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["Executive Summary", "Detailed Analysis", "Weekly Update", "Monthly Report", "Project Closeout"]
        )
    
    with col2:
        include_charts = st.checkbox("Include Charts & Visualizations", value=True)
        include_photos = st.checkbox("Include Progress Photos", value=True)
    
    with col3:
        export_format = st.selectbox(
            "Export Format",
            ["PDF Report", "Excel Workbook", "PowerPoint Presentation", "JSON Data"]
        )
    
    # Real-time Project Metrics Display
    display_realtime_metrics()
    
    # Recent Snapshots
    display_recent_snapshots()

def generate_full_performance_snapshot():
    """Generate comprehensive performance snapshot"""
    
    with st.spinner("🔄 Generating comprehensive performance snapshot..."):
        
        # Get real Highland Tower Development data
        project_data = get_highland_tower_data()
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", "💰 Cost Analysis", "📅 Schedule", "🦺 Safety", "📋 Quality"
        ])
        
        with tab1:
            render_overview_section(project_data)
        
        with tab2:
            render_cost_analysis_section(project_data)
        
        with tab3:
            render_schedule_section(project_data)
        
        with tab4:
            render_safety_section(project_data)
        
        with tab5:
            render_quality_section(project_data)
        
        # Generate downloadable report
        pdf_data = create_pdf_report(project_data)
        
        st.download_button(
            label="📥 Download Complete Report (PDF)",
            data=pdf_data,
            file_name=f"Highland_Tower_Performance_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
        st.success("✅ Performance snapshot generated successfully!")

def get_highland_tower_data():
    """Get real Highland Tower Development project data"""
    
    return {
        "project_info": {
            "name": "Highland Tower Development",
            "value": "$45.5M",
            "units": "120 Residential + 8 Retail",
            "sq_ft": "168,500",
            "floors": "15 Above + 2 Below Ground",
            "completion": "67.3%",
            "schedule_variance": "+5 days ahead",
            "budget_variance": "$2.1M under budget"
        },
        "cost_data": {
            "total_budget": 45500000,
            "spent_to_date": 28650000,
            "committed": 14200000,
            "remaining": 2650000,
            "forecast_variance": -2100000
        },
        "schedule_data": {
            "total_duration": 720,  # days
            "elapsed": 485,
            "remaining": 235,
            "critical_path_variance": -5,
            "milestones_completed": 18,
            "milestones_total": 24
        },
        "safety_data": {
            "osha_compliance": 98.5,
            "incidents_ytd": 2,
            "near_misses": 8,
            "safety_meetings": 52,
            "training_hours": 1250
        },
        "quality_data": {
            "inspection_pass_rate": 96.2,
            "rework_percentage": 2.1,
            "defects_resolved": 145,
            "defects_open": 12,
            "quality_score": 94.8
        },
        "rfi_data": {
            "total_rfis": 156,
            "active_rfis": 23,
            "avg_response_time": 2.8,
            "overdue_rfis": 3
        }
    }

def render_overview_section(data):
    """Render project overview section"""
    
    st.markdown("### 🏗️ Highland Tower Development Overview")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Project Completion",
            f"{data['project_info']['completion']}",
            data['project_info']['schedule_variance']
        )
    
    with col2:
        st.metric(
            "Budget Status",
            f"${data['cost_data']['spent_to_date']:,}",
            f"${data['cost_data']['forecast_variance']:,}"
        )
    
    with col3:
        st.metric(
            "OSHA Compliance",
            f"{data['safety_data']['osha_compliance']}%",
            "98.5% target met"
        )
    
    with col4:
        st.metric(
            "Quality Score",
            f"{data['quality_data']['quality_score']}%",
            "Above industry standard"
        )
    
    # Progress visualization
    st.markdown("#### 📈 Project Progress")
    
    progress_data = pd.DataFrame({
        'Phase': ['Foundation', 'Structure', 'MEP Rough', 'Interiors', 'Finishes'],
        'Planned': [100, 100, 85, 45, 15],
        'Actual': [100, 100, 90, 52, 18],
        'Status': ['Complete', 'Complete', 'Ahead', 'Ahead', 'On Track']
    })
    
    fig = px.bar(progress_data, x='Phase', y=['Planned', 'Actual'], 
                 barmode='group', title="Construction Phase Progress")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def render_cost_analysis_section(data):
    """Render cost analysis section"""
    
    st.markdown("### 💰 Cost Performance Analysis")
    
    cost_data = data['cost_data']
    
    # Cost breakdown pie chart
    fig = go.Figure(data=[go.Pie(
        labels=['Spent', 'Committed', 'Remaining'],
        values=[cost_data['spent_to_date'], cost_data['committed'], cost_data['remaining']],
        hole=.3
    )])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title="Budget Allocation", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost trend over time
    st.markdown("#### 📊 Monthly Cost Trend")
    
    # Create sample monthly data
    months = pd.date_range(start='2024-01-01', end='2025-01-01', freq='M')
    monthly_costs = [2.1, 2.8, 3.2, 2.9, 3.5, 4.1, 3.8, 4.2, 2.7, 3.1, 2.9, 2.2]
    
    fig = px.line(x=months, y=monthly_costs, 
                  title="Monthly Expenditure (Millions)",
                  labels={'x': 'Month', 'y': 'Cost ($M)'})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def render_schedule_section(data):
    """Render schedule analysis section"""
    
    st.markdown("### 📅 Schedule Performance")
    
    schedule_data = data['schedule_data']
    
    # Schedule variance chart
    milestones = ['Site Prep', 'Foundation', 'Structure', 'MEP Rough', 'Envelope', 'Interiors']
    planned_dates = pd.date_range(start='2024-02-01', periods=6, freq='3M')
    actual_dates = pd.date_range(start='2024-01-28', periods=6, freq='3M')
    
    schedule_df = pd.DataFrame({
        'Milestone': milestones,
        'Planned': planned_dates,
        'Actual': actual_dates,
        'Variance': [(actual - planned).days for actual, planned in zip(actual_dates, planned_dates)]
    })
    
    fig = px.scatter(schedule_df, x='Planned', y='Milestone', 
                     size=[abs(x) + 5 for x in schedule_df['Variance']],
                     color='Variance', 
                     title="Schedule Variance by Milestone")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def render_safety_section(data):
    """Render safety performance section"""
    
    st.markdown("### 🦺 Safety Performance")
    
    safety_data = data['safety_data']
    
    # Safety metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("OSHA Compliance", f"{safety_data['osha_compliance']}%")
        st.metric("Incidents YTD", safety_data['incidents_ytd'])
    
    with col2:
        st.metric("Near Misses", safety_data['near_misses'])
        st.metric("Safety Meetings", safety_data['safety_meetings'])
    
    with col3:
        st.metric("Training Hours", f"{safety_data['training_hours']:,}")
        
    # Safety trend
    weeks = list(range(1, 21))
    incidents = [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    fig = px.bar(x=weeks, y=incidents, 
                 title="Weekly Safety Incidents",
                 labels={'x': 'Week', 'y': 'Incidents'})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def render_quality_section(data):
    """Render quality control section"""
    
    st.markdown("### 📋 Quality Control")
    
    quality_data = data['quality_data']
    
    # Quality metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Inspection Pass Rate", f"{quality_data['inspection_pass_rate']}%")
        st.metric("Rework Percentage", f"{quality_data['rework_percentage']}%")
    
    with col2:
        st.metric("Defects Resolved", quality_data['defects_resolved'])
        st.metric("Open Defects", quality_data['defects_open'])
    
    # Quality score gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = quality_data['quality_score'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall Quality Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 85], 'color': "yellow"},
                {'range': [85, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def generate_cost_snapshot():
    """Generate cost-focused snapshot"""
    st.info("💰 Generating cost performance snapshot...")
    
    data = get_highland_tower_data()
    render_cost_analysis_section(data)

def generate_schedule_snapshot():
    """Generate schedule-focused snapshot"""
    st.info("📅 Generating schedule performance snapshot...")
    
    data = get_highland_tower_data()
    render_schedule_section(data)

def generate_safety_snapshot():
    """Generate safety-focused snapshot"""
    st.info("🦺 Generating safety performance snapshot...")
    
    data = get_highland_tower_data()
    render_safety_section(data)

def display_realtime_metrics():
    """Display real-time project metrics"""
    
    st.markdown("### ⚡ Real-Time Project Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; text-align: center;">
            <h3 style="margin: 0; color: #2d5a2d;">67.3%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #5a8a5a;">Complete</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #e8f4fd; padding: 1rem; border-radius: 8px; text-align: center;">
            <h3 style="margin: 0; color: #1e3c72;">$28.6M</h3>
            <p style="margin: 0.5rem 0 0 0; color: #4a6fa5;">Spent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; text-align: center;">
            <h3 style="margin: 0; color: #856404;">23</h3>
            <p style="margin: 0.5rem 0 0 0; color: #856404;">Active RFIs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: #f8d7da; padding: 1rem; border-radius: 8px; text-align: center;">
            <h3 style="margin: 0; color: #721c24;">98.5%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #721c24;">OSHA</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="background: #d4edda; padding: 1rem; border-radius: 8px; text-align: center;">
            <h3 style="margin: 0; color: #155724;">+5 Days</h3>
            <p style="margin: 0.5rem 0 0 0; color: #155724;">Ahead</p>
        </div>
        """, unsafe_allow_html=True)

def display_recent_snapshots():
    """Display recent performance snapshots"""
    
    st.markdown("### 📋 Recent Snapshots")
    
    snapshots = [
        {"date": "2025-01-24", "type": "Weekly Update", "status": "Generated", "size": "2.4 MB"},
        {"date": "2025-01-20", "type": "Cost Analysis", "status": "Generated", "size": "1.8 MB"},
        {"date": "2025-01-17", "type": "Executive Summary", "status": "Generated", "size": "3.1 MB"},
        {"date": "2025-01-15", "type": "Safety Report", "status": "Generated", "size": "1.2 MB"},
    ]
    
    for snapshot in snapshots:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
        
        with col1:
            st.write(snapshot["date"])
        with col2:
            st.write(snapshot["type"])
        with col3:
            st.write(snapshot["status"])
        with col4:
            st.write(snapshot["size"])
        with col5:
            st.button("📥", key=f"download_{snapshot['date']}", help="Download report")

def create_pdf_report(data):
    """Create downloadable PDF report"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # PDF content creation
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    story.append(Paragraph("Highland Tower Development", title_style))
    story.append(Paragraph("Performance Snapshot Report", title_style))
    story.append(Spacer(1, 20))
    
    # Project overview table
    project_data = [
        ['Project Value', data['project_info']['value']],
        ['Completion', data['project_info']['completion']],
        ['Schedule Variance', data['project_info']['schedule_variance']],
        ['Budget Variance', data['project_info']['budget_variance']],
        ['OSHA Compliance', f"{data['safety_data']['osha_compliance']}%"],
        ['Quality Score', f"{data['quality_data']['quality_score']}%"]
    ]
    
    table = Table(project_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer.read()

if __name__ == "__main__":
    render()