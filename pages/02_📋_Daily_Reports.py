"""
Daily Reports Page - Highland Tower Development
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.utils.helpers import check_authentication

st.set_page_config(page_title="Daily Reports - gcPanel", page_icon="📋", layout="wide")

# Check authentication
if not check_authentication():
    st.error("🔒 Please log in to access this page")
    st.stop()


st.title("📋 Daily Reports")
st.markdown("Highland Tower Development - Daily Progress & Activity Reports")
st.markdown("---")

# Initialize session state for daily reports
if 'daily_reports' not in st.session_state:
    st.session_state.daily_reports = [
        {
            "id": "DR-001",
            "date": "2024-12-15",
            "weather": "Clear, 45°F",
            "crew_count": 45,
            "hours_worked": 360,
            "activities": "Structural steel installation - Floor 22",
            "progress": "85% complete on Floor 22 framing",
            "issues": "None reported",
            "safety_incidents": 0
        }
    ]

# Main tabs
tab1, tab2, tab3 = st.tabs(["📊 Reports Database", "📝 Create Report", "📈 Progress Summary"])

with tab1:
    st.subheader("📊 Daily Reports Database")
    if st.session_state.daily_reports:
        df = pd.DataFrame(st.session_state.daily_reports)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No daily reports available")

with tab2:
    st.subheader("📝 Create Daily Report")
    st.info("Daily report creation form coming soon")

with tab3:
    st.subheader("📈 Progress Summary")
    if st.session_state.daily_reports:
        df = pd.DataFrame(st.session_state.daily_reports)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_reports = len(st.session_state.daily_reports)
            st.metric("Total Reports", total_reports)
        
        with col2:
            total_hours = sum(report['hours_worked'] for report in st.session_state.daily_reports)
            st.metric("Total Hours", f"{total_hours:,}")
        
        with col3:
            total_crew = sum(report['crew_count'] for report in st.session_state.daily_reports)
            avg_crew = total_crew / len(st.session_state.daily_reports) if st.session_state.daily_reports else 0
            st.metric("Avg Crew Size", f"{avg_crew:.1f}")
        
        with col4:
            safety_incidents = sum(report['safety_incidents'] for report in st.session_state.daily_reports)
            st.metric("Safety Incidents", safety_incidents)
        
        # Progress tracking
        st.subheader("Daily Progress Tracking")
        st.write("**Recent Activities:**")
        for report in st.session_state.daily_reports:
            st.write(f"• {report['date']}: {report['activities']}")
    else:
        st.info("No daily reports available for analysis")
