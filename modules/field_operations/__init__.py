"""
Field Operations module for the gcPanel Construction Management Dashboard.

This module provides field operations management features including daily reports,
quality control, and field inspection tracking.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def render_field_operations():
    """Render the field operations module"""
    
    # Header
    st.title("Field Operations")
    
    # Tab navigation for field operations sections
    tab1, tab2, tab3 = st.tabs(["Daily Reports", "Quality Control", "Field Inspections"])
    
    # Daily Reports Tab
    with tab1:
        render_daily_reports()
    
    # Quality Control Tab
    with tab2:
        render_quality_control()
    
    # Field Inspections Tab
    with tab3:
        render_field_inspections()

def render_daily_reports():
    """Render the daily reports section"""
    
    # Header with button
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.header("Daily Reports")
    
    with col3:
        if st.button("Add New Daily Report", type="primary", key="add_daily_report_top"):
            st.session_state.show_daily_report_form = True
    
    # Filters in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range selector
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    with col3:
        # Trade filter
        trade = st.selectbox("Trade", ["All", "Concrete", "Steel", "Electrical", "Mechanical", "Plumbing"])
    
    # Sample data for daily reports
    reports = [
        {
            "date": datetime.now() - timedelta(days=x),
            "trade": random.choice(["Concrete", "Steel", "Electrical", "Mechanical", "Plumbing"]),
            "crew_size": random.randint(3, 15),
            "hours_worked": random.randint(6, 10),
            "weather": random.choice(["Sunny", "Cloudy", "Rainy", "Windy"]),
            "temperature": random.randint(45, 85),
            "work_performed": f"Work item {random.randint(1, 100)}",
            "delays": random.choice([None, "Material delivery", "Equipment failure", "Weather"]),
            "safety_incidents": random.choice([None, None, None, "Minor injury"]),
            "author": random.choice(["John Doe", "Jane Smith", "Bob Johnson"])
        } for x in range(30)
    ]
    
    df = pd.DataFrame(reports)
    
    # Filter data
    filtered_df = df[(df['date'] >= pd.Timestamp(start_date)) & 
                    (df['date'] <= pd.Timestamp(end_date))]
    
    if trade != "All":
        filtered_df = filtered_df[filtered_df['trade'] == trade]
    
    # Display stats
    st.subheader("Daily Report Statistics")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total Reports", len(filtered_df))
    
    with stat_col2:
        avg_crew = filtered_df['crew_size'].mean()
        st.metric("Avg. Crew Size", f"{avg_crew:.1f}")
    
    with stat_col3:
        delays = filtered_df['delays'].notna().sum()
        st.metric("Delays Reported", delays)
    
    with stat_col4:
        incidents = filtered_df['safety_incidents'].notna().sum()
        st.metric("Safety Incidents", incidents)
    
    # Display data in expandable sections
    st.subheader("Daily Reports")
    
    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['date'].strftime('%Y-%m-%d')} - {row['trade']} - {row['work_performed']}"):
            report_col1, report_col2 = st.columns(2)
            
            with report_col1:
                st.markdown(f"**Date:** {row['date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Trade:** {row['trade']}")
                st.markdown(f"**Crew Size:** {row['crew_size']}")
                st.markdown(f"**Hours Worked:** {row['hours_worked']}")
            
            with report_col2:
                st.markdown(f"**Weather:** {row['weather']}")
                st.markdown(f"**Temperature:** {row['temperature']}°F")
                st.markdown(f"**Delays:** {row['delays'] if pd.notna(row['delays']) else 'None'}")
                st.markdown(f"**Safety Incidents:** {row['safety_incidents'] if pd.notna(row['safety_incidents']) else 'None'}")
            
            st.markdown(f"**Work Performed:** {row['work_performed']}")
            st.markdown(f"**Author:** {row['author']}")
    
    # Divider before form
    st.divider()
    
    # Display form if button was clicked
    if st.session_state.get("show_daily_report_form", False):
        with st.form("daily_report_form"):
            st.subheader("New Daily Report")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                report_date = st.date_input("Date", datetime.now())
                report_trade = st.selectbox("Trade", ["Concrete", "Steel", "Electrical", "Mechanical", "Plumbing"])
                crew_size = st.number_input("Crew Size", min_value=1, max_value=100, value=5)
                hours_worked = st.number_input("Hours Worked", min_value=0, max_value=24, value=8)
            
            with form_col2:
                weather = st.selectbox("Weather", ["Sunny", "Cloudy", "Rainy", "Windy", "Snow"])
                temperature = st.number_input("Temperature (°F)", min_value=-20, max_value=120, value=70)
                delays = st.text_input("Delays (if any)")
                safety_incidents = st.text_input("Safety Incidents (if any)")
            
            work_performed = st.text_area("Work Performed")
            
            submitted = st.form_submit_button("Submit Report")
            
            if submitted:
                st.success("Daily report submitted successfully!")
                st.session_state.show_daily_report_form = False
                st.rerun()


def render_quality_control():
    """Render the quality control section"""
    
    # Header with button
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.header("Quality Control")
    
    with col3:
        if st.button("Add New QC Inspection", type="primary", key="add_qc_inspection_top"):
            st.session_state.show_qc_form = True
    
    # Sample data for quality control items
    qc_items = [
        {
            "id": f"QC-{2025}-{i:03d}",
            "date": datetime.now() - timedelta(days=random.randint(1, 60)),
            "inspector": random.choice(["John Doe", "Jane Smith", "Bob Johnson"]),
            "location": f"Building A - Floor {random.randint(1, 5)} - Room {random.randint(101, 150)}",
            "trade": random.choice(["Concrete", "Steel", "Electrical", "Mechanical", "Plumbing"]),
            "description": f"Quality inspection item {i}",
            "status": random.choice(["Pending", "Passed", "Failed", "Remediated"]),
            "photos": random.randint(0, 5)
        } for i in range(1, 31)
    ]
    
    df = pd.DataFrame(qc_items)
    
    # Filters in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Status filter
        status_filter = st.multiselect("Status", ["Pending", "Passed", "Failed", "Remediated"], default=["Pending", "Failed"])
    
    with col2:
        # Trade filter
        trade_filter = st.multiselect("Trade", ["Concrete", "Steel", "Electrical", "Mechanical", "Plumbing"], default=[])
    
    with col3:
        # Inspector filter
        inspector_filter = st.multiselect("Inspector", df['inspector'].unique().tolist(), default=[])
    
    # Filter data
    filtered_df = df.copy()
    
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    
    if trade_filter:
        filtered_df = filtered_df[filtered_df['trade'].isin(trade_filter)]
    
    if inspector_filter:
        filtered_df = filtered_df[filtered_df['inspector'].isin(inspector_filter)]
    
    # Sort by status priority (Failed, Pending, Remediated, Passed)
    status_priority = {
        "Failed": 0,
        "Pending": 1,
        "Remediated": 2,
        "Passed": 3
    }
    filtered_df['status_priority'] = filtered_df['status'].map(status_priority)
    filtered_df = filtered_df.sort_values('status_priority')
    
    # Display stats
    st.subheader("Quality Control Statistics")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total Items", len(filtered_df))
    
    with stat_col2:
        passed = len(filtered_df[filtered_df['status'] == 'Passed'])
        pass_rate = (passed / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("Pass Rate", f"{pass_rate:.1f}%")
    
    with stat_col3:
        failed = len(filtered_df[filtered_df['status'] == 'Failed'])
        st.metric("Failed Items", failed)
    
    with stat_col4:
        pending = len(filtered_df[filtered_df['status'] == 'Pending'])
        st.metric("Pending Items", pending)
    
    # Display data table
    st.subheader("Quality Control Items")
    
    # Display dataframe
    filtered_df_display = filtered_df.drop('status_priority', axis=1)
    st.dataframe(filtered_df_display, hide_index=True)
    
    # Divider before form
    st.divider()
    
    # Display form if button was clicked
    if st.session_state.get("show_qc_form", False):
        with st.form("qc_form"):
            st.subheader("New Quality Control Inspection")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                qc_date = st.date_input("Date", datetime.now())
                qc_inspector = st.selectbox("Inspector", ["John Doe", "Jane Smith", "Bob Johnson"])
                qc_location = st.text_input("Location", "Building A - Floor 1 - Room 101")
            
            with form_col2:
                qc_trade = st.selectbox("Trade", ["Concrete", "Steel", "Electrical", "Mechanical", "Plumbing"])
                qc_status = st.selectbox("Status", ["Pending", "Passed", "Failed", "Remediated"])
                qc_photos = st.file_uploader("Upload Photos", accept_multiple_files=True)
            
            qc_description = st.text_area("Description")
            
            submitted = st.form_submit_button("Submit Inspection")
            
            if submitted:
                st.success("Quality control inspection submitted successfully!")
                st.session_state.show_qc_form = False
                st.rerun()

def render_field_inspections():
    """Render the field inspections section"""
    
    st.header("Field Inspections")
    
    # Tabs for different types of inspections
    inspection_tab1, inspection_tab2, inspection_tab3 = st.tabs(["Scheduled", "Completed", "Non-Compliance"])
    
    # Sample data for inspections
    inspections = [
        {
            "id": f"INSP-{2025}-{i:03d}",
            "date": datetime.now() + timedelta(days=random.randint(-30, 30)),
            "inspector": random.choice(["John Doe", "Jane Smith", "Bob Johnson", "Building Official", "Fire Marshal"]),
            "type": random.choice(["Building", "Electrical", "Mechanical", "Plumbing", "Fire Safety", "ADA"]),
            "location": f"Building A - Floor {random.randint(1, 5)}",
            "status": "Scheduled" if (datetime.now() + timedelta(days=random.randint(-30, 30))) > datetime.now() 
                      else random.choice(["Passed", "Failed", "Conditionally Passed"]),
            "description": f"Inspection for {random.choice(['rough-in', 'final', 'framing', 'foundation', 'insulation'])}",
            "notes": "" if random.random() > 0.3 else "Some notes about the inspection"
        } for i in range(1, 41)
    ]
    
    df = pd.DataFrame(inspections)
    df['is_compliant'] = df['status'] != "Failed"
    
    # Scheduled Inspections Tab
    with inspection_tab1:
        scheduled_df = df[df['status'] == "Scheduled"].sort_values('date')
        
        if len(scheduled_df) > 0:
            st.info(f"You have {len(scheduled_df)} upcoming inspections")
            
            # Calendar view
            st.subheader("Inspection Calendar")
            
            # Group inspections by date
            today = datetime.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            dates = [start_of_week + timedelta(days=i) for i in range(14)]  # 2 weeks
            
            # Create calendar grid with 7 columns (1 week per row)
            weeks = [dates[:7], dates[7:]]
            
            for week in weeks:
                cols = st.columns(7)
                
                for i, date in enumerate(week):
                    with cols[i]:
                        # Date header
                        is_today = date == today
                        header_style = "background-color: #e6f2ff; font-weight: bold; padding: 5px; border-radius: 5px;" if is_today else ""
                        st.markdown(f"<div style='{header_style}'>{date.strftime('%a %m/%d')}</div>", unsafe_allow_html=True)
                        
                        # Inspections for this date
                        day_inspections = scheduled_df[scheduled_df['date'].dt.date == date]
                        
                        for _, insp in day_inspections.iterrows():
                            st.markdown(
                                f"<div style='background-color: #f0f0f0; padding: 5px; margin: 3px 0; border-radius: 3px; font-size: 0.8em;'>" +
                                f"<strong>{insp['type']}</strong><br/>" +
                                f"{insp['location']}<br/>" +
                                f"<em>{insp['inspector']}</em>" +
                                "</div>", 
                                unsafe_allow_html=True
                            )
            
            # List view
            st.subheader("Upcoming Inspections")
            for _, insp in scheduled_df.iterrows():
                with st.expander(f"{insp['date'].strftime('%Y-%m-%d')} - {insp['type']} - {insp['description']}"):
                    insp_col1, insp_col2 = st.columns(2)
                    
                    with insp_col1:
                        st.markdown(f"**ID:** {insp['id']}")
                        st.markdown(f"**Date:** {insp['date'].strftime('%Y-%m-%d')}")
                        st.markdown(f"**Inspector:** {insp['inspector']}")
                        st.markdown(f"**Type:** {insp['type']}")
                    
                    with insp_col2:
                        st.markdown(f"**Location:** {insp['location']}")
                        st.markdown(f"**Status:** {insp['status']}")
                        st.markdown(f"**Description:** {insp['description']}")
                    
                    if insp['notes']:
                        st.markdown(f"**Notes:** {insp['notes']}")
                    
                    # Action buttons
                    st.button("Reschedule", key=f"reschedule_{insp['id']}")
                    st.button("Cancel", key=f"cancel_{insp['id']}", type="secondary")
        else:
            st.info("No scheduled inspections")
    
    # Completed Inspections Tab
    with inspection_tab2:
        completed_df = df[df['status'].isin(["Passed", "Failed", "Conditionally Passed"])].sort_values('date', ascending=False)
        
        if len(completed_df) > 0:
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status_filter = st.multiselect(
                    "Status", 
                    ["Passed", "Failed", "Conditionally Passed"],
                    default=["Passed", "Failed", "Conditionally Passed"]
                )
            
            with col2:
                type_filter = st.multiselect(
                    "Type",
                    completed_df['type'].unique().tolist(),
                    default=[]
                )
            
            with col3:
                inspector_filter = st.multiselect(
                    "Inspector",
                    completed_df['inspector'].unique().tolist(),
                    default=[]
                )
            
            # Apply filters
            filtered_df = completed_df.copy()
            
            if status_filter:
                filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
            
            if type_filter:
                filtered_df = filtered_df[filtered_df['type'].isin(type_filter)]
            
            if inspector_filter:
                filtered_df = filtered_df[filtered_df['inspector'].isin(inspector_filter)]
            
            # Display stats
            st.subheader("Inspection Statistics")
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            
            with stat_col1:
                total = len(filtered_df)
                st.metric("Total Inspections", total)
            
            with stat_col2:
                passed = len(filtered_df[filtered_df['status'] == 'Passed'])
                pass_rate = (passed / total * 100) if total > 0 else 0
                st.metric("Pass Rate", f"{pass_rate:.1f}%")
            
            with stat_col3:
                failed = len(filtered_df[filtered_df['status'] == 'Failed'])
                st.metric("Failed Inspections", failed)
            
            # Display table
            st.subheader("Completed Inspections")
            filtered_df_display = filtered_df.drop('is_compliant', axis=1)
            st.dataframe(filtered_df_display, hide_index=True)
        else:
            st.info("No completed inspections")
    
    # Non-Compliance Tab
    with inspection_tab3:
        non_compliant_df = df[~df['is_compliant']].sort_values('date', ascending=False)
        
        if len(non_compliant_df) > 0:
            st.warning(f"You have {len(non_compliant_df)} non-compliant inspections that require attention")
            
            # Group by type
            grouped = non_compliant_df.groupby('type').size().reset_index(name='count')
            
            # Display chart
            st.subheader("Non-Compliance by Type")
            st.bar_chart(grouped.set_index('type'))
            
            # Display list of non-compliant items
            st.subheader("Non-Compliant Inspections")
            
            for _, insp in non_compliant_df.iterrows():
                with st.expander(f"{insp['date'].strftime('%Y-%m-%d')} - {insp['type']} - {insp['description']}"):
                    insp_col1, insp_col2 = st.columns(2)
                    
                    with insp_col1:
                        st.markdown(f"**ID:** {insp['id']}")
                        st.markdown(f"**Date:** {insp['date'].strftime('%Y-%m-%d')}")
                        st.markdown(f"**Inspector:** {insp['inspector']}")
                        st.markdown(f"**Type:** {insp['type']}")
                    
                    with insp_col2:
                        st.markdown(f"**Location:** {insp['location']}")
                        st.markdown(f"**Status:** {insp['status']}")
                        st.markdown(f"**Description:** {insp['description']}")
                    
                    if insp['notes']:
                        st.markdown(f"**Notes:** {insp['notes']}")
                    
                    # Action buttons
                    st.button("Schedule Re-inspection", key=f"reinspect_{insp['id']}", type="primary")
                    st.button("Mark as Remediated", key=f"remediate_{insp['id']}")
        else:
            st.success("No non-compliant inspections!")
    
    # Add new inspection button
    st.divider()
    if st.button("Schedule New Inspection", type="primary"):
        st.session_state.show_inspection_form = True
    
    # Display form if button was clicked
    if st.session_state.get("show_inspection_form", False):
        with st.form("inspection_form"):
            st.subheader("Schedule New Inspection")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                insp_date = st.date_input("Date", datetime.now() + timedelta(days=3))
                insp_inspector = st.selectbox("Inspector", ["John Doe", "Jane Smith", "Building Official", "Fire Marshal"])
                insp_type = st.selectbox("Type", ["Building", "Electrical", "Mechanical", "Plumbing", "Fire Safety", "ADA"])
            
            with form_col2:
                insp_location = st.text_input("Location", "Building A - Floor 1")
                insp_time = st.time_input("Time", datetime.now().time())
                insp_description = st.text_input("Description", "Final inspection")
            
            insp_notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Schedule Inspection")
            
            if submitted:
                st.success("Inspection scheduled successfully!")
                st.session_state.show_inspection_form = False
                st.rerun()