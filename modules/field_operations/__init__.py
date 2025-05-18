"""
Field Operations module for the gcPanel Construction Management Dashboard.

This module provides field operations management features including daily reports,
quality control, field inspection tracking, and delivery tracking.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, time
import random
import calendar
from utils.notifications import send_delivery_notification, NotificationType

def render_field_operations():
    """Render the field operations module"""
    
    # Header
    st.title("Field Operations")
    
    # Tab navigation for field operations sections
    tab1, tab2, tab3, tab4 = st.tabs(["Daily Reports", "Quality Control", "Field Inspections", "Delivery Tracking"])
    
    # Daily Reports Tab
    with tab1:
        render_daily_reports()
    
    # Quality Control Tab
    with tab2:
        render_quality_control()
    
    # Field Inspections Tab
    with tab3:
        render_field_inspections()
        
    # Delivery Tracking Tab
    with tab4:
        render_delivery_tracking()

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

def render_delivery_tracking():
    """Render the delivery tracking section, integrated with procurement items"""
    
    # Initialize session state variables if they don't exist
    if "show_delivery_form" not in st.session_state:
        st.session_state.show_delivery_form = False
    if "show_reschedule_form" not in st.session_state:
        st.session_state.show_reschedule_form = False
    if "reschedule_delivery_id" not in st.session_state:
        st.session_state.reschedule_delivery_id = None
    
    # Header with button
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.header("Delivery Tracking")
    
    # Show notification indicator in the header
    with col2:
        from components.notification_center import notification_indicator
        notification_indicator()
    
    with col3:
        if st.button("Add New Delivery", type="primary", key="add_delivery_btn"):
            st.session_state.show_delivery_form = True
    
    # Show reschedule form if button was clicked
    if st.session_state.get("show_reschedule_form", False) and st.session_state.get("reschedule_delivery_id"):
        render_reschedule_form(st.session_state.reschedule_delivery_id)
    
    # Date filters
    view_col1, view_col2, view_col3 = st.columns(3)
    with view_col1:
        view_option = st.radio(
            "View",
            ["Calendar", "List"],
            horizontal=True,
            key="delivery_view_option"
        )
    
    with view_col2:
        # For calendar view, select month/year
        if view_option == "Calendar":
            selected_month = st.selectbox(
                "Month",
                list(range(1, 13)),
                index=datetime.now().month - 1,
                format_func=lambda x: calendar.month_name[x],
                key="delivery_month"
            )
            
    with view_col3:
        if view_option == "Calendar":
            selected_year = st.selectbox(
                "Year",
                list(range(datetime.now().year - 1, datetime.now().year + 3)),
                index=1,  # Default to current year
                key="delivery_year"
            )
        else:
            # For list view, select date range
            date_range = st.selectbox(
                "Date Range",
                ["Today", "This Week", "This Month", "Next 30 Days", "All"],
                key="delivery_date_range"
            )
    
    # Generate sample procurement items with delivery dates
    # In a real application, this would come from the database
    procurement_items = generate_sample_procurement_items()
    
    # Filter based on selected date range for list view
    if view_option == "List":
        st.subheader("Upcoming Deliveries")
        filtered_items = filter_deliveries_by_date_range(procurement_items, date_range)
        render_delivery_list(filtered_items)
    else:
        # Calendar view
        st.subheader(f"Delivery Calendar - {calendar.month_name[selected_month]} {selected_year}")
        render_delivery_calendar(procurement_items, selected_month, selected_year)
    
    # Delivery statistics
    st.divider()
    st.subheader("Delivery Statistics")
    
    # Calculate statistics
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        today_deliveries = len(procurement_items[procurement_items['delivery_date'].dt.date == datetime.now().date()])
        st.metric("Today's Deliveries", today_deliveries)
    
    with stats_col2:
        # Calculate this week's deliveries
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_mask = (procurement_items['delivery_date'].dt.date >= week_start) & (procurement_items['delivery_date'].dt.date <= week_end)
        week_deliveries = len(procurement_items[week_mask])
        st.metric("This Week's Deliveries", week_deliveries)
    
    with stats_col3:
        on_time_count = len(procurement_items[procurement_items['status'] == 'On Schedule'])
        total_count = len(procurement_items)
        on_time_pct = (on_time_count / total_count * 100) if total_count > 0 else 0
        st.metric("On-Time Delivery Rate", f"{on_time_pct:.1f}%")
    
    with stats_col4:
        critical_deliveries = len(procurement_items[procurement_items['priority'] == 'Critical'])
        st.metric("Critical Deliveries", critical_deliveries)
    
    # Display form for adding new delivery if button was clicked
    if st.session_state.get("show_delivery_form", False):
        with st.form("delivery_form"):
            st.subheader("Add New Delivery")
            
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                item_name = st.text_input("Item Name", "Curtain Wall Panels")
                supplier = st.text_input("Supplier", "Acme Glass & Aluminum")
                quantity = st.number_input("Quantity", min_value=1, value=10)
                unit = st.selectbox(
                    "Unit", 
                    ["Each", "Pallets", "Truckloads", "Cubic Yards", "Tons", "Square Feet"],
                    key="delivery_unit"
                )
            
            with form_col2:
                delivery_date = st.date_input("Delivery Date", datetime.now() + timedelta(days=7))
                delivery_time = st.time_input("Delivery Time", time(9, 0))
                priority = st.selectbox(
                    "Priority", 
                    ["Standard", "High", "Critical"],
                    key="delivery_priority"
                )
                delivery_location = st.text_input("Delivery Location", "North Loading Dock")
            
            notes = st.text_area("Delivery Notes", "Call site superintendent 30 minutes prior to arrival.")
            
            # Associated schedule task selection
            related_tasks = ["Foundation Work", "Structural Steel", "Curtain Wall Installation", "MEP Rough-In", "Interior Finishes"]
            associated_task = st.selectbox("Associated Schedule Task", related_tasks)
            
            # Form submission buttons
            submit_col1, submit_col2 = st.columns([1, 5])
            with submit_col1:
                submitted = st.form_submit_button("Save Delivery")
            with submit_col2:
                canceled = st.form_submit_button("Cancel")
            
            if submitted:
                st.success(f"Delivery for '{item_name}' scheduled for {delivery_date.strftime('%Y-%m-%d')} at {delivery_time.strftime('%H:%M')}")
                st.session_state.show_delivery_form = False
                st.rerun()
            
            if canceled:
                st.session_state.show_delivery_form = False
                st.rerun()

def filter_deliveries_by_date_range(deliveries_df, date_range):
    """Filter deliveries based on date range selection"""
    today = datetime.now().date()
    
    if date_range == "Today":
        return deliveries_df[deliveries_df['delivery_date'].dt.date == today]
    
    elif date_range == "This Week":
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        return deliveries_df[(deliveries_df['delivery_date'].dt.date >= week_start) & 
                             (deliveries_df['delivery_date'].dt.date <= week_end)]
    
    elif date_range == "This Month":
        month_start = today.replace(day=1)
        if today.month == 12:
            month_end = today.replace(year=today.year+1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = today.replace(month=today.month+1, day=1) - timedelta(days=1)
        return deliveries_df[(deliveries_df['delivery_date'].dt.date >= month_start) & 
                             (deliveries_df['delivery_date'].dt.date <= month_end)]
    
    elif date_range == "Next 30 Days":
        end_date = today + timedelta(days=30)
        return deliveries_df[(deliveries_df['delivery_date'].dt.date >= today) & 
                             (deliveries_df['delivery_date'].dt.date <= end_date)]
    
    # "All" option - return everything
    return deliveries_df

def render_delivery_list(deliveries_df):
    """Render deliveries in a list view"""
    # Sort by date
    deliveries_df = deliveries_df.sort_values('delivery_date')
    
    # Group by date
    current_date = None
    
    if len(deliveries_df) == 0:
        st.info("No deliveries found for the selected period.")
        return
    
    for _, row in deliveries_df.iterrows():
        delivery_date = row['delivery_date'].date()
        
        # Add date header when date changes
        if current_date != delivery_date:
            st.write(f"### {delivery_date.strftime('%A, %B %d, %Y')}")
            current_date = delivery_date
        
        # Create a card for each delivery
        with st.expander(f"{row['delivery_time'].strftime('%H:%M')} - {row['item_name']} ({row['quantity']} {row['unit']})"):
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown(f"**Item:** {row['item_name']}")
                st.markdown(f"**Supplier:** {row['supplier']}")
                st.markdown(f"**Quantity:** {row['quantity']} {row['unit']}")
                st.markdown(f"**Location:** {row['delivery_location']}")
                
            with col2:
                st.markdown(f"**Time:** {row['delivery_time'].strftime('%H:%M')}")
                st.markdown(f"**Priority:** {row['priority']}")
                st.markdown(f"**Status:** {row['status']}")
                st.markdown(f"**Task:** {row['related_task']}")
            
            if row['notes']:
                st.markdown(f"**Notes:** {row['notes']}")
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Mark as Received", key=f"receive_{row['id']}"):
                    update_delivery_status(row, "Received")
            with col2:
                if st.button("Report Delay", key=f"delay_{row['id']}"):
                    update_delivery_status(row, "Delayed")
            with col3:
                if st.button("Reschedule", key=f"reschedule_{row['id']}"):
                    st.session_state.reschedule_delivery_id = row['id']
                    st.session_state.show_reschedule_form = True
            with col4:
                st.button("View Details", key=f"details_{row['id']}")

def render_delivery_calendar(deliveries_df, month, year):
    """Render deliveries in a calendar view"""
    # Get the calendar for the selected month/year
    cal = calendar.monthcalendar(year, month)
    
    # Create a datetime object for the first day of the month
    first_day = datetime(year, month, 1)
    
    # Get the number of days in the month
    _, num_days = calendar.monthrange(year, month)
    
    # Create containers for each day in the calendar
    days_in_week = 7
    for week in cal:
        cols = st.columns(days_in_week)
        
        # For each day in the week
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:  # Day is outside the month
                    st.markdown("", unsafe_allow_html=True)
                else:
                    # Create date for this calendar day
                    day_date = datetime(year, month, day).date()
                    
                    # Check if today
                    is_today = day_date == datetime.now().date()
                    today_style = "background-color: #e6f3ff; border-radius: 5px; padding: 5px;" if is_today else ""
                    
                    # Get deliveries for this day
                    day_deliveries = deliveries_df[deliveries_df['delivery_date'].dt.date == day_date]
                    num_deliveries = len(day_deliveries)
                    
                    # Display the day with the number of deliveries
                    if num_deliveries > 0:
                        # Show day with deliveries count
                        header_color = "#4CAF50" if num_deliveries > 0 else "#666666"
                        st.markdown(f"""
                            <div style="{today_style}">
                                <div style="font-weight: bold; margin-bottom: 5px;">
                                    <span style="float: left;">{day}</span>
                                    <span style="float: right; background-color: {header_color}; color: white; border-radius: 50%; width: 25px; height: 25px; text-align: center; line-height: 25px;">{num_deliveries}</span>
                                    <div style="clear: both;"></div>
                                </div>
                        """, unsafe_allow_html=True)
                        
                        # List the deliveries for this day (limit to 3 with "more" link)
                        display_limit = 3
                        for i, (_, delivery) in enumerate(day_deliveries.iterrows()):
                            if i < display_limit:
                                priority_color = {
                                    "Critical": "#f44336",
                                    "High": "#ff9800",
                                    "Standard": "#4CAF50"
                                }.get(delivery['priority'], "#4CAF50")
                                
                                st.markdown(f"""
                                    <div style="font-size: 0.8em; margin-bottom: 3px; padding: 3px; border-left: 3px solid {priority_color};">
                                        {delivery['delivery_time'].strftime('%H:%M')} - {delivery['item_name'][:15]}...
                                    </div>
                                """, unsafe_allow_html=True)
                        
                        if num_deliveries > display_limit:
                            st.markdown(f"""
                                <div style="font-size: 0.8em; color: #0066cc; cursor: pointer;">
                                    + {num_deliveries - display_limit} more
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        # Just show the day number
                        st.markdown(f"""
                            <div style="{today_style}">
                                <div style="font-weight: bold; margin-bottom: 5px; color: #666666;">
                                    {day}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

def generate_sample_procurement_items():
    """Generate sample procurement data with delivery dates for demonstration"""
    # Define possible values for random generation
    item_names = [
        "Structural Steel", "Concrete Mix", "HVAC Equipment", "Electrical Panels",
        "Roofing Materials", "Windows", "Elevator Equipment", "Drywall", "Tiles",
        "Plumbing Fixtures", "Light Fixtures", "Flooring", "Exterior Cladding",
        "Security Systems", "Fire Protection Equipment", "Insulation", "Paint",
        "Interior Doors", "Exterior Doors", "Landscaping Materials"
    ]
    
    suppliers = [
        "ABC Construction Supply", "Highland Steel Co.", "Metro Building Materials",
        "City Electrical Supply", "Acme Glass & Metal", "Quality HVAC Systems",
        "Eagle Lumber", "Pro Interiors", "GlobalTech Systems", "Premium Fixtures Inc."
    ]
    
    locations = [
        "North Loading Dock", "South Entrance", "East Delivery Bay", 
        "West Storage Area", "Main Entrance", "Basement Access",
        "Tower Crane Drop Zone", "Material Storage Area A", "Material Storage Area B"
    ]
    
    units = ["Each", "Pallets", "Truckloads", "Cubic Yards", "Tons", "Square Feet", "Linear Feet"]
    
    priorities = ["Standard", "Standard", "Standard", "High", "High", "Critical"]
    
    statuses = ["On Schedule", "On Schedule", "On Schedule", "Delayed", "Early"]
    
    tasks = [
        "Foundation Work", "Structural Steel Erection", "Building Envelope", 
        "MEP Rough-In", "Interior Framing", "Drywall and Finishes", 
        "Exterior Finishes", "Site Work", "Final Inspections"
    ]
    
    notes = [
        "Call site superintendent 30 minutes prior to arrival.",
        "Requires tower crane for unloading.",
        "Delivery vehicle must be under 12 feet in height.",
        "Requires escort to delivery location.",
        "Materials to be inspected upon delivery.",
        "Fragile materials - handle with care.",
        "COO documentation required.",
        "",  # Empty string for some items having no notes
        "Delivery window: 7:00 AM - 11:00 AM only.",
        "Weekend delivery surcharge applies."
    ]
    
    # Create random dates for the next 60 days
    start_date = datetime.now()
    end_date = start_date + timedelta(days=60)
    
    # Generate sample data
    data = []
    for i in range(1, 51):  # 50 sample deliveries
        # Generate random date and time
        delivery_date = start_date + timedelta(days=random.randint(0, 60))
        hour = random.randint(7, 16)  # Deliveries between 7 AM and 4 PM
        minute = random.choice([0, 15, 30, 45])
        delivery_time = time(hour, minute)
        
        # Random item data
        item_name = random.choice(item_names)
        supplier = random.choice(suppliers)
        quantity = random.randint(1, 100)
        unit = random.choice(units)
        priority = random.choice(priorities)
        status = random.choice(statuses)
        location = random.choice(locations)
        related_task = random.choice(tasks)
        note = random.choice(notes)
        
        # Create entry
        data.append({
            'id': f"DEL-{2025}-{i:03d}",
            'item_name': item_name,
            'supplier': supplier,
            'quantity': quantity,
            'unit': unit,
            'delivery_date': pd.Timestamp(delivery_date),
            'delivery_time': delivery_time,
            'priority': priority,
            'status': status,
            'delivery_location': location,
            'related_task': related_task,
            'notes': note
        })
    
    return pd.DataFrame(data)

def update_delivery_status(delivery_data, new_status):
    """
    Update the status of a delivery and send notifications
    
    Args:
        delivery_data (dict): The delivery data to update
        new_status (str): The new status for the delivery
    """
    # In a real application, this would update the database
    # For now, just show a success message and send a notification
    
    delivery_id = delivery_data['id']
    item_name = delivery_data['item_name']
    
    notification_type = None
    additional_message = None
    
    # Set notification type and additional message based on new status
    if new_status == "Scheduled":
        notification_type = NotificationType.DELIVERY_SCHEDULED
        success_msg = f"Delivery for '{item_name}' has been scheduled."
    
    elif new_status == "Confirmed":
        notification_type = NotificationType.DELIVERY_CONFIRMED
        success_msg = f"Delivery for '{item_name}' has been confirmed by the supplier."
    
    elif new_status == "Delayed":
        notification_type = NotificationType.DELIVERY_DELAYED
        success_msg = f"Delivery for '{item_name}' has been marked as delayed."
        additional_message = "Please contact the project manager for more information."
    
    elif new_status == "Canceled":
        notification_type = NotificationType.DELIVERY_CANCELED
        success_msg = f"Delivery for '{item_name}' has been canceled."
        additional_message = "Please contact procurement to reschedule."
    
    elif new_status == "Received":
        notification_type = NotificationType.DELIVERY_ARRIVED
        success_msg = f"Delivery for '{item_name}' has been marked as received."
    
    elif new_status == "Incomplete":
        notification_type = NotificationType.DELIVERY_INCOMPLETE
        success_msg = f"Delivery for '{item_name}' has been marked as incomplete."
        additional_message = "Please document any missing or damaged items."
    
    # If we have a valid notification type, send the notification
    if notification_type:
        # Get the recipients based on user roles (simplified for demo)
        recipients = ["project_manager", "site_superintendent"]
        
        # Get other interested parties based on the affected tasks
        if "related_task" in delivery_data:
            task = delivery_data["related_task"]
            if "Concrete" in task or "Foundation" in task:
                recipients.append("concrete_foreman")
            elif "Steel" in task:
                recipients.append("steel_foreman")
            elif "MEP" in task:
                recipients.append("mep_coordinator")
        
        # Send the notification
        success = send_delivery_notification(
            delivery_data=delivery_data,
            notification_type=notification_type,
            recipients=recipients,
            additional_message=additional_message
        )
        
        if success:
            st.success(success_msg)
        else:
            st.warning(f"Status updated to {new_status}, but there was an issue sending notifications.")
    else:
        st.success(f"Delivery status updated to {new_status}.")

def render_reschedule_form(delivery_id):
    """
    Render a form to reschedule a delivery
    
    Args:
        delivery_id (str): The ID of the delivery to reschedule
    """
    # In a real application, we would fetch the delivery data from the database
    # For this demo, we'll create sample data
    
    delivery_data = {
        'id': delivery_id,
        'item_name': "Sample Item",
        'supplier': "Sample Supplier",
        'delivery_date': datetime.now() + timedelta(days=3),
        'delivery_time': time(9, 0),
    }
    
    with st.form(key=f"reschedule_form_{delivery_id}"):
        st.subheader(f"Reschedule Delivery: {delivery_data['item_name']}")
        
        # Date and time selection
        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input(
                "New Delivery Date", 
                delivery_data['delivery_date']
            )
        
        with col2:
            new_time = st.time_input(
                "New Delivery Time",
                delivery_data['delivery_time']
            )
        
        # Reason for rescheduling
        reason = st.selectbox(
            "Reason for Rescheduling",
            ["Supplier Request", "Site Not Ready", "Weather Conditions", "Material Shortages", "Other"]
        )
        
        if reason == "Other":
            other_reason = st.text_input("Specify Reason")
        
        # Notes
        notes = st.text_area("Additional Notes", "")
        
        # Notify options
        notify_options = st.multiselect(
            "Notify",
            ["Supplier", "Project Manager", "Site Superintendent", "Subcontractors"],
            default=["Supplier", "Project Manager"]
        )
        
        # Submit buttons
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Save Changes")
        with col2:
            canceled = st.form_submit_button("Cancel")
        
        if submitted:
            # Update delivery data
            delivery_data['delivery_date'] = new_date
            delivery_data['delivery_time'] = new_time
            
            # In a real app, save this to the database
            
            # Send notification about rescheduled delivery
            notification_type = NotificationType.DELIVERY_SCHEDULED
            recipients = []
            
            if "Supplier" in notify_options:
                recipients.append("supplier")
            if "Project Manager" in notify_options:
                recipients.append("project_manager")
            if "Site Superintendent" in notify_options:
                recipients.append("site_superintendent")
            if "Subcontractors" in notify_options:
                recipients.append("subcontractors")
            
            additional_message = f"This delivery has been rescheduled. Reason: {reason if reason != 'Other' else other_reason}."
            if notes:
                additional_message += f" Notes: {notes}"
            
            success = send_delivery_notification(
                delivery_data=delivery_data,
                notification_type=notification_type,
                recipients=recipients,
                additional_message=additional_message
            )
            
            if success:
                st.success(f"Delivery for '{delivery_data['item_name']}' has been rescheduled. Notifications sent.")
            else:
                st.warning(f"Delivery rescheduled, but there was an issue sending notifications.")
            
            # Clear the form
            st.session_state.show_reschedule_form = False
            st.session_state.reschedule_delivery_id = None
            st.rerun()
        
        if canceled:
            st.session_state.show_reschedule_form = False
            st.session_state.reschedule_delivery_id = None
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