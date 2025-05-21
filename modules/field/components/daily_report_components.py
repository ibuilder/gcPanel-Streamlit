"""
Daily Report components for the Field module.

This module provides the UI components for daily report management including:
- Daily report list view
- Daily report details view
- Daily report form (add/edit)
- Daily report analysis view
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data for demonstration
def generate_sample_daily_reports():
    """Generate sample daily report data for demonstration"""
    return [
        {
            "ID": "DR-2025-001",
            "Date": "2025-01-15",
            "Author": "David Kim",
            "Weather": "Sunny, 72°F",
            "Work_Areas": ["Foundation", "Site Work"],
            "Workers_Count": 28,
            "Equipment_Count": 6,
            "Status": "Complete"
        },
        {
            "ID": "DR-2025-002",
            "Date": "2025-01-16",
            "Author": "Sarah Williams",
            "Weather": "Partly Cloudy, 68°F",
            "Work_Areas": ["Foundation", "Structural Steel"],
            "Workers_Count": 32,
            "Equipment_Count": 7,
            "Status": "Complete"
        },
        {
            "ID": "DR-2025-003",
            "Date": "2025-01-17",
            "Author": "Michael Davis",
            "Weather": "Rainy, 58°F",
            "Work_Areas": ["Site Work"],
            "Workers_Count": 15,
            "Equipment_Count": 4,
            "Status": "Complete"
        },
        {
            "ID": "DR-2025-004",
            "Date": "2025-01-18",
            "Author": "Jennifer Wilson",
            "Weather": "Sunny, 75°F",
            "Work_Areas": ["Foundation", "Structural Steel"],
            "Workers_Count": 34,
            "Equipment_Count": 8,
            "Status": "Complete"
        },
        {
            "ID": "DR-2025-005",
            "Date": "2025-01-19",
            "Author": "James Smith",
            "Weather": "Cloudy, 65°F",
            "Work_Areas": ["Foundation", "Structural Steel", "Electrical"],
            "Workers_Count": 38,
            "Equipment_Count": 9,
            "Status": "Complete"
        },
        {
            "ID": "DR-2025-006",
            "Date": "2025-01-20",
            "Author": "Emma Brown",
            "Weather": "Sunny, 78°F",
            "Work_Areas": ["Structural Steel", "Concrete", "Electrical"],
            "Workers_Count": 42,
            "Equipment_Count": 10,
            "Status": "Complete"
        },
        {
            "ID": "DR-2025-007",
            "Date": "2025-01-21",
            "Author": "David Kim",
            "Weather": "Sunny, 76°F",
            "Work_Areas": ["Structural Steel", "MEP Rough-in"],
            "Workers_Count": 45,
            "Equipment_Count": 11,
            "Status": "Complete"
        }
    ]

def render_daily_report_list():
    """Render the daily report list view with filtering and sorting"""
    st.subheader("Daily Reports")
    
    # Get sample data
    reports = generate_sample_daily_reports()
    
    with st.expander("Filters", expanded=True):
        # Create columns for the filters
        col1, col2 = st.columns(2)
        
        with col1:
            # Date range filter
            min_date = min(datetime.strptime(report["Date"], "%Y-%m-%d") for report in reports)
            max_date = max(datetime.strptime(report["Date"], "%Y-%m-%d") for report in reports)
            
            start_date = st.date_input(
                "Start Date",
                value=min_date,
                key="report_start_date"
            )
            
            end_date = st.date_input(
                "End Date",
                value=max_date,
                key="report_end_date"
            )
        
        with col2:
            # Author filter
            authors = ["All Authors"] + sorted(list(set(report["Author"] for report in reports)))
            selected_author = st.selectbox("Author", authors, key="report_author_filter")
            
            # Work area filter
            all_areas = []
            for report in reports:
                all_areas.extend(report["Work_Areas"])
            unique_areas = ["All Areas"] + sorted(list(set(all_areas)))
            selected_area = st.selectbox("Work Area", unique_areas, key="report_area_filter")
            
            # Search field
            search_term = st.text_input("Search", key="report_search", placeholder="Search reports...")
    
    # Filter the data based on selections
    filtered_reports = reports
    
    # Filter by date range
    filtered_reports = [
        report for report in filtered_reports 
        if start_date <= datetime.strptime(report["Date"], "%Y-%m-%d").date() <= end_date
    ]
    
    if selected_author != "All Authors":
        filtered_reports = [report for report in filtered_reports if report["Author"] == selected_author]
    
    if selected_area != "All Areas":
        filtered_reports = [report for report in filtered_reports if selected_area in report["Work_Areas"]]
    
    if search_term:
        filtered_reports = [report for report in filtered_reports if 
                          search_term.lower() in report["ID"].lower() or
                          search_term.lower() in report["Author"].lower() or
                          search_term.lower() in report["Weather"].lower()]

    # Add button
    if st.button("➕ Add Daily Report", use_container_width=True):
        st.session_state.daily_report_view = "add"
        st.rerun()
    
    # Check if we have any results
    if not filtered_reports:
        st.info("No daily reports match your filters.")
        return
    
    # Show item count
    st.caption(f"Showing {len(filtered_reports)} daily reports")
    
    # Display the filtered reports
    for report in filtered_reports:
        # Create a container for each report
        report_container = st.container()
        
        with report_container:
            # Add a subtle divider between reports
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
            
            # Create a row with columns for the report data and action buttons
            row_container = st.container()
            
            # Create a more balanced row layout with condensed columns
            col1, col2, col3, col4, col_actions = row_container.columns([0.8, 3, 2, 1.5, 0.7])
            
            with col1:
                st.write(f"**{report['Date']}**")
                st.caption(f"{report['ID']}")
            
            with col2:
                st.write(f"📋 **Daily Report**")
                st.caption(f"Author: {report['Author']}")
            
            with col3:
                # Work areas list
                areas_text = ", ".join(report["Work_Areas"])
                st.markdown(f"<small><b>Work Areas:</b><br>{areas_text}</small>", unsafe_allow_html=True)
            
            with col4:
                # Weather and workforce
                st.markdown(f"<small><b>Weather:</b><br>{report['Weather']}</small>", unsafe_allow_html=True)
                st.markdown(f"<small><b>Workforce:</b> {report['Workers_Count']} workers, {report['Equipment_Count']} equipment</small>", unsafe_allow_html=True)
            
            # Action buttons in a single column
            with col_actions:
                # Create two buttons side by side in the actions column
                action_btn_cols = st.columns(2)
                
                # View button
                with action_btn_cols[0]:
                    if st.button("👁️", key=f"view_{report['ID']}", help="View daily report details"):
                        # Store report details in session state
                        st.session_state.selected_daily_report_id = report['ID'] 
                        st.session_state.selected_daily_report_data = report
                        # Set view mode
                        st.session_state["daily_report_view"] = "view"
                        # Force refresh
                        st.rerun()
                
                # Edit button
                with action_btn_cols[1]:
                    if st.button("✏️", key=f"edit_{report['ID']}", help="Edit daily report"):
                        # Store report data for editing
                        st.session_state.edit_daily_report_id = report['ID']
                        st.session_state.edit_daily_report_data = report
                        # Set edit mode 
                        st.session_state["daily_report_view"] = "edit"
                        # Force refresh
                        st.rerun()

def render_daily_report_details():
    """Render the daily report details view (single record view)"""
    st.subheader("Daily Report Details")
    
    # Ensure we have a selected report
    if not st.session_state.get("selected_daily_report_id"):
        st.error("No daily report selected. Please select a report from the list.")
        # Return to list view
        st.session_state.daily_report_view = "list"
        st.rerun()
        return
    
    # Get the selected report data
    report = st.session_state.get("selected_daily_report_data", None)
    
    if not report:
        # If somehow we have an ID but no data, try to find it
        reports = generate_sample_daily_reports()
        report = next((r for r in reports if r["ID"] == st.session_state.selected_daily_report_id), None)
        
        if not report:
            st.error(f"Daily report with ID {st.session_state.selected_daily_report_id} not found.")
            # Return to list view
            st.session_state.daily_report_view = "list"
            st.rerun()
            return
    
    # Display report details
    with st.container():
        # Style for report details
        st.markdown("""
        <style>
            .report-details {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
            }
            .report-header {
                margin-bottom: 20px;
            }
            .report-section {
                margin-top: 15px;
                margin-bottom: 15px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Start report details container
        st.markdown('<div class="report-details">', unsafe_allow_html=True)
        
        # Header section
        st.markdown(f'<div class="report-header">', unsafe_allow_html=True)
        st.markdown(f"# Daily Report - {report['Date']}")
        st.markdown(f"#### ID: {report['ID']} | Author: {report['Author']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Weather and site conditions
        st.markdown(f'<div class="report-section">', unsafe_allow_html=True)
        st.markdown("### Weather and Site Conditions")
        st.markdown(f"**Weather:** {report['Weather']}")
        
        # Generate random site conditions
        site_conditions = [
            "Site conditions were good for work.",
            "Site had wet conditions due to recent rain, but work continued.",
            "Excellent site conditions, no impediments to work.",
            "Some areas of site required additional drainage due to groundwater.",
            "Site access was temporarily restricted in the morning due to material delivery."
        ]
        
        st.markdown(f"**Site Conditions:** {random.choice(site_conditions)}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Workforce
        st.markdown(f'<div class="report-section">', unsafe_allow_html=True)
        st.markdown("### Workforce")
        
        # Create a table of contractors and workers
        contractors = [
            {"name": "General Contractor", "workers": int(report["Workers_Count"] * 0.3)},
            {"name": "Structural Subcontractor", "workers": int(report["Workers_Count"] * 0.25)},
            {"name": "Electrical Subcontractor", "workers": int(report["Workers_Count"] * 0.15)},
            {"name": "Mechanical Subcontractor", "workers": int(report["Workers_Count"] * 0.15)},
            {"name": "Other Subcontractors", "workers": report["Workers_Count"] - int(report["Workers_Count"] * 0.85)}
        ]
        
        df_contractors = pd.DataFrame(contractors)
        st.dataframe(df_contractors, use_container_width=True)
        
        st.markdown(f"**Total Workers On Site:** {report['Workers_Count']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Equipment
        st.markdown(f'<div class="report-section">', unsafe_allow_html=True)
        st.markdown("### Equipment")
        
        # Generate random equipment
        equipment_types = ["Excavator", "Bulldozer", "Crane", "Concrete Pump", "Forklift", 
                          "Dump Truck", "Backhoe", "Loader", "Generator", "Compressor"]
        
        equipment = []
        for i in range(report["Equipment_Count"]):
            equipment.append({
                "Equipment Type": random.choice(equipment_types),
                "Quantity": random.randint(1, 3),
                "Hours": random.randint(4, 10),
                "Status": random.choice(["Active", "Standby", "Maintenance"])
            })
        
        df_equipment = pd.DataFrame(equipment)
        st.dataframe(df_equipment, use_container_width=True)
        
        st.markdown(f"**Total Equipment On Site:** {report['Equipment_Count']} units")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Work performed
        st.markdown(f'<div class="report-section">', unsafe_allow_html=True)
        st.markdown("### Work Performed")
        
        # Generate work descriptions for each area
        for area in report["Work_Areas"]:
            work_descriptions = [
                f"Continued {area.lower()} work according to schedule.",
                f"Completed phase 1 of {area.lower()} activities.",
                f"Began installation of {area.lower()} components.",
                f"Conducted inspection of {area.lower()} work completed yesterday.",
                f"Made progress on {area.lower()} ahead of schedule."
            ]
            
            st.markdown(f"**{area}:** {random.choice(work_descriptions)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Materials
        st.markdown(f'<div class="report-section">', unsafe_allow_html=True)
        st.markdown("### Materials")
        
        # Generate random material deliveries
        has_deliveries = random.choice([True, False])
        
        if has_deliveries:
            material_types = ["Concrete", "Rebar", "Structural Steel", "Lumber", "Conduit", 
                            "Electrical Cable", "Drywall", "Piping", "HVAC Equipment", "Insulation"]
            
            deliveries = []
            for i in range(random.randint(1, 3)):
                deliveries.append({
                    "Material": random.choice(material_types),
                    "Quantity": f"{random.randint(10, 1000)} {random.choice(['cu.yd', 'tons', 'pcs', 'sq.ft', 'rolls'])}",
                    "Supplier": random.choice(["ABC Supply Co.", "XYZ Materials", "Metro Building Supplies", "United Industrial"]),
                    "Status": "Received"
                })
            
            df_deliveries = pd.DataFrame(deliveries)
            st.dataframe(df_deliveries, use_container_width=True)
        else:
            st.info("No material deliveries recorded for this day.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quality/Safety
        st.markdown(f'<div class="report-section">', unsafe_allow_html=True)
        st.markdown("### Quality & Safety")
        
        # Generate random safety observations
        safety_notes = [
            "No safety incidents reported. Toolbox talk conducted on proper lifting techniques.",
            "Safety inspection conducted by site safety officer. Minor corrections requested.",
            "One near-miss reported and documented. Additional safety briefing scheduled.",
            "All safety protocols followed. No issues to report.",
            "Safety audit conducted by corporate safety team. Site received good marks."
        ]
        
        st.markdown(f"**Safety Notes:** {random.choice(safety_notes)}")
        
        # Generate random quality observations
        quality_notes = [
            "Quality inspection of recent concrete pour completed. Results satisfactory.",
            "QA/QC team reviewed installation of structural components. All within specifications.",
            "Material testing conducted on recent deliveries. All materials meet project requirements.",
            "Quality control checks implemented for all completed work. Documentation updated.",
            "Third-party inspector reviewed recent work. No significant issues found."
        ]
        
        st.markdown(f"**Quality Notes:** {random.choice(quality_notes)}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Issues/Concerns
        st.markdown(f'<div class="report-section">', unsafe_allow_html=True)
        st.markdown("### Issues & Concerns")
        
        # Generate random issues
        has_issues = random.choice([True, False])
        
        if has_issues:
            issues = [
                "Delivery of mechanical equipment delayed by supplier. May impact schedule if not resolved soon.",
                "Discrepancy found between electrical drawings and site conditions. RFI submitted for clarification.",
                "Weather forecast shows potential storms later this week. Preparing contingency plans.",
                "Unexpected soil conditions discovered in north section. Geotechnical engineer notified.",
                "Subcontractor staffing below committed levels. Issue raised with subcontractor management."
            ]
            
            st.markdown(f"• {random.choice(issues)}")
        else:
            st.info("No significant issues or concerns to report.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Photos (placeholder)
        st.markdown(f'<div class="report-section">', unsafe_allow_html=True)
        st.markdown("### Site Photos")
        
        # Add placeholder for photos
        st.info("Photos are not available in this view. Please check the detailed report.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Edit Report", use_container_width=True):
                st.session_state.edit_daily_report_id = report['ID']
                st.session_state.edit_daily_report_data = report
                st.session_state.daily_report_view = "edit"
                st.rerun()
        
        with col2:
            if st.button("📊 View Analysis", use_container_width=True):
                st.session_state.daily_report_view = "analysis"
                st.rerun()
        
        # End the report details container
        st.markdown('</div>', unsafe_allow_html=True)


def render_daily_report_form(is_edit=False):
    """Render the daily report creation/edit form"""
    if is_edit:
        st.subheader("Edit Daily Report")
        # Ensure we have a report to edit
        if not st.session_state.get("edit_daily_report_id"):
            st.error("No daily report selected for editing. Please select a report from the list.")
            # Return to list view
            st.session_state.daily_report_view = "list"
            st.rerun()
            return
        
        # Get the report data for editing
        report = st.session_state.get("edit_daily_report_data", {})
    else:
        st.subheader("Create New Daily Report")
        # Initialize empty report for new entries
        today = datetime.now()
        report = {
            "ID": f"DR-{today.year}-{random.randint(100, 999)}",
            "Date": today.strftime("%Y-%m-%d"),
            "Author": "",
            "Weather": "",
            "Work_Areas": [],
            "Workers_Count": 0,
            "Equipment_Count": 0,
            "Status": "Draft"
        }
    
    # Create the form
    with st.form(key="daily_report_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            # For display only
            if is_edit:
                st.text_input("Report ID", value=report.get("ID", ""), disabled=True)
            
            report_date = st.date_input(
                "Report Date *",
                value=datetime.strptime(report.get("Date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
            )
        
        with col2:
            author = st.text_input("Author *", value=report.get("Author", ""))
            
            # Status dropdown
            status_options = ["Draft", "Complete"]
            
            # Find index of selected status if editing
            status_index = 0
            if is_edit and report.get("Status") in status_options:
                status_index = status_options.index(report.get("Status"))
            
            selected_status = st.selectbox(
                "Status *",
                status_options,
                index=status_index
            )
        
        # Weather and site conditions
        st.subheader("Weather and Site Conditions")
        col1, col2 = st.columns(2)
        
        with col1:
            weather = st.text_input(
                "Weather Conditions *", 
                value=report.get("Weather", ""),
                placeholder="e.g., Sunny, 72°F"
            )
        
        with col2:
            temperature = st.slider(
                "Temperature (°F)",
                min_value=0,
                max_value=100,
                value=72,
                step=1
            )
        
        site_conditions = st.text_area(
            "Site Conditions",
            value=report.get("Site_Conditions", ""),
            height=100,
            placeholder="Describe current site conditions..."
        )
        
        # Work areas
        st.subheader("Work Areas")
        
        # Available work areas
        all_work_areas = ["Foundation", "Site Work", "Structural Steel", "Concrete", "Masonry", 
                         "Mechanical", "Electrical", "Plumbing", "Drywall", "Finishes", "Roofing", 
                         "MEP Rough-in", "Interior Framing", "Exterior Envelope"]
        
        # Multi-select for work areas
        selected_work_areas = st.multiselect(
            "Select Work Areas *",
            all_work_areas,
            default=report.get("Work_Areas", [])
        )
        
        # Workforce
        st.subheader("Workforce")
        col1, col2 = st.columns(2)
        
        with col1:
            workers_count = st.number_input(
                "Total Workers On Site *",
                min_value=0,
                value=int(report.get("Workers_Count", 0)),
                step=1
            )
        
        with col2:
            equipment_count = st.number_input(
                "Total Equipment On Site *",
                min_value=0,
                value=int(report.get("Equipment_Count", 0)),
                step=1
            )
        
        # Work performed
        st.subheader("Work Performed")
        work_performed = st.text_area(
            "Work Performed *",
            value=report.get("Work_Performed", ""),
            height=200,
            placeholder="Describe work performed in each area..."
        )
        
        # Materials
        st.subheader("Materials")
        materials_delivered = st.text_area(
            "Materials Delivered",
            value=report.get("Materials_Delivered", ""),
            height=100,
            placeholder="List materials delivered to site..."
        )
        
        # Quality/Safety
        st.subheader("Quality & Safety")
        col1, col2 = st.columns(2)
        
        with col1:
            safety_notes = st.text_area(
                "Safety Notes",
                value=report.get("Safety_Notes", ""),
                height=100,
                placeholder="Document safety observations, incidents, or concerns..."
            )
        
        with col2:
            quality_notes = st.text_area(
                "Quality Notes",
                value=report.get("Quality_Notes", ""),
                height=100,
                placeholder="Document quality control activities and observations..."
            )
        
        # Issues/Concerns
        st.subheader("Issues & Concerns")
        issues = st.text_area(
            "Issues & Concerns",
            value=report.get("Issues", ""),
            height=100,
            placeholder="Document any issues or concerns that need attention..."
        )
        
        # Photos
        st.subheader("Site Photos")
        uploaded_files = st.file_uploader("Upload Site Photos", accept_multiple_files=True)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "Save Report" if is_edit else "Create Report",
                use_container_width=True
            )
        
        with col2:
            cancel_button = st.form_submit_button(
                "Cancel",
                use_container_width=True
            )
    
    # Handle form submission
    if submit_button:
        # Validate required fields
        if not author:
            st.error("Please enter an author name.")
            return
        
        if not weather:
            st.error("Please enter weather conditions.")
            return
        
        if not selected_work_areas:
            st.error("Please select at least one work area.")
            return
        
        if not work_performed:
            st.error("Please describe work performed.")
            return
            
        # In a real app, this would save to database
        if is_edit:
            st.success(f"Daily report for {report_date.strftime('%Y-%m-%d')} updated successfully!")
        else:
            st.success(f"Daily report for {report_date.strftime('%Y-%m-%d')} created successfully!")
        
        # Return to list view
        st.session_state.daily_report_view = "list"
        st.rerun()
    
    if cancel_button:
        # Return to previous view
        st.session_state.daily_report_view = "list"
        st.rerun()


def render_daily_report_analysis():
    """Render the daily report analysis view with charts and metrics"""
    st.subheader("Daily Report Analysis")
    
    # Get sample data
    reports = generate_sample_daily_reports()
    
    # Calculate summary metrics
    total_reports = len(reports)
    total_workers = sum(report["Workers_Count"] for report in reports)
    total_equipment = sum(report["Equipment_Count"] for report in reports)
    avg_workers = total_workers / total_reports if total_reports > 0 else 0
    
    # Summary metrics
    st.subheader("Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reports", f"{total_reports}")
    
    with col2:
        st.metric("Total Workers", f"{total_workers}")
    
    with col3:
        st.metric("Total Equipment", f"{total_equipment}")
    
    with col4:
        st.metric("Avg. Workers/Day", f"{avg_workers:.1f}")
    
    # Workforce trend
    st.subheader("Workforce Trend")
    
    # Prepare data for workforce trend chart
    workforce_trend = []
    for report in sorted(reports, key=lambda x: x["Date"]):
        workforce_trend.append({
            "Date": report["Date"],
            "Workers": report["Workers_Count"],
            "Equipment": report["Equipment_Count"]
        })
    
    # Create a DataFrame
    workforce_df = pd.DataFrame(workforce_trend)
    
    # Display the chart
    st.line_chart(workforce_df.set_index('Date'))
    
    # Work area analysis
    st.subheader("Work Area Analysis")
    
    # Count occurrences of each work area
    area_counts = {}
    for report in reports:
        for area in report["Work_Areas"]:
            if area in area_counts:
                area_counts[area] += 1
            else:
                area_counts[area] = 1
    
    # Create a DataFrame
    area_df = pd.DataFrame({
        'Work Area': list(area_counts.keys()),
        'Days Active': list(area_counts.values())
    })
    
    # Sort by days active
    area_df = area_df.sort_values('Days Active', ascending=False)
    
    # Display the chart
    st.bar_chart(area_df.set_index('Work Area'))
    
    # Weather impact analysis
    st.subheader("Weather Analysis")
    
    # Analyze weather patterns
    weather_patterns = {}
    for report in reports:
        weather_type = report["Weather"].split(',')[0]  # Extract weather type (e.g., "Sunny" from "Sunny, 72°F")
        if weather_type in weather_patterns:
            weather_patterns[weather_type] += 1
        else:
            weather_patterns[weather_type] = 1
    
    # Create a DataFrame
    weather_df = pd.DataFrame({
        'Weather': list(weather_patterns.keys()),
        'Days': list(weather_patterns.values())
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Display pie chart
        st.write("#### Weather Distribution")
        st.dataframe(weather_df, use_container_width=True)
    
    with col2:
        # Calculate workforce by weather
        weather_workforce = {}
        for report in reports:
            weather_type = report["Weather"].split(',')[0]
            if weather_type in weather_workforce:
                weather_workforce[weather_type]["Workers"].append(report["Workers_Count"])
            else:
                weather_workforce[weather_type] = {"Workers": [report["Workers_Count"]]}
        
        # Calculate averages
        weather_avg_workforce = []
        for weather, data in weather_workforce.items():
            avg_workers = sum(data["Workers"]) / len(data["Workers"])
            weather_avg_workforce.append({
                "Weather": weather,
                "Avg. Workers": avg_workers
            })
        
        # Create a DataFrame
        weather_workers_df = pd.DataFrame(weather_avg_workforce)
        
        st.write("#### Avg. Workforce by Weather")
        st.dataframe(weather_workers_df, use_container_width=True)