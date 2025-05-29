"""
Daily Reports Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import check_authentication, initialize_session_state, clean_dataframe_for_display

# Import database modules
try:
    from database.connection import save_daily_report, get_daily_reports
    from modules.file_manager import render_document_upload_section
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

st.set_page_config(
    page_title="Daily Reports - gcPanel",
    page_icon="📋",
    layout="wide"
)

# Initialize session state
initialize_session_state()

if not check_authentication():
    st.switch_page("app.py")

st.title("📋 Daily Reports")
st.markdown("Highland Tower Development - Daily Progress Documentation")
st.markdown("---")

# Initialize daily reports in session state if not exists
if 'daily_reports' not in st.session_state:
    st.session_state.daily_reports = [
        {
            "id": 1,
            "date": "2024-12-15",
            "weather": "Partly Cloudy",
            "temperature": 45,
            "wind": "5-10 mph",
            "crew_size": 24,
            "work_performed": "Foundation work on Level B2, concrete pour for north wall",
            "issues_delays": "Delivery of reinforcement bars delayed by 2 hours",
            "tomorrow_plan": "Continue foundation work, install waterproofing membrane",
            "safety_incidents": "None reported",
            "inspections": "Structural inspection passed for columns C1-C8",
            "materials_delivered": "40 tons rebar, 120 cubic yards concrete",
            "created_by": "Site Superintendent",
            "status": "Active"
        }
    ]

# Main content
tab1, tab2 = st.tabs(["📊 Daily Reports", "📝 Create New Report"])

with tab1:
    st.subheader("📊 Daily Reports Database")
    
    # Load reports from database or session
    all_reports = []
    if DATABASE_AVAILABLE:
        try:
            db_reports = get_daily_reports()
            if db_reports:
                all_reports = db_reports
            else:
                all_reports = st.session_state.daily_reports
        except Exception as e:
            st.warning(f"Database unavailable, showing session data: {str(e)}")
            all_reports = st.session_state.daily_reports
    else:
        all_reports = st.session_state.daily_reports
    
    if all_reports:
        df = pd.DataFrame(all_reports)
        
        # Search and filter
        col1, col2 = st.columns([2, 1])
        with col1:
            search_term = st.text_input("🔍 Search reports...", placeholder="Search by date, weather, or work performed", key="daily_reports_search_1")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Active", "Archived"])
        
        # Filter data
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[
                filtered_df.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)
            ]
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df.get('status', 'Active') == status_filter]
        
        # Display results
        st.write(f"**Total Reports:** {len(filtered_df)}")
        
        if not filtered_df.empty:
            # Clean the dataframe for display
            display_df = clean_dataframe_for_display(filtered_df)
            
            # Display with column configuration
            st.dataframe(
                display_df,
                column_config={
                    "date": st.column_config.DateColumn("Date"),
                    "weather": st.column_config.TextColumn("Weather"),
                    "temperature": st.column_config.NumberColumn("Temperature (°F)"),
                    "crew_size": st.column_config.NumberColumn("Crew Size"),
                    "status": st.column_config.SelectboxColumn("Status", options=["Active", "Archived"])
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No reports found matching your criteria.")
    else:
        st.info("No daily reports available. Create your first report in the Create tab!")

with tab2:
    st.subheader("📝 Create New Daily Report")
    
    with st.form("daily_report_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            report_date = st.date_input("Report Date", value=date.today())
            weather = st.selectbox("Weather Conditions", 
                ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Snow", "Windy"])
            temperature = st.number_input("Temperature (°F)", min_value=-20, max_value=120, value=50)
            wind = st.text_input("Wind Conditions", placeholder="e.g., 5-10 mph NE")
            crew_size = st.number_input("Crew Size", min_value=0, max_value=100, value=20)
        
        with col2:
            work_performed = st.text_area("Work Performed Today", height=100,
                placeholder="Describe the main work activities completed...")
            issues_delays = st.text_area("Issues & Delays", height=100,
                placeholder="Report any issues, delays, or problems encountered...")
            tomorrow_plan = st.text_area("Tomorrow's Plan", height=100,
                placeholder="Outline planned activities for the next day...")
        
        col3, col4 = st.columns(2)
        with col3:
            safety_incidents = st.text_area("Safety Incidents", height=68,
                placeholder="Report any safety incidents or near misses...")
            inspections = st.text_area("Inspections Completed", height=68,
                placeholder="List inspections completed today...")
        
        with col4:
            materials_delivered = st.text_area("Materials Delivered", height=68,
                placeholder="List materials and quantities delivered...")
        
        # File upload section within the form
        st.markdown("**📎 Attachments (Optional)**")
        if DATABASE_AVAILABLE:
            try:
                uploaded_files = render_document_upload_section()
            except:
                st.info("File upload functionality temporarily unavailable")
        
        submitted = st.form_submit_button("💾 Save Daily Report", type="primary", use_container_width=True)
        
        if submitted:
            new_report = {
                "date": str(report_date),
                "weather": weather,
                "temperature": temperature,
                "wind": wind,
                "crew_size": crew_size,
                "work_performed": work_performed,
                "issues_delays": issues_delays,
                "tomorrow_plan": tomorrow_plan,
                "safety_incidents": safety_incidents,
                "inspections": inspections,
                "materials_delivered": materials_delivered
            }
            
            # Save to database if available
            if DATABASE_AVAILABLE:
                try:
                    if save_daily_report(new_report):
                        st.success("Daily report saved to database successfully!")
                    else:
                        st.error("Failed to save to database, saved to session instead")
                        # Fallback to session storage
                        new_report["id"] = len(st.session_state.daily_reports) + 1
                        new_report["created_by"] = "Site Superintendent"
                        new_report["status"] = "Active"
                        st.session_state.daily_reports.insert(0, new_report)
                except Exception as e:
                    st.error(f"Database error: {str(e)}")
                    # Fallback to session storage
                    new_report["id"] = len(st.session_state.daily_reports) + 1
                    new_report["created_by"] = "Site Superintendent"
                    new_report["status"] = "Active"
                    st.session_state.daily_reports.insert(0, new_report)
            else:
                # Fallback to session storage
                new_report["id"] = len(st.session_state.daily_reports) + 1
                new_report["created_by"] = "Site Superintendent"
                new_report["status"] = "Active"
                st.session_state.daily_reports.insert(0, new_report)
                st.success("Daily report saved successfully!")
            
            st.rerun()

