"""
Safety module for the gcPanel Construction Management Dashboard.

This module provides safety management features including incident tracking,
safety inspections, and safety metrics visualization.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.express as px

def render_safety():
    """Render the safety module"""
    
    # Header
    st.title("Safety Management")
    
    # Tab navigation for safety sections
    tab1, tab2, tab3 = st.tabs(["Incidents", "Inspections", "Training"])
    
    # Incidents Tab
    with tab1:
        render_incidents()
    
    # Inspections Tab
    with tab2:
        render_inspections()
    
    # Training Tab
    with tab3:
        render_training()

def render_incidents():
    """Render the incidents section"""
    
    st.header("Incident Management")
    
    # Filters in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range selector
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=90), key="incident_start_date")
    
    with col2:
        end_date = st.date_input("End Date", datetime.now(), key="incident_end_date")
    
    with col3:
        # Filter by severity
        severity = st.multiselect(
            "Severity", 
            ["Near Miss", "Minor", "Moderate", "Serious", "Critical"],
            default=["Minor", "Moderate", "Serious", "Critical"],
            key="incident_severity"
        )
    
    # Sample data for incidents
    incidents = [
        {
            "id": f"INC-{2025}-{i:03d}",
            "date": datetime.now() - timedelta(days=random.randint(1, 90)),
            "location": f"Building A - Floor {random.randint(1, 5)} - {random.choice(['North', 'South', 'East', 'West'])} Wing",
            "type": random.choice(["Slip/Trip/Fall", "Struck By", "Caught In/Between", "Electrical", "Chemical Exposure", "Ergonomic"]),
            "severity": random.choice(["Near Miss", "Minor", "Moderate", "Serious", "Critical"]),
            "description": f"Incident description {i}",
            "reported_by": random.choice(["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown"]),
            "status": random.choice(["Open", "Under Investigation", "Closed"]),
            "days_lost": random.randint(0, 30) if random.random() > 0.7 else 0,
            "corrective_action": f"Corrective action {i}" if random.random() > 0.3 else "",
        } for i in range(1, 26)
    ]
    
    df = pd.DataFrame(incidents)
    
    # Filter by date range and severity
    filtered_df = df[
        (df['date'] >= pd.Timestamp(start_date)) & 
        (df['date'] <= pd.Timestamp(end_date))
    ]
    
    if severity:
        filtered_df = filtered_df[filtered_df['severity'].isin(severity)]
    
    # Display safety metrics
    st.subheader("Safety Metrics")
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        total_incidents = len(filtered_df)
        st.metric("Total Incidents", total_incidents)
    
    with metrics_col2:
        serious_incidents = len(filtered_df[filtered_df['severity'].isin(['Serious', 'Critical'])])
        st.metric("Serious Incidents", serious_incidents)
    
    with metrics_col3:
        total_days_lost = filtered_df['days_lost'].sum()
        st.metric("Days Lost", total_days_lost)
    
    with metrics_col4:
        incident_rate = (total_incidents / 90) * 30  # Monthly rate based on selected period
        st.metric("Monthly Incident Rate", f"{incident_rate:.1f}")
    
    # Incident trend chart
    st.subheader("Incident Trends")
    
    # Group by date and count
    df_counts = filtered_df.copy()
    df_counts['month'] = df_counts['date'].dt.strftime('%Y-%m')
    trend_data = df_counts.groupby('month').size().reset_index(name='count')
    
    # Create trend chart with Plotly
    fig = px.bar(
        trend_data, 
        x='month', 
        y='count',
        title="Incidents by Month",
        labels={"month": "Month", "count": "Number of Incidents"}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Severity distribution pie chart
    severity_counts = filtered_df['severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    
    severity_fig = px.pie(
        severity_counts, 
        values='Count', 
        names='Severity',
        title="Incidents by Severity",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    
    st.plotly_chart(severity_fig, use_container_width=True)
    
    # Display incidents in a table
    st.subheader("Incident List")
    
    # Sort by date (newest first)
    filtered_df = filtered_df.sort_values('date', ascending=False)
    
    # Format the incident list with expandable details
    for i, row in filtered_df.iterrows():
        # Color based on severity
        if row['severity'] == "Critical":
            severity_color = "#721c24"  # Dark red
        elif row['severity'] == "Serious":
            severity_color = "#bd2130"  # Red
        elif row['severity'] == "Moderate":
            severity_color = "#e0a800"  # Orange
        elif row['severity'] == "Minor":
            severity_color = "#20c997"  # Teal
        else:  # Near Miss
            severity_color = "#6c757d"  # Gray
        
        with st.expander(f"{row['date'].strftime('%Y-%m-%d')} - {row['type']} - {row['severity']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**ID:** {row['id']}")
                st.markdown(f"**Date:** {row['date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Location:** {row['location']}")
                st.markdown(f"**Type:** {row['type']}")
                st.markdown(f"**Severity:** <span style='color: {severity_color}; font-weight: bold;'>{row['severity']}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**Reported By:** {row['reported_by']}")
                st.markdown(f"**Status:** {row['status']}")
                st.markdown(f"**Days Lost:** {row['days_lost']}")
                if row['corrective_action']:
                    st.markdown(f"**Corrective Action:** {row['corrective_action']}")
            
            st.markdown(f"**Description:** {row['description']}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Update Status", key=f"update_status_{row['id']}")
            with col2:
                st.button("Edit Details", key=f"edit_details_{row['id']}")
            with col3:
                st.button("View Full Report", key=f"view_report_{row['id']}")
    
    # Add incident form
    st.divider()
    if st.button("Report New Incident", type="primary", key="report_incident_btn"):
        st.session_state.show_incident_form = True
    
    # Display form if button was clicked
    if st.session_state.get("show_incident_form", False):
        with st.form("incident_form"):
            st.subheader("New Incident Report")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                incident_date = st.date_input("Date", datetime.now(), key="incident_date")
                incident_location = st.text_input("Location", "Building A - Floor 1", key="incident_location")
                incident_type = st.selectbox(
                    "Type", 
                    ["Slip/Trip/Fall", "Struck By", "Caught In/Between", "Electrical", "Chemical Exposure", "Ergonomic", "Other"],
                    key="incident_type"
                )
                incident_severity = st.selectbox(
                    "Severity",
                    ["Near Miss", "Minor", "Moderate", "Serious", "Critical"],
                    key="incident_severity_select"
                )
            
            with form_col2:
                incident_reported_by = st.text_input("Reported By", "", key="incident_reported_by")
                incident_status = st.selectbox(
                    "Status",
                    ["Open", "Under Investigation", "Closed"],
                    key="incident_status"
                )
                incident_days_lost = st.number_input("Days Lost", min_value=0, value=0, key="incident_days_lost")
                incident_corrective_action = st.text_input("Corrective Action", "", key="incident_corrective_action")
            
            incident_description = st.text_area("Description", "", key="incident_description")
            
            # Add photo upload
            incident_photos = st.file_uploader("Upload Photos", accept_multiple_files=True, key="incident_photos")
            
            submitted = st.form_submit_button("Submit Incident Report")
            
            if submitted:
                st.success("Incident report submitted successfully!")
                st.session_state.show_incident_form = False
                st.rerun()

def render_inspections():
    """Render the safety inspections section"""
    
    st.header("Safety Inspections")
    
    # Filters in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range selector
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30), key="inspection_start_date")
    
    with col2:
        end_date = st.date_input("End Date", datetime.now() + timedelta(days=30), key="inspection_end_date")
    
    with col3:
        # Filter by type
        inspection_type = st.selectbox(
            "Type", 
            ["All", "Daily", "Weekly", "Monthly", "Quarterly", "Annual", "Special"],
            key="inspection_type"
        )
    
    # Sample data for safety inspections
    inspections = [
        {
            "id": f"SAF-INSP-{2025}-{i:03d}",
            "date": datetime.now() + timedelta(days=random.randint(-30, 30)),
            "inspector": random.choice(["John Doe", "Jane Smith", "Safety Manager", "Site Foreman", "OSHA Inspector"]),
            "type": random.choice(["Daily", "Weekly", "Monthly", "Quarterly", "Annual", "Special"]),
            "location": f"Building A - Floor {random.randint(1, 5)} - {random.choice(['North', 'South', 'East', 'West'])} Wing",
            "status": "Scheduled" if (datetime.now() + timedelta(days=random.randint(-30, 30))) > datetime.now() 
                      else random.choice(["Completed - Pass", "Completed - Issues Found", "Cancelled"]),
            "findings": random.randint(0, 10),
            "critical_issues": random.randint(0, 3) if random.random() > 0.7 else 0,
            "description": f"Safety inspection {i}",
            "followup_required": random.choice([True, False])
        } for i in range(1, 31)
    ]
    
    df = pd.DataFrame(inspections)
    
    # Filter data
    filtered_df = df[
        (df['date'] >= pd.Timestamp(start_date)) & 
        (df['date'] <= pd.Timestamp(end_date))
    ]
    
    if inspection_type != "All":
        filtered_df = filtered_df[filtered_df['type'] == inspection_type]
    
    # Tabs for different views
    insp_tab1, insp_tab2, insp_tab3 = st.tabs(["Upcoming", "Completed", "Dashboard"])
    
    # Upcoming Inspections Tab
    with insp_tab1:
        upcoming_df = filtered_df[filtered_df['status'] == "Scheduled"].sort_values('date')
        
        if len(upcoming_df) > 0:
            st.subheader("Upcoming Safety Inspections")
            
            # Calendar view (simplified)
            st.markdown("### Schedule")
            
            # Group by date
            today = datetime.now().date()
            dates = sorted([date.date() for date in upcoming_df['date']])
            
            # Create a basic calendar view
            today_week = today - timedelta(days=today.weekday())
            next_week = today_week + timedelta(days=7)
            
            st.markdown("**This Week:**")
            this_week_inspections = upcoming_df[
                (upcoming_df['date'].dt.date >= today_week) & 
                (upcoming_df['date'].dt.date < next_week)
            ]
            
            if not this_week_inspections.empty:
                for _, insp in this_week_inspections.iterrows():
                    day_name = insp['date'].strftime('%A')
                    st.markdown(
                        f"<div style='background-color: #e6f2ff; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>"
                        f"<strong>{day_name}, {insp['date'].strftime('%b %d')}</strong>: "
                        f"{insp['type']} Inspection - {insp['location']} - Inspector: {insp['inspector']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No inspections scheduled for this week")
            
            st.markdown("**Upcoming:**")
            future_inspections = upcoming_df[upcoming_df['date'].dt.date >= next_week]
            
            if not future_inspections.empty:
                for _, insp in future_inspections.iterrows():
                    st.markdown(
                        f"<div style='padding: 10px; border-radius: 5px; margin-bottom: 5px; border: 1px solid #e0e0e0;'>"
                        f"<strong>{insp['date'].strftime('%b %d, %Y')}</strong>: "
                        f"{insp['type']} Inspection - {insp['location']} - Inspector: {insp['inspector']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No inspections scheduled beyond this week")
            
            # Schedule new inspection button
            st.divider()
            if st.button("Schedule New Inspection", key="schedule_new_inspection"):
                st.session_state.show_inspection_form = True
            
            # Inspection form
            if st.session_state.get("show_inspection_form", False):
                with st.form("inspection_form"):
                    st.subheader("Schedule New Safety Inspection")
                    
                    form_col1, form_col2 = st.columns(2)
                    
                    with form_col1:
                        inspection_date = st.date_input("Date", datetime.now() + timedelta(days=7), key="new_inspection_date")
                        inspection_inspector = st.text_input("Inspector", "Safety Manager", key="new_inspection_inspector")
                        inspection_type_input = st.selectbox(
                            "Type", 
                            ["Daily", "Weekly", "Monthly", "Quarterly", "Annual", "Special"],
                            key="new_inspection_type"
                        )
                    
                    with form_col2:
                        inspection_location = st.text_input("Location", "Building A - Floor 1", key="new_inspection_location")
                        inspection_description = st.text_area("Description", "", key="new_inspection_description")
                    
                    submitted = st.form_submit_button("Schedule Inspection")
                    
                    if submitted:
                        st.success("Safety inspection scheduled successfully!")
                        st.session_state.show_inspection_form = False
                        st.rerun()
        
        else:
            st.info("No upcoming inspections in the selected date range")
    
    # Completed Inspections Tab
    with insp_tab2:
        completed_df = filtered_df[filtered_df['status'] != "Scheduled"].sort_values('date', ascending=False)
        
        if len(completed_df) > 0:
            st.subheader("Completed Safety Inspections")
            
            for i, insp in completed_df.iterrows():
                # Set card color based on status
                if insp['status'] == "Completed - Pass":
                    card_color = "#d4edda"  # Green
                    text_color = "#155724"
                elif insp['status'] == "Completed - Issues Found":
                    card_color = "#f8d7da"  # Red
                    text_color = "#721c24"
                else:  # Cancelled
                    card_color = "#e2e3e5"  # Gray
                    text_color = "#383d41"
                
                with st.expander(f"{insp['date'].strftime('%Y-%m-%d')} - {insp['type']} - {insp['location']}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**ID:** {insp['id']}")
                        st.markdown(f"**Date:** {insp['date'].strftime('%Y-%m-%d')}")
                        st.markdown(f"**Type:** {insp['type']}")
                        st.markdown(f"**Inspector:** {insp['inspector']}")
                    
                    with col2:
                        st.markdown(f"**Location:** {insp['location']}")
                        st.markdown(f"**Status:** <span style='color: {text_color}; font-weight: bold;'>{insp['status']}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Findings:** {insp['findings']}")
                        st.markdown(f"**Critical Issues:** {insp['critical_issues']}")
                    
                    st.markdown(f"**Description:** {insp['description']}")
                    st.markdown(f"**Follow-up Required:** {'Yes' if insp['followup_required'] else 'No'}")
                    
                    # Action buttons
                    if insp['status'] == "Completed - Issues Found":
                        if st.button("Create Action Plan", key=f"action_plan_{insp['id']}"):
                            st.info("Creating action plan...")
        else:
            st.info("No completed inspections in the selected date range")
    
    # Dashboard Tab
    with insp_tab3:
        st.subheader("Safety Inspection Dashboard")
        
        # Summary metrics
        dashboard_col1, dashboard_col2, dashboard_col3, dashboard_col4 = st.columns(4)
        
        with dashboard_col1:
            total_inspections = len(filtered_df)
            st.metric("Total Inspections", total_inspections)
        
        with dashboard_col2:
            completed = len(filtered_df[filtered_df['status'] != "Scheduled"])
            completion_rate = (completed / total_inspections * 100) if total_inspections > 0 else 0
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        with dashboard_col3:
            total_findings = filtered_df['findings'].sum()
            st.metric("Total Findings", total_findings)
        
        with dashboard_col4:
            total_critical = filtered_df['critical_issues'].sum()
            st.metric("Critical Issues", total_critical)
        
        # Charts
        st.subheader("Inspection Analysis")
        
        # Findings by inspection type
        if not filtered_df.empty:
            findings_by_type = filtered_df.groupby('type')[['findings', 'critical_issues']].sum().reset_index()
            
            findings_fig = px.bar(
                findings_by_type,
                x='type',
                y=['findings', 'critical_issues'],
                title="Findings by Inspection Type",
                labels={"type": "Inspection Type", "value": "Number of Findings", "variable": "Finding Type"},
                barmode='group'
            )
            
            st.plotly_chart(findings_fig, use_container_width=True)
            
            # Status distribution
            status_counts = filtered_df['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            status_fig = px.pie(
                status_counts,
                values='Count',
                names='Status',
                title="Inspection Status Distribution",
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            
            st.plotly_chart(status_fig, use_container_width=True)
        else:
            st.info("No data available for analysis")

def render_training():
    """Render the safety training section"""
    
    st.header("Safety Training")
    
    # Sample data for training courses
    training_courses = [
        {
            "id": f"TR-{2025}-{i:03d}",
            "title": random.choice([
                "OSHA 10-Hour Construction", "Fall Protection", "Confined Space Entry",
                "Hazard Communication", "First Aid & CPR", "Scaffold Safety",
                "Electrical Safety", "Fire Prevention", "Personal Protective Equipment",
                "Trenching & Excavation", "Equipment Operation", "Emergency Response"
            ]),
            "instructor": random.choice(["John Smith", "Safety Manager", "External Trainer", "Online Course"]),
            "start_date": datetime.now() + timedelta(days=random.randint(-60, 60)),
            "duration_hours": random.choice([1, 2, 4, 8, 10, 30]),
            "location": random.choice(["On-site", "Training Center", "Virtual"]),
            "required_for": random.choice(["All Workers", "Supervisors", "Equipment Operators", "Electricians", "New Hires"]),
            "max_participants": random.randint(10, 30),
            "current_participants": random.randint(0, 25),
            "status": random.choice(["Scheduled", "In Progress", "Completed", "Cancelled"]),
            "certification": random.choice([True, False])
        } for i in range(1, 21)
    ]
    
    df = pd.DataFrame(training_courses)
    
    # Make status coherent with dates
    for i, row in df.iterrows():
        if row['start_date'].date() > datetime.now().date():
            df.at[i, 'status'] = "Scheduled"
        elif row['start_date'].date() == datetime.now().date():
            df.at[i, 'status'] = "In Progress"
        else:
            if df.at[i, 'status'] in ["Scheduled", "In Progress"]:
                df.at[i, 'status'] = "Completed"
    
    # Add completion data
    df['completion_rate'] = df.apply(
        lambda x: random.randint(80, 100) if x['status'] == "Completed" 
                else random.randint(0, 80) if x['status'] == "In Progress"
                else 0,
        axis=1
    )
    
    # Filter controls
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        status_filter = st.multiselect(
            "Status",
            ["Scheduled", "In Progress", "Completed", "Cancelled"],
            default=["Scheduled", "In Progress"],
            key="training_status_filter"
        )
    
    with filter_col2:
        if df['required_for'].nunique() > 1:
            role_filter = st.multiselect(
                "Required For",
                df['required_for'].unique().tolist(),
                default=[],
                key="training_role_filter"
            )
        else:
            role_filter = []
    
    # Apply filters
    filtered_df = df.copy()
    
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    
    if role_filter:
        filtered_df = filtered_df[filtered_df['required_for'].isin(role_filter)]
    
    # Sort by date (upcoming first)
    filtered_df = filtered_df.sort_values('start_date')
    
    # Tabs for different views
    training_tab1, training_tab2, training_tab3 = st.tabs(["Calendar", "Certifications", "Compliance"])
    
    # Calendar Tab
    with training_tab1:
        st.subheader("Training Calendar")
        
        # Group upcoming trainings by month
        upcoming_df = filtered_df[filtered_df['status'] != "Completed"].copy()
        upcoming_df['month'] = upcoming_df['start_date'].dt.strftime('%B %Y')
        
        if not upcoming_df.empty:
            months = upcoming_df['month'].unique()
            
            for month in months:
                st.markdown(f"### {month}")
                month_trainings = upcoming_df[upcoming_df['month'] == month]
                
                for _, training in month_trainings.iterrows():
                    # Status color
                    if training['status'] == "Scheduled":
                        status_color = "#0d6efd"  # Blue
                    elif training['status'] == "In Progress":
                        status_color = "#198754"  # Green
                    else:  # Cancelled
                        status_color = "#dc3545"  # Red
                    
                    # Training card
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <h4 style="margin: 0;">{training['title']}</h4>
                                    <p style="margin: 5px 0; color: #495057;">Instructor: {training['instructor']}</p>
                                </div>
                                <div style="text-align: right;">
                                    <p style="margin: 0; font-weight: bold;">{training['start_date'].strftime('%b %d, %Y')}</p>
                                    <p style="margin: 0; color: {status_color};">{training['status']}</p>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                                <p style="margin: 0;"><strong>Duration:</strong> {training['duration_hours']} hours</p>
                                <p style="margin: 0;"><strong>Location:</strong> {training['location']}</p>
                                <p style="margin: 0;"><strong>For:</strong> {training['required_for']}</p>
                                <p style="margin: 0;"><strong>Participants:</strong> {training['current_participants']}/{training['max_participants']}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Add training button
            st.divider()
            if st.button("Schedule New Training", type="primary", key="add_training_btn"):
                st.session_state.show_training_form = True
            
            # Training form
            if st.session_state.get("show_training_form", False):
                with st.form("training_form"):
                    st.subheader("Schedule New Safety Training")
                    
                    form_col1, form_col2 = st.columns(2)
                    
                    with form_col1:
                        training_title = st.text_input("Title", "", key="new_training_title")
                        training_instructor = st.text_input("Instructor", "", key="new_training_instructor")
                        training_date = st.date_input("Date", datetime.now() + timedelta(days=14), key="new_training_date")
                        training_duration = st.number_input("Duration (hours)", min_value=1, value=4, key="new_training_duration")
                    
                    with form_col2:
                        training_location = st.selectbox("Location", ["On-site", "Training Center", "Virtual"], key="new_training_location")
                        training_required_for = st.text_input("Required For", "All Workers", key="new_training_required_for")
                        training_max_participants = st.number_input("Maximum Participants", min_value=1, value=20, key="new_training_max")
                        training_certification = st.checkbox("Provides Certification", value=True, key="new_training_certification")
                    
                    submitted = st.form_submit_button("Schedule Training")
                    
                    if submitted:
                        st.success("Training scheduled successfully!")
                        st.session_state.show_training_form = False
                        st.rerun()
        else:
            st.info("No upcoming training sessions scheduled")
    
    # Certifications Tab
    with training_tab2:
        st.subheader("Safety Certifications")
        
        # Sample data for certifications
        cert_names = [
            "OSHA 10-Hour Construction", "OSHA 30-Hour Construction", "Fall Protection",
            "Confined Space Entry", "First Aid & CPR", "Forklift Operator",
            "Scaffold Competent Person", "Electrical Safety", "Trench Safety"
        ]
        
        employees = [
            "John Smith", "Jane Doe", "Bob Johnson", "Alice Brown", 
            "Carlos Rodriguez", "Sarah Lee", "Michael Chen", "David Wilson"
        ]
        
        certifications = []
        for i in range(1, 41):
            employee = random.choice(employees)
            cert = random.choice(cert_names)
            issue_date = datetime.now() - timedelta(days=random.randint(0, 730))
            valid_years = random.choice([1, 2, 3, 5])
            expiry_date = issue_date + timedelta(days=365 * valid_years)
            
            certifications.append({
                "id": f"CERT-{2025}-{i:03d}",
                "employee": employee,
                "certification": cert,
                "issue_date": issue_date,
                "expiry_date": expiry_date,
                "issuing_authority": random.choice(["OSHA", "Red Cross", "Company Training", "External Vendor"]),
                "status": "Valid" if expiry_date > datetime.now() else "Expired"
            })
        
        cert_df = pd.DataFrame(certifications)
        
        # Calculate expiration status
        cert_df['days_to_expiry'] = (cert_df['expiry_date'] - datetime.now()).dt.days
        
        # Filter controls
        cert_col1, cert_col2 = st.columns(2)
        
        with cert_col1:
            cert_status_filter = st.selectbox(
                "Status",
                ["All", "Valid", "Expired", "Expiring Soon (< 30 days)"],
                key="cert_status_filter"
            )
        
        with cert_col2:
            cert_type_filter = st.selectbox(
                "Certification Type",
                ["All"] + cert_names,
                key="cert_type_filter"
            )
        
        # Apply filters
        filtered_cert_df = cert_df.copy()
        
        if cert_status_filter == "Valid":
            filtered_cert_df = filtered_cert_df[filtered_cert_df['status'] == "Valid"]
        elif cert_status_filter == "Expired":
            filtered_cert_df = filtered_cert_df[filtered_cert_df['status'] == "Expired"]
        elif cert_status_filter == "Expiring Soon (< 30 days)":
            filtered_cert_df = filtered_cert_df[(filtered_cert_df['status'] == "Valid") & (filtered_cert_df['days_to_expiry'] <= 30)]
        
        if cert_type_filter != "All":
            filtered_cert_df = filtered_cert_df[filtered_cert_df['certification'] == cert_type_filter]
        
        # Status dashboard
        st.subheader("Certification Status")
        
        cert_metrics_col1, cert_metrics_col2, cert_metrics_col3, cert_metrics_col4 = st.columns(4)
        
        with cert_metrics_col1:
            total_certs = len(cert_df)
            st.metric("Total Certifications", total_certs)
        
        with cert_metrics_col2:
            valid_certs = len(cert_df[cert_df['status'] == "Valid"])
            st.metric("Valid Certifications", valid_certs)
        
        with cert_metrics_col3:
            expired_certs = len(cert_df[cert_df['status'] == "Expired"])
            st.metric("Expired Certifications", expired_certs)
        
        with cert_metrics_col4:
            expiring_soon = len(cert_df[(cert_df['status'] == "Valid") & (cert_df['days_to_expiry'] <= 30)])
            st.metric("Expiring Soon", expiring_soon)
        
        # Certification list table
        st.subheader("Certification List")
        
        # Sort by expiry date
        filtered_cert_df = filtered_cert_df.sort_values('days_to_expiry')
        
        for i, cert in filtered_cert_df.iterrows():
            # Status color
            if cert['status'] == "Expired":
                status_color = "#dc3545"  # Red
                status_text = "Expired"
            elif cert['days_to_expiry'] <= 30:
                status_color = "#fd7e14"  # Orange
                status_text = f"Expires in {cert['days_to_expiry']} days"
            else:
                status_color = "#198754"  # Green
                status_text = f"Valid ({cert['days_to_expiry']} days remaining)"
            
            # Certificate card
            st.markdown(
                f"""
                <div style="border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <h4 style="margin: 0;">{cert['certification']}</h4>
                            <p style="margin: 5px 0; color: #495057;">Holder: {cert['employee']}</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="margin: 0; color: {status_color}; font-weight: bold;">{status_text}</p>
                            <p style="margin: 0;">ID: {cert['id']}</p>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                        <p style="margin: 0;"><strong>Issued:</strong> {cert['issue_date'].strftime('%b %d, %Y')}</p>
                        <p style="margin: 0;"><strong>Expires:</strong> {cert['expiry_date'].strftime('%b %d, %Y')}</p>
                        <p style="margin: 0;"><strong>Authority:</strong> {cert['issuing_authority']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Compliance Tab
    with training_tab3:
        st.subheader("Training Compliance")
        
        # Sample data for training requirements
        roles = ["Site Worker", "Foreman", "Supervisor", "Equipment Operator", "Electrician", "Plumber"]
        
        role_requirements = []
        for role in roles:
            # Choose 3-5 required trainings for each role
            required_trainings = random.sample(cert_names, random.randint(3, min(5, len(cert_names))))
            for training in required_trainings:
                role_requirements.append({
                    "role": role,
                    "required_training": training,
                    "frequency_years": random.choice([1, 2, 3, 5]),
                    "compliance_rate": random.randint(70, 100),
                    "employees_total": random.randint(5, 20),
                    "employees_trained": random.randint(3, 18)
                })
        
        req_df = pd.DataFrame(role_requirements)
        req_df['compliance_pct'] = (req_df['employees_trained'] / req_df['employees_total'] * 100).round(1)
        
        # Compliance chart
        st.subheader("Training Compliance by Role")
        
        compliance_by_role = req_df.groupby('role')['compliance_pct'].mean().reset_index()
        compliance_by_role['compliance_pct'] = compliance_by_role['compliance_pct'].round(1)
        
        compliance_fig = px.bar(
            compliance_by_role,
            x='role',
            y='compliance_pct',
            color='compliance_pct',
            color_continuous_scale=['red', 'yellow', 'green'],
            range_color=[70, 100],
            title="Average Training Compliance by Role",
            labels={"role": "Role", "compliance_pct": "Compliance Rate (%)"}
        )
        
        compliance_fig.add_hline(
            y=90,
            line_dash="dash",
            line_color="green",
            annotation_text="Target (90%)",
            annotation_position="bottom right"
        )
        
        st.plotly_chart(compliance_fig, use_container_width=True)
        
        # Detailed compliance table
        st.subheader("Required Training by Role")
        
        # Group by role
        for role in roles:
            role_df = req_df[req_df['role'] == role]
            
            if not role_df.empty:
                with st.expander(f"{role}", expanded=False):
                    st.markdown(f"### {role} Required Training")
                    
                    # Calculate overall compliance for this role
                    overall_compliance = role_df['compliance_pct'].mean()
                    if overall_compliance >= 90:
                        compliance_color = "green"
                    elif overall_compliance >= 75:
                        compliance_color = "orange"
                    else:
                        compliance_color = "red"
                    
                    st.markdown(f"<h4>Overall Compliance: <span style='color: {compliance_color};'>{overall_compliance:.1f}%</span></h4>", unsafe_allow_html=True)
                    
                    # Training requirements
                    for _, req in role_df.iterrows():
                        if req['compliance_pct'] >= 90:
                            req_color = "#d4edda"  # Green background
                            text_color = "#155724"  # Dark green text
                        elif req['compliance_pct'] >= 75:
                            req_color = "#fff3cd"  # Yellow background
                            text_color = "#856404"  # Dark yellow text
                        else:
                            req_color = "#f8d7da"  # Red background
                            text_color = "#721c24"  # Dark red text
                        
                        st.markdown(
                            f"""
                            <div style="background-color: {req_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                                <div style="display: flex; justify-content: space-between;">
                                    <div>
                                        <h5 style="margin: 0; color: {text_color};">{req['required_training']}</h5>
                                        <p style="margin: 5px 0;">Frequency: Every {req['frequency_years']} year(s)</p>
                                    </div>
                                    <div style="text-align: right;">
                                        <h5 style="margin: 0; color: {text_color};">{req['compliance_pct']}% Compliant</h5>
                                        <p style="margin: 5px 0;">{req['employees_trained']}/{req['employees_total']} Employees</p>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("Schedule Training", key=f"schedule_{role}")
                    with col2:
                        st.button("View Employees", key=f"view_{role}")
        
        # Compliance improvements
        st.subheader("Recommended Actions")
        
        # Find trainings with low compliance
        low_compliance = req_df[req_df['compliance_pct'] < 75].sort_values('compliance_pct')
        
        if not low_compliance.empty:
            for _, action in low_compliance.iterrows():
                needed_employees = action['employees_total'] - action['employees_trained']
                
                st.markdown(
                    f"""
                    <div style="border: 1px solid #dc3545; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                        <h5 style="color: #dc3545; margin-top: 0;">Schedule {action['required_training']} for {action['role']}</h5>
                        <p>Current compliance: <strong>{action['compliance_pct']}%</strong></p>
                        <p>{needed_employees} employees need this training to achieve compliance</p>
                        <p>This would improve overall compliance by approximately <strong>{(needed_employees / req_df['employees_total'].sum() * 100).round(1)}%</strong></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.success("All training requirements are above 75% compliance. Focus on maintaining current training schedule.")